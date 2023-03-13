from dataclasses import dataclass
from typing import Any


@dataclass
class CategoryItem:
    name: str = ""
    customer: str = ""
    id: int | None = None

    is_update: bool = False
    update_list: dict = None

    def get(self, key: str, default: Any | None = None):
        return getattr(self, key, default)

    def set(self, key: str, value: str) -> None:
        setattr(self, key, self.validate(key, value))

    def validate(self, key: str, value: str):
        match key:
            case "customer":
                value = self.validate_customer(value)
            case _:
                value = value
        if self.is_update:
            self.update_list[key] = value
        return value

    def validate_customer(self, value: str) -> str:
        return value.upper()

    def get_as_sql_values(self):
        return f"('{self.name}', '{self.customer}')"

    def parse(obj, order: list, update: bool = False):
        if not obj:
            return CategoryItem()
        row = {}
        if update:
            row["is_update"] = True
            row["update_list"] = {}
        for index in range(len(order)):
            row[order[index]] = obj[index] if not obj[index] == "None" else None

        return CategoryItem(**row)

    def parse_list(args: list, order: list):
        retval: list[CategoryItem] = []
        for obj in args:
            retval.append(CategoryItem.parse(obj, order))
        return retval

    def create_dict(self, columns: list[str]):
        data = {}
        for key in columns:
            data[key] = self.get(key)
        return data

    def list_as_tagging_dict(all_tags: list):
        rows = {}
        for item in all_tags:
            rows[f"{item.get('customer')}-{item.get('name')}"] = item.get("id")
        return rows


@dataclass
class CategoryTagItem:
    tag: str = ""
    category_id: int | None = None
    name: str = ""
    customer: str = ""
    id: int | None = None

    is_update: bool = False
    update_list: dict = None

    def get(self, key: str, default: Any | None = None):
        return getattr(self, key, default)

    def set(self, key: str, value: str) -> None:
        setattr(self, key, self.validate(key, value))

    def validate(self, key: str, value: str):
        match key:
            case _:
                value = value
        if self.is_update:
            self.update_list[key] = value
        return value

    def get_as_sql_values(self):
        return f"('{self.tag}', '{int(self.category_id)}')"

    def parse(obj, order: list, update: bool = False):
        if not obj:
            return CategoryTagItem()
        row = {}
        if update:
            row["is_update"] = True
            row["update_list"] = {}
        for index in range(len(order)):
            row[order[index]] = obj[index] if not obj[index] == "None" else None

        return CategoryTagItem(**row)

    def create_dict(self, columns: list[str]):
        data = {}
        for key in columns:
            data[key] = self.get(key)
        return data

    def parse_list(args: list, order: list):
        retval: list[CategoryTagItem] = []
        for obj in args:
            retval.append(CategoryTagItem.parse(obj, order))
        return retval

    def list_as_customer_dict(all_tags: list):
        rows = {}
        for item in all_tags:
            rows[item.get("tag")] = f"{item.get('customer')}-{item.get('name')}"
        return rows
