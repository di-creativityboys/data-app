
# ---------- IMPORTS ---------------

# import sys
# sys.path.insert(0,'/workspaces/data-app/app/database')

# basic imports
import psycopg2
import pandas as pd
import numpy as np
import pandas.io.sql as sqlio
from database.database import Database


# -------------- LOAD ----------------

def load_clusters_into_db(articles):
    # new database connection
    database = Database()
    database.open_connection()

    # write clusterIds and clusterTopics into database
    for index, row in articles.iterrows():
        try:
            database.execute(sqlStatement='''UPDATE articles
                                SET clusterId = %s, clusterTopic = %s
                                WHERE urlid = %s''',
                                valuesTuple=(row.clusterId,
                                 row.clusterTopic,
                                 row.urlid
                                )
                            )
        except BaseException as ex:
            print('Error: ', ex)
    database.close_connection()