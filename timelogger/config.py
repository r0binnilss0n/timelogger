from typing import Final
from utils.input import INPUT_FIELD_TYPES

LOG_TABLE: Final[str] = "Logger"

ALL_COLUMNS = [
    "id",
    "customer",
    "issue",
    "start_time",
    "end_time",
    "spent",
    "date_created",
    "date_updated",
]
BASIC_COLUMNS = ["id", "customer", "issue", "start_time", "end_time", "spent"]
CREATE_COLUMNS = [
    "customer",
    "issue",
    "start_time",
    "end_time",
    "spent",
    "date_updated",
]

BASIC_HEADER_STR = "%-5s %-50s %-10s %-10s %-10s %-10s" % (
    "ID",
    "TASK",
    "START",
    "END",
    "SPENT",
    "TAG",
)
BASIC_ROW_STR = "{id}@{customer}-{issue}@{start_time}@{end_time}@{spent}@{tag}"
BASIC_LINE_FORMAT = "%-5s %-50s %-10s %-10s %-10s %-10s"


DETAIL_HEADER_STR = "%-5s %-40s %-10s %-10s %-10s %-20s %-15s" % (
    "ID",
    "TASK",
    "START",
    "END",
    "SPENT",
    "CREATED",
    "UPDATED",
)
DETAIL_ROW_STR = "{id}@{customer}-{issue}@{start_time}@{end_time}@{spent}@{date_created}@{date_updated}"
DETAIL_LINE_FORMAT = "%-5s %-40s %-10s %-10s %-10s %-20s %-15s"

INPUT_FIELDS = {
    "customer": INPUT_FIELD_TYPES.DEFAULT,
    "issue": INPUT_FIELD_TYPES.DEFAULT,
    "start_time": INPUT_FIELD_TYPES.DEFAULT,
    "end_time": INPUT_FIELD_TYPES.DEFAULT,
}
