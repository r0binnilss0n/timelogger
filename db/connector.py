import sqlite3
from sqlite3 import Connection
from typing import Any


class Connector:

    connector: Connection | None = None

    def __init__(self, database_path: str) -> None:
        self.connector = sqlite3.connect(database_path)

    def execute(self, sql: str) -> Any:
        cursor = self.connector.cursor()
        return cursor.execute(sql)

    def done(self, keep_alive: bool = False) -> None:
        self.save()
        if not keep_alive:
            self.close()

    def save(self) -> None:
        """
        Commits changes to database
        """
        self.connector.commit()

    def close(self) -> None:
        """
        Closes connection to db
        """
        self.connector.close()
