import psycopg2
from database.database import Database


def load(transformed_tweets):
    database = Database()
    database.open_connection()

    for tweet in transformed_tweets.values():
        try:
            statement = """INSERT INTO Tweets(rawContent, publishDatetime, tweetUser, replyCount, retweetCount, likeCount, profileImageUrl,scrapingTimeStamp) 
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

            database.execute(sqlStatement=statement, valuesTuple=values)
        except psycopg2.IntegrityError as e:
            if "duplicate key value violates unique constraint" in str(e):
                print("Tweet already exists in the database.")

    database.close_connection()
