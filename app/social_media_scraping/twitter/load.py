import pandas as pd
from database.database import Database
import psycopg2


def load(transformed: pd.DataFrame):
    # create db connection
    database = Database()
    database.open_connection()

    # insert tweets of user into database
    insert_into_database(transformed, database)

    # close db connection
    database.close_connection()


def insert_into_database(df_tweets: pd.DataFrame, database: Database):
    for index, row in df_tweets.iterrows():
        try:
            database.execute(
                """INSERT INTO Tweets (
                                id,
                                tweetUrl,
                                publishDatetime,
                                tweetUser,
                                languageCode,
                                rawContent,
                                replyCount,
                                retweetCount,
                                likeCount,
                                quoteCount,
                                hashtags,
                                cashtags,
                                mentionedusers,
                                linksInTweet,
                                viewCount,
                                reTweetedTweetId,
                                quotedTweetId,
                                inReplyToUser,
                                photoLinks,
                                videoLinks,
                                animatedLinks,
                                scrapingTimeStamp
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, NOW());""",
                (
                    row.id,
                    row.tweet_url,
                    row.publish_date,
                    row.tweet_user,
                    row.lang,
                    row.rawContent,
                    row.replyCount,
                    row.retweetCount,
                    row.likeCount,
                    row.quoteCount,
                    row.hashtags,
                    row.cashtags,
                    row.mentionedUsers,
                    row.links,
                    row.viewCount,
                    row.retweetedTweet,
                    row.quotedTweet,
                    row.inReplyToUser,
                    row.photoLinks,
                    row.videoLinks,
                    row.animatedLinks,
                ),
            )
        except psycopg2.errors.UniqueViolation:
            print("Tweet already in database. Tweet ID: ", row.id)
        except BaseException as ex:
            print("Different Error: ", ex)
