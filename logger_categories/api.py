import calendar
import inquirer
import pyperclip
from datetime import timedelta
from logger_categories.config import (
    ALL_CATEGORIES_TAG_COLUMNS,
    CATEGORIES_INPUT_FIELDS,
    TAG_CREATE_COLUMNS,
    CATEGORY_CREATE_COLUMNS,
    ALL_CATEGORIES_COLUMNS,
    ALL_CATEGORIES_TAG_COLUMNS,
)
from logger_categories.schema import CategoryTagItem, CategoryItem
from utils.dates import str_to_timdelta, time_str
from timelogger.api import *
from typing import Iterator
from timelogger.schema import LoggItem
from db.sql_templates import list_all, create
from utils.input import receive_item_input
from db.api import get_configuration_by_key

TABLE_C = "Logger_categories"
TABLE_T = "logger_categories_tags"
LIST_ALL_C = list_all(TABLE_C)
LIST_ALL_T = """
SELECT t.id, t.tag, c.name, c.customer, t.category_id
    FROM Logger_categories c JOIN logger_categories_tags t ON c.id = t.category_id;
"""


def all_tags(db: Connector) -> dict:
    qs = db.execute(LIST_ALL_T).fetchall()
    return CategoryTagItem.list_as_customer_dict(
        CategoryTagItem.parse_list(qs, ALL_CATEGORIES_TAG_COLUMNS)
    )


def all_categories(db: Connector) -> dict:
    qs = db.execute(LIST_ALL_C).fetchall()
    return CategoryItem.list_as_tagging_dict(
        CategoryItem.parse_list(qs, ALL_CATEGORIES_COLUMNS)
    )


def create_tag(db: Connector, new_item: CategoryTagItem) -> None:
    db.execute(
        create(TABLE_T, TAG_CREATE_COLUMNS, new_item.create_dict(TAG_CREATE_COLUMNS))
    )


def create_category(db: Connector, new_item: CategoryItem) -> int:
    new_id = db.execute(
        create(
            TABLE_C,
            CATEGORY_CREATE_COLUMNS,
            new_item.create_dict(CATEGORY_CREATE_COLUMNS),
        )
    ).lastrowid
    return new_id


def go_through_and_tag_rows(
    db: Connector, categories: dict, tags: dict, rows: Iterator[LoggItem]
) -> None:

    for row in rows:
        issue = row.get("issue", None)
        if issue and tags.get(issue, None) or row.get("customer") == "LUNCH":
            continue

        print_rows(row_str(row, True, tags))

        questions = [
            inquirer.List(
                "choice",
                message="Select tag or create new one?",
                choices=["create_new", "skip"] + [key for key in categories.keys()],
            ),
        ]
        answers = inquirer.prompt(questions)

        response = answers["choice"]
        if response != "create_new" and response != "skip":
            new_tag = CategoryTagItem(
                tag=row.get("issue"), category_id=categories.get(response)
            )
            create_tag(db, new_tag)
        elif response != "skip":
            # create category
            new_item = CategoryItem()
            receive_item_input(new_item, CATEGORIES_INPUT_FIELDS)
            new_id = create_category(db, new_item)
            new_item.set("id", new_id)

            categories[new_item.get("name")] = new_id

            # create tag
            new_tag = CategoryTagItem(tag=row.get("issue"), category_id=new_id)
        else:
            continue


## OUTPUTS


def sort_rows_into_days(rows_this_week: Iterator[LoggItem]) -> dict:
    sorted__rows_by_days = {}
    for row in rows_this_week:
        # Sort all entries into Calendar days with arrays of entries
        date = datetime.strptime(row.get("date_created"), "%Y-%m-%d %H:%M:%S")

        weekDay = calendar.day_name[date.weekday()]
        day_key = f"{weekDay[:3]} {date.day}"

        if not sorted__rows_by_days.get(day_key, None):
            sorted__rows_by_days[day_key] = [row]
        else:
            sorted__rows_by_days[day_key].append(row)

    return sorted__rows_by_days


def generate_export_data(rows_this_week: Iterator[LoggItem], tags: dict | None) -> None:
    export_settings = get_configuration_by_key("CUSTOMER_CONF")

    sorted_rows = sort_rows_into_days(rows_this_week)

    # Run calculations for each day
    caluclated = {}
    for day, day_entries in sorted_rows.items():

        day_started = str_to_timdelta(day_entries[0].get("start_time"))
        worked = timedelta()

        time_log_categories = {"LUNCH": timedelta()}
        for key in export_settings.keys():
            time_log_categories[key] = timedelta()

        for key, value in tags.items():
            if not value in time_log_categories.keys():
                time_log_categories[value] = timedelta()
    
        for row in day_entries:
            # Makes sure start is the smallest start_time entry
            if new_start := str_to_timdelta(row.get("start_time")) < day_started:
                day_started = new_start

            # Put time spent into resp category
            if time_spent := str_to_timdelta(row.get("spent", None)):
                worked += time_spent

                customer = row.get("customer")
                for category in time_log_categories:
                    if customer in export_settings.get(category, []):
                        time_log_categories[category] += time_spent
                    if customer == category:
                        time_log_categories[category] += time_spent
                
                if tag := tags.get(row.get("issue", "")):
                    time_log_categories[tag] += time_spent

        for category in time_log_categories:
            time_log_categories[category] = time_str(time_log_categories[category])
        caluclated[day] = {
            "START": time_str(day_started),
            "END": time_str(day_started + worked),
            **time_log_categories,
        }

    pyperclip.copy(str(caluclated).replace("'", '"'))
