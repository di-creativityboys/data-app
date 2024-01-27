import psycopg2
import os

DATABASE_PORT: str = os.environ.get("DATABASE_PORT", "5432")
DATABASE_HOST: str = os.environ.get("DATABASE_HOST", "localhost")


class Database:
    def open_connection(self):
        self.connection = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            port=DATABASE_PORT,
            host=DATABASE_HOST,
        )

        # Then you dont need to commit by yourself
        self.connection.autocommit = True

        self.cursor = self.connection.cursor()

    def execute(self, sqlStatement: str, valuesTuple: tuple) -> None:
        self.cursor.execute(query=sqlStatement, vars=valuesTuple)

    def close_connection(self) -> None:
        self.connection.close()

    def initialize_schema(self) -> None:
        schema: str = open(file="./database.sql", mode="r").read()

        self.execute(sqlStatement=schema, valuesTuple=())
