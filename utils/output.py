from typing import Iterator


def print_rows(print_rows: Iterator[str] | str, table_name: str | None = None) -> None:
    if table_name:
        print(f"########## {table_name.upper()} ##########")

    if not isinstance(print_rows, list):
        print(print_rows)
    else:
        for row in print_rows:
            print(row)
