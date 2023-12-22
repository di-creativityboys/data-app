import psycopg2
from database.database import Database


def load(transformed_tweets):
    for tweet in transformed_tweets.values():
        try:
            statement = """INSERT INTO TweetsNew(rawContent, publishDatetime, tweetUser, replyCount, retweetCount, likeCount, profilImage,scrapingTimeStamp) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s,%s);"""
            values = (
                tweet["content"],
                tweet["date"],
                tweet["user"],
                tweet["comment"],
                tweet["share"],
                tweet["likes"],
                tweet["image"],
                tweet["scrapingTimeStamp"],
            )
            database = Database()
            database.open_connection()
            database.execute(statement, values)
        except psycopg2.IntegrityError as e:
            if "duplicate key value violates unique constraint" in str(e):
                print("Tweet already exists in the database.")
