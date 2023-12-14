import psycopg2
import os

DATABASE_PORT = os.environ.get("DATABASE_PORT", "5432")
DATABASE_HOST = os.environ.get("DATABASE_HOST", "localhost")


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

    def execute(self, sqlStatement: str, valuesTuple: tuple):
        self.cursor.execute(sqlStatement, valuesTuple)

    def close_connection(self):
        self.connection.close()

    def initialize_schema(self):
        schema = open("./database.sql", "r").read()

        self.execute(schema, ())
