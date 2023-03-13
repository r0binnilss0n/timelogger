#!/usr/bin/env python3.10
import pathlib
from pydoc import describe
import click
from timelogger.api import *
from logger_categories.api import all_categories
from utils.input import receive_item_input
from db.connector import Connector
from db.config import DB_TABLE_SETUP_SQL
from timelogger.config import INPUT_FIELDS
from logger_categories.api import (
    generate_export_data,
    go_through_and_tag_rows,
    all_tags,
)
from db.api import (
    run_new_setup,
    run_update_setup,
    SETUP_KEYS,
    reset_settings,
    read_conf_to_dict,
    get_configuration_by_key,
)


DEFAULT_PATH = str(pathlib.Path(__file__).parent.resolve()) + "/db/database.json"


@click.group()
def cli():
    pass


def setup_db_connection(is_setup: bool = False):
    if not bool(get_configuration_by_key("HAS_RUN_CONF")) and not is_setup:
        raise click.ClickException("You'll have to run logger config before continuing")
    # Add load config file
    db_path = get_configuration_by_key("DATABASE_FILE_LOCATION")
    return Connector(DEFAULT_PATH if not db_path != "" else db_path)


def close_db_connection(db: Connector):
    db.save()
    db.close()


@click.command(help="Time logger, log/display/export your time")
def create():
    db = setup_db_connection()
    # Prevents creation of new log entry before finished previous row
    if not handle_log_entries_missing_end_time(db):
        # Creating new log entry
        last_entry = get_previous_entry_for_log_date(db)
        new_item = LoggItem()
        if last_entry.get("end_time"):
            new_item.set("start_time", last_entry.end_time)
        receive_item_input(new_item, INPUT_FIELDS)
        create_new_item(db, new_item)
    close_db_connection(db)


@click.command(help="Update a log entry with given id")
@click.argument("identifier", required=True)
def update(identifier):
    db = setup_db_connection()
    item = get_log_item(db, identifier, True)
    print_rows(row_str(item, True), "LOGGER -> EDITING")
    receive_item_input(item, INPUT_FIELDS)
    if len(item.update_list) > 0:
        updated_item = update_item(db, item.id, item.update_list)
        print_rows(row_str(updated_item), "LOGGER -> UPDATED")
    close_db_connection(db)


@click.command(help="Remove log entry with given Id")
@click.argument("identifier", required=True)
def remove(identifier: str | None):
    db = setup_db_connection()
    removed_item = remove_log_item(db, identifier)
    print_rows(row_str(removed_item), "LOGGER -> REMOVED")
    close_db_connection(db)


@click.command(help="List all log entries with timestamp today")
@click.argument("date_string", required=False)
def list_day(date_string):
    db = setup_db_connection()
    tags = all_tags(db)
    print_rows(item_str(get_log_item_for_date(db, date_string), tags), "LOG -> LIST")
    close_db_connection(db)


@click.command(help="List all log entries by day for each weekday Mon-Sun")
@click.argument("week_string", required=False)
def list_week(week_string: str | None = ""):
    db = setup_db_connection()
    tags = all_tags(db)
    print_rows(week__str(get_log_item_for_week(db, week_string), tags))
    close_db_connection(db)


@click.command(help="Export day/week of log entries to json format")
@click.argument("week_string", required=False)
def export(week_string: str | None):
    db = setup_db_connection()
    rows_to_export = get_log_item_for_week(db, week_string)
    tags = all_tags(db)
    generate_export_data(rows_to_export, tags)
    close_db_connection(db)


@click.command(help="Tag log entries for special export time groups")
@click.argument("week_string", required=False)
def set_tags(week_string: str | None):
    db = setup_db_connection()
    categories = all_categories(db)
    available_tags = all_tags(db)
    rows_to_tag = get_log_item_for_week(db, week_string)
    go_through_and_tag_rows(db, categories, available_tags, rows_to_tag)

    close_db_connection(db)


@click.command(
    help=f"Configure the application settings, can run with config specific key as argument {SETUP_KEYS}"
)
@click.argument("update", required=False)
def config(update: str | None):
    print(update)
    # Makes sure the database it initialized
    db = setup_db_connection(is_setup=True)
    for item in DB_TABLE_SETUP_SQL:
        db.execute(item)
    close_db_connection(db)

    if not update:
        run_new_setup()
    else:
        run_update_setup(update)


@click.command(help="Resets application settings and db")
def reset_conf():
    reset_settings()


@click.command(help="prints current configuration")
def display_conf():
    print(read_conf_to_dict())


cli.add_command(create)
cli.add_command(list_day, "list")
cli.add_command(list_week, "list_week")
cli.add_command(update)
cli.add_command(remove)
cli.add_command(export)
cli.add_command(set_tags, "set_tags")
cli.add_command(config)
cli.add_command(reset_conf, "reset")
cli.add_command(display_conf, "display_conf")

if __name__ == "__main__":
    cli()
