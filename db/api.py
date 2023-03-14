import shelve
import pathlib
from typing import Any
from db.config import DATABSE_FILE_LOCATION, CUSTOMER_CONF, HAS_RUN_CONF
from utils.output import print_rows

CONF_PATH = str(pathlib.Path(__file__).parent.resolve()) + "/user_configurations.dat"
AVAILABLE_KEYS = ["DATABASE_FILE_LOCATION", "CUSTOMER_CONF", "HAS_RUN_CONF"]
SETUP_KEYS = ["DATABASE_FILE_LOCATION", "CUSTOMER_CONF"]


def write_conf_to_file(conf: dict) -> None:
    with shelve.open(CONF_PATH) as shelf:
        for key, value in conf.items():
            shelf[key] = value


def read_conf_to_dict() -> Any:
    data = {}
    with shelve.open(CONF_PATH) as shelf:
        for key in AVAILABLE_KEYS:
            data[key] = shelf.get(key, "")
    return data


def get_configuration_by_key(key: str) -> Any:
    assert key in AVAILABLE_KEYS, "invalid key"
    with shelve.open(CONF_PATH) as shelf:
        key_value = shelf.get(key, "")
    return key_value


def reset_settings() -> None:
    with shelve.open(CONF_PATH) as shelf:
        shelf["DATABASE_FILE_LOCATION"] = DATABSE_FILE_LOCATION
        shelf["CUSTOMER_CONF"] = CUSTOMER_CONF
        shelf["HAS_RUN_CONF"] = HAS_RUN_CONF


def run_new_setup():
    new_settings = {}
    for key in AVAILABLE_KEYS:
        match key:
            case "DATABASE_FILE_LOCATION":
                database_path = ""
                print_rows(
                    [
                        "\n----------------------------------------------------------------------",
                        "Not required, but if you want to store the database file"
                        "outside the application you can enter the FULL path below + :"
                        "name of the database: eg. User/.../.../db.json",
                        "(leave empty to use default in db folder)",
                        "----------------------------------------------------------------------\n",
                    ]
                )
                database_path = input("Database-path: ")
                new_settings[key] = database_path
            case "CUSTOMER_CONF":
                print_rows(
                    [
                        "\n----------------------------------------------------------------------",
                        "This step is required for the system to be able to properly",
                        "export your logged time. For each category input comma seperated",
                        "list of 'customer-tags' ex. INT = internal, COMP = competence development...",
                        "----------------------------------------------------------------------\n",
                    ]
                )
                customer_confs = {}
                for key in CUSTOMER_CONF.keys():
                    customer_tags = ""
                    customer_tags = input(key + ": ")
                    customer_confs[key] = customer_tags.replace(" ", "").split(",")
                new_settings["CUSTOMER_CONF"] = customer_confs
            case "HAS_RUN_CONF":
                new_settings[key] = True
    write_conf_to_file(new_settings)


def run_update_setup(key_to_change: str) -> None:
    new_settings = {}
    current_value = get_configuration_by_key(key_to_change)
    match key_to_change:
        case "DATABASE_FILE_LOCATION":
            database_path = ""
            print_rows(
                [
                    "\n----------------------------------------------------------------------",
                    "Not required, but if you want to store the database file"
                    "outside the application you can enter the path below:"
                    "(leave empty to use default)",
                    "----------------------------------------------------------------------\n",
                ]
            )
            database_path = input(f"Database-path [{current_value}]: ")
            new_settings[key_to_change] = database_path
        case "CUSTOMER_CONF":
            print_rows(
                [
                    "\n----------------------------------------------------------------------",
                    "This step is required for the system to be able to properly",
                    "export your logged time. For each category input comma seperated",
                    "list of 'customer-tags' ex. INT = internal, COMP = competence development...",
                    "----------------------------------------------------------------------\n",
                ]
            )
            customer_confs = {}
            for key in CUSTOMER_CONF.keys():
                customer_tags = ""
                customer_tags = input(key + f"[{current_value[key]}]: ")
                if customer_tags != "":
                    customer_confs["test"] = customer_tags.replace(" ", "").split(",")
            new_settings[key_to_change] = customer_confs
    write_conf_to_file(new_settings)
