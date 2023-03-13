## Helpers
def convert_dict_to_sql_setters(data: dict) -> str:
    as_sql_setters = ""
    for key, value in data.items():
        as_sql_setters += f"{key} = '{value}'"
        if key != list(data.keys())[-1]:
            as_sql_setters += ","

    return as_sql_setters


def convert_dict_to_sql_values(data: dict, create_fields: list[str] = None) -> str:
    as_sql_values = "("
    last_entry = list(data.keys())[-1]
    for key, value in data.items():
        if not create_fields or (create_fields and key in create_fields):
            as_sql_values += f"'{value}'" + (")" if key == last_entry else ",")
        else:
            pass

    return as_sql_values


def conver_columns_list_to_sql_columns(columns: list[str]) -> str:
    as_sql_columns = "("
    last_column = columns[-1]
    for column in columns:
        as_sql_columns += f"{column}" + (")" if column == last_column else ",")

    return as_sql_columns


# ---------------------------------------------


def list_all(table: str) -> str:
    return f"SELECT * FROM {table}"


def list_columns(table: str, columns: list[str]) -> str:
    formatted_columns: str = str(tuple(columns)).replace("'", "")[1:-1]
    return f"SELECT {formatted_columns} FROM {table}"


def retrieve(list_sql: str, identifier: str, pk_name: str = "id") -> str:
    return list_sql + f" WHERE {pk_name} = '{identifier}'"


def retrieve_with_rule(list_sql: str, field: str, value: str) -> str:
    return list_sql + f" WHERE {field} = {value}"


def retrieve_with_between(list_sql: str, field: str, start: str, end: str) -> str:
    return list_sql + f" WHERE {field} BETWEEN '{start}' AND '{end}'"


def update(table: str, identifier: str, data: dict, pk_name: str = "id") -> str:
    sql_setters = convert_dict_to_sql_setters(data)
    return f"UPDATE {table} SET {sql_setters} WHERE {pk_name} = '{identifier}'"


def delete(table: str, identifier: str, pk_name: str = "id") -> str:
    return f"DELETE FROM {table} WHERE {pk_name} = '{identifier}'"


def create(table: str, columns: list[str], values: dict) -> str:
    sql_values = convert_dict_to_sql_values(values, columns)
    sql_columns = conver_columns_list_to_sql_columns(columns)

    return f"INSERT INTO {table}{sql_columns} VALUES {sql_values}"
