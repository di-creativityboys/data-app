# ------------- IMPORT --------------------

# ensure path for database module works
import sys
sys.path.insert(0,'/workspaces/data-app/app/database')

# basic imports
import psycopg2
import pandas as pd
import numpy as np
import pandas.io.sql as sqlio
from database import Database # type: ignore


# -------------- EXTRACT -----------------

def extract_articles():
    # open database connection
    database = Database()
    database.open_connection()

    # get articles table into datframe
    sql = "SELECT * FROM articles;"
    articles = sqlio.read_sql_query(sql, database.connection)
    database.close_connection()

    return articles