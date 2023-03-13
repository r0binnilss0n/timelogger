from dataclasses import dataclass
from datetime import timedelta, datetime
from utils.dates import calc_time_diff, str_to_timdelta
from typing import Any
from utils.validators import validate_time_field


@dataclass
class LoggItem:

    customer: str = ""
    issue: str = ""
    start_time: timedelta | None = None
    id: int | None = None
    end_time: timedelta | None = None
    spent: timedelta | None = None
    date_created: datetime | None = None
    date_updated: datetime | None = None

    is_update: bool = False
    update_list: dict = None

    def get(self, key: str, default: Any | None = None):
        return getattr(self, key, default)

    def set(self, key: str, value: str):
        setattr(self, key, self.validate(key, value))

    def validate(self, key: str, value: str):
        match key:
            case "customer":
                value = self.validate_customer(value)
            case "start_time":
                value = self.validate_start_time(value)
            case "end_time":
                value = self.validate_end_time(value)
            case _:
                value = value
        if self.is_update:
            self.update_list[key] = value
        return value

    def validate_customer(self, value: str) -> str:
        return value.upper()

    def validate_start_time(self, value: str) -> timedelta:
        return str_to_timdelta(validate_time_field(value))

    def validate_end_time(self, value: str) -> timedelta:
        if value:
            end_time = str_to_timdelta(validate_time_field(value))
            if not isinstance(self.start_time, timedelta):
                self.start_time = str_to_timdelta(self.start_time)
            assert (
                self.start_time < end_time if self.start_time else True
            ), "End time can't be before start"
            self.set("spent", calc_time_diff(self.start_time, end_time))
            return end_time
        return value

    def create_dict(self, columns: list[str]):
        calc_spent = self.start_time and self.end_time
        setattr(
            self,
            "spent",
            calc_time_diff(self.start_time, self.end_time) if calc_spent else None,
        )
        setattr(self, "date_updated", datetime.now())
        data = {}
        for key in columns:
            data[key] = self.get(key)
        return data

    def parse(obj, order: list, update: bool = False):
        if not obj:
            return LoggItem()
        row = {}
        if update:
            row["is_update"] = True
            row["update_list"] = {}
        for index in range(len(order)):
            row[order[index]] = obj[index] if not obj[index] == "None" else None

        return LoggItem(**row)

    def parse_list(args: list, order: list):
        retval: list[LoggItem] = []
        for obj in args:
            retval.append(LoggItem.parse(obj, order))
        return retval
