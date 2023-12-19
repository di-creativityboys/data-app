import pandas as pd
import psycopg2
from social_media_scraping.twitter.scrape_twitter import gettweets
# import os
from database.database import Database

# DB_PORT = os.environ.get("DATABASE_PORT", "5432")
# DB_HOST = os.environ.get("DATABASE_HOST", "localhost")


def insert_into_database(df_tweets: pd.DataFrame, database: Database):

    df_tweets.rename(columns={'url': 'tweet_url', 'date': 'publish_date', 'user': 'tweet_user'}, inplace=True)

    for index, row in df_tweets.iterrows():
        try:
            database.execute('''INSERT INTO Tweets (
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
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, NOW());''',
                           (row.id,
                            row.tweet_url,
                            row.publish_date,
                            str(row.tweet_user['username']),
                            row.lang,
                            row.rawContent,
                            row.replyCount,
                            row.retweetCount,
                            row.likeCount,
                            row.quoteCount,
                            row.hashtags if str(
                                row.hashtags) != '[]' else None,
                            row.cashtags if str(
                                row.cashtags) != '[]' else None,
                            list(pd.DataFrame(row.mentionedUsers)['username']) if str(
                                row.mentionedUsers) != '[]' else None,
                            list(pd.DataFrame(row.links)['url']) if str(
                                row.links) != '[]' else None,
                            int(row.viewCount) if str(
                                row.viewCount) != 'nan' else None,
                            row.retweetedTweet['id'] if row.retweetedTweet != None else None,
                            row.quotedTweet['id'] if row.quotedTweet != None else None,
                            row.inReplyToUser['username'] if row.inReplyToUser != None else None,
                            list(pd.DataFrame(row.media['photos'])['url']) if str(
                                row.media['photos']) != '[]' else None,  # photoLinks
                            [pd.DataFrame(row.media['videos'])['variants'][0][0]['url']] if str(
                                row.media['videos']) != '[]' else None,  # videoLinks
                            list(pd.DataFrame(row.media['animated'])['thumbnailUrl']) if str(
                                row.media['animated']) != '[]' else None,  # animatedLinks
                            )
                           )
        except psycopg2.errors.UniqueViolation:
            print('Tweet already in database. Tweet ID: ', row.id)
        except BaseException as ex:
            print('Differen Error: ', ex)


async def scrape_twitter(user_name, limit):
    # parameters: twitter username and amount of tweets requested

    # scrape
    scraped_tweets = await gettweets(user_name, limit)

    # prepare to load in db
    df_tweets = pd.DataFrame(scraped_tweets)

    # create db connection
    database = Database()
    database.open_connection()


    # insert tweets of user into database
    insert_into_database(df_tweets, database)

    # insert retweeted tweets into database
    df_retweetedTweets = df_tweets['retweetedTweet'].dropna().to_list()
    df_retweeted = pd.DataFrame(df_retweetedTweets)
    insert_into_database(df_retweeted, database)

    # insert quoted tweets into database
    df_quotedTweets = df_tweets['quotedTweet'].dropna().to_list()
    df_quoted = pd.DataFrame(df_quotedTweets)
    insert_into_database(df_quoted, database)

    # close db connection
    database.close_connection()
