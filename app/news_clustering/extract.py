# ------------- IMPORT --------------------

# # ensure path for database module works
# import sys
# sys.path.insert(0,'/workspaces/data-app/app/database')

# basic imports
import pandas.io.sql as sqlio
from database.database import Database


# -------------- EXTRACT -----------------


def extract_articles():
    # open database connection
    db = Database()
    db.open_connection()

    # get articles table into datframe
    sql = "SELECT * FROM articles;"
    articles = sqlio.read_sql_query(sql, db.connection)  # type: ignore
    db.close_connection()

    return articles
