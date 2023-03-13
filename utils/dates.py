from datetime import date, timedelta, datetime
from enum import Enum
import re

FORMATS = ["%d/%m/%Y", "%H:%M:%S"]


class DateFormat(Enum):
    DEFAULT = 0
    TIME = 1


def parse_date_string(date_string: str) -> datetime.date:
    formats = [
        "%Y/%m/%d",
        "%Y:%m:%d",
        "%Y%m%d",
        "%m/%d",
        "%m:%d",
        "%m%d",
        "%d",
        "%d",
        "%d",
    ]
    if not date_string:
        date_string = ""
    today = datetime.today()
    year = month = day = 0

    # Try parsing the date string using each format
    # for fmt in formats:
    #     try:
    #         parsed_date = datetime.strptime(date_string, fmt)
    #     except ValueError:
    #         pass

    if "/" in date_string:
        date_components = date_string.split("/")
    elif ":" in date_string:
        date_components = date_string.split(":")
    else:
        if len(date_string) <= 4:
            date_components = re.findall("..", date_string)
        else:
            year, other = date_string[:4], re.findall("..", date_string[4:])
            date_components = [year] + other

    if len(date_components) == 1:
        year, month, day = today.year, today.month, int(date_components[0])
    elif len(date_components) == 2:
        year = today.year
        month, day = map(int, date_components)
    elif len(date_components) == 3:
        year, month, day = map(int, date_components)
    else:
        return today.date()

    return datetime(year=year, month=month, day=day).date()


def parse_week_string(week_string: str) -> datetime.date:
    formats = ["%Y:%W-%w", "%Y/%W-%w", "%Y%W-%w", "%W-%w", "%Y-%W-%w"]
    today = datetime.today()
    parsed_date = None

    if week_string:
        # Try parsing the date string using each format
        for fmt in formats:
            try:
                # The -1 and -%w pattern tells the parser to pick the Monday in that week
                parsed_date = datetime.strptime(week_string + "-1", fmt)
            except ValueError:
                pass

    if not parsed_date:
        days_since_monday = today.weekday()
        most_recent_monday = today - timedelta(days=days_since_monday)
        return most_recent_monday.date()

    if len(week_string) <= 2:
        parsed_date = parsed_date.replace(year=today.year)

    return parsed_date.date()


def get_today(format: DateFormat = DateFormat.DEFAULT):
    return date.today().strftime(FORMATS[format.value])


def date_str(date: datetime, format: DateFormat = DateFormat.DEFAULT):
    return date.strftime(FORMATS[format.value])


def time_str(time: timedelta) -> str:
    time_total_seconds = time.total_seconds()
    hours = str(time_total_seconds / 3600).split(".")[0]
    minutes = str((time_total_seconds // 60) % 60).split(".")[0]
    return f"{('0' if len(hours) < 2 else '') + hours}:{('0' if len(minutes) < 2 else '') + minutes}"


def get_most_recent_monday(specific_date):
    today = date.today() if not specific_date else specific_date
    days_since_monday = today.weekday()
    most_recent_monday = today - timedelta(days=days_since_monday)
    return most_recent_monday


# Steps 6 = monday -> sunday
def create_array_of_week_dates(start: datetime, steps: int = 5):
    days = [date_str(start)]
    for index in range(6):
        next = start + timedelta(days=(index + 1))
        days.append(date_str(next))

    return days


def calc_time_diff(start: str | timedelta, end: str | timedelta) -> timedelta:
    format = DateFormat.TIME
    start_time_delta = start
    end_time_delta = end
    if isinstance(start, str):
        start_date = datetime.strptime(start, FORMATS[format.value])
        start_time_delta = timedelta(hours=start_date.hour, minutes=start_date.minute)
    if isinstance(end, str):
        end_date = datetime.strptime(end, FORMATS[format.value])
        end_time_delta = timedelta(hours=end_date.hour, minutes=end_date.minute)

    return end_time_delta - start_time_delta


def str_to_timdelta(time_str) -> timedelta:
    if not time_str:
        return None
    format = DateFormat.TIME
    extra = ":00" if len(time_str) <= 5 else ""
    value = time_str + extra
    start_date = datetime.strptime(value, FORMATS[format.value])
    return timedelta(hours=start_date.hour, minutes=start_date.minute)
