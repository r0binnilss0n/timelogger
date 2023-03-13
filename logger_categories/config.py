from utils.input import INPUT_FIELD_TYPES

ALL_CATEGORIES_COLUMNS = ["id", "name", "customer"]
CATEGORY_CREATE_COLUMNS = ["name", "customer"]

ALL_CATEGORIES_TAG_COLUMNS = ["id", "tag", "name", "customer", "category_id"]
TAG_CREATE_COLUMNS = ["tag", "category_id"]


DETAIL_HEADER_STR = "%-5s %-20s %-20s" % ("ID", "NAME/TAG", "CUSTOMER")
DETAIL_ROW_STR = "{id}@{customer}@{name}"
DETAIL_LINE_FORMAT = "%-5s %-20s %-20s"


CATEGORIES_INPUT_FIELDS = {
    "name": INPUT_FIELD_TYPES.DEFAULT,
    "customer": INPUT_FIELD_TYPES.DEFAULT,
}

CATEGORIES_TAG_INPUT_FIELDS = {
    "tag": INPUT_FIELD_TYPES.DEFAULT,
    "customer": INPUT_FIELD_TYPES.DEFAULT,
}
