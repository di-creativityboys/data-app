from datetime import datetime

import psycopg2
from database.database import Database


def load(transformed_articles):
    for article in transformed_articles.values():
        try:
            statement = """INSERT INTO Articles(URLId, Headline, Content, Authors, UploadTimestamp, ImageURL, ImageDescription,scrapingTimeStamp, source, topic) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s);"""
            values = (
                article["url"],
                article["headline"],
                article["contents"],
                article["authors"],
                article["date"],
                article["ImageURL"],
                article["ImageDescription"],
                article["scrapingTimeStamp"],
                article["source"],
                article["topics"],
            )
            database = Database()
            database.open_connection()
            database.execute(sqlStatement=statement, valuesTuple=values)
        except psycopg2.IntegrityError as e:
            if "duplicate key value violates unique constraint" in str(e):
                print(f"Article with URLId {article['url']} already exists in the database.")
