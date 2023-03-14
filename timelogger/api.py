from datetime import timedelta, datetime
import calendar
from db.connector import Connector
from timelogger.schema import LoggItem
from utils.dates import parse_date_string, str_to_timdelta, parse_week_string
from utils.output import print_rows
from utils.input import receive_item_input, INPUT_FIELD_TYPES
from db.sql_templates import (
    list_all,
    retrieve,
    retrieve_with_rule,
    update,
    create,
    delete,
    retrieve_with_between,
)
from timelogger.config import (
    BASIC_ROW_STR,
    CREATE_COLUMNS,
    BASIC_COLUMNS,
    BASIC_HEADER_STR,
    BASIC_LINE_FORMAT,
    ALL_COLUMNS,
)
from typing import Iterator

TABLE = "Logger"
LIST_ALL = list_all(TABLE)


def handle_log_entries_missing_end_time(db: Connector) -> bool:
    qs = db.execute(retrieve_with_rule(LIST_ALL, "end_time", "''")).fetchall()

    faulty = LoggItem.parse_list(qs, BASIC_COLUMNS)
    if len(faulty) > 0:
        item = faulty[0]
        print_rows(row_str(item), "LOGGER -> SET END TIME")

        receive_item_input(item, {"end_time": INPUT_FIELD_TYPES.DEFAULT})
        data = {"end_time": item.get("end_time"), "spent": item.get("spent")}
        db.execute(update(TABLE, item.id, data))
        return True
    return False


def get_previous_entry_for_log_date(db: Connector) -> LoggItem:
    qs = db.execute(
        retrieve_with_rule(LIST_ALL, "date(date_created)", "date('now')")
        + "ORDER BY date_created DESC"
    ).fetchone()
    return LoggItem.parse(qs, BASIC_COLUMNS)


def create_new_item(db: Connector, new_item: LoggItem) -> None:
    db.execute(create(TABLE, CREATE_COLUMNS, new_item.create_dict(CREATE_COLUMNS)))


def update_item(db: Connector, identifier: str, updates: dict) -> LoggItem:
    db.execute(update(TABLE, identifier, updates)).fetchone()
    return get_log_item(db, identifier)


def remove_log_item(db: Connector, identifier: str) -> LoggItem:
    item_to_remove = get_log_item(db, identifier)
    db.execute(delete(TABLE, identifier))
    return item_to_remove


def get_log_item(db: Connector, identifier: str, is_update: bool = False) -> LoggItem:
    qs = db.execute(retrieve(LIST_ALL, identifier)).fetchone()

    return LoggItem.parse(qs, BASIC_COLUMNS, is_update)


def get_log_item_for_date(db: Connector, date_string: str) -> Iterator[LoggItem]:
    formatted_date = parse_date_string(date_string)
    qs = db.execute(
        retrieve_with_rule(LIST_ALL, "date(date_created)", f"date('{formatted_date}')") + " ORDER BY date_created"
    ).fetchall()
    return LoggItem.parse_list(qs, BASIC_COLUMNS)


def get_log_item_for_week(db: Connector, week_string: str) -> Iterator[LoggItem]:
    start = parse_week_string(week_string)
    end = start + timedelta(days=6)

    qs = db.execute(
        retrieve_with_between(LIST_ALL, "date(date_created)", start, end)  + " ORDER BY date_created"
    ).fetchall()
    return LoggItem.parse_list(qs, ALL_COLUMNS)


## OUTPUTS
def week__str(rows_this_week: Iterator[LoggItem], tags: dict | None) -> Iterator[str]:
    retval = []
    day_str = {}
    for row in rows_this_week:
        current_day = str(
            datetime.strptime(row.get("date_created"), "%Y-%m-%d %H:%M:%S").day
        )
        if not day_str.get(current_day, None):
            day_str[current_day] = [row]
        else:
            day_str[current_day].append(row)

    for key in day_str.keys():
        rows = day_str[key]

        date = datetime.strptime(rows[0].get("date_created"), "%Y-%m-%d %H:%M:%S")

        weekDay = calendar.day_name[date.weekday()]
        day_header = f"########## {weekDay} >> {key}  ##########"
        retval.append(day_header)
        rows_str = item_str(rows, tags) + ["\n"]
        retval += rows_str

    def _time_str(time: str):
        hours = str(time / 3600).split(".")[0]
        minutes = str((time // 60) % 60).split(".")[0]
        return f"{('0' if len(hours) < 2 else '') + hours}:{('0' if len(minutes) < 2 else '') + minutes}"

    week_to_work = timedelta(hours=40)
    week_worked = timedelta()
    for row in rows_this_week:
        if row.get("spent") and row.get("customer") != "LUNCH":
            week_worked += str_to_timdelta(row.get("spent"))
    extra = (
        "overtime"
        if (week_worked.total_seconds() > week_to_work.total_seconds())
        else "remaining"
    )
    extra_time = _time_str(abs((week_to_work - week_worked)).total_seconds())
    week_footer = [
        f"___________ {_time_str(week_worked.total_seconds())}/{_time_str(week_to_work.total_seconds())} >>>>>>>> {extra}: {extra_time} ______________"
    ]
    retval += week_footer
    return retval


def __line__(row, tags: dict | None = None) -> str:
    row_data = {}
    tag_options = {} if not tags else tags
    for column in BASIC_COLUMNS:
        row_data[column] = row.get(
            column if not column == "" or not column == None else "EMPTY", "EMPTY"
        )

    tag = "EMPTY"
    issue = row.get("issue", None)
    if issue:
        if custom_tag := tag_options.get(issue, None):
            tag = custom_tag

    row_data["tag"] = tag
    line_str = BASIC_LINE_FORMAT % tuple(BASIC_ROW_STR.format(**row_data).split("@"))
    return line_str


def row_str(row, divider: bool = False, tags: dict | None = None) -> Iterator[str]:
    retval = [BASIC_HEADER_STR]
    retval.append(__line__(row, tags))
    if divider:
        retval.append("-" * 64)
    return retval


def item_str(rows, tags: dict | None) -> Iterator[str]:
    def _time_str_(time: str):
        return str(time)[0:-3]

    retval = [BASIC_HEADER_STR]

    to_work = timedelta(hours=8)
    worked = timedelta()

    for row in rows:
        row_str = __line__(row, tags)

        if row.get("spent") and row.get("customer") != "LUNCH":
            worked += str_to_timdelta(row.get("spent"))
        retval.append(row_str)

    extra = "overtime" if (worked.seconds) > (to_work.seconds) else "remaining"
    extra_time = _time_str_(abs((to_work - worked)))
    footer = f"######## worked {_time_str_(worked)}/{_time_str_(to_work)} >>>>> {extra}: {extra_time} ########"
    retval.append(footer)
    return retval
