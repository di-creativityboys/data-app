from .scrape_twitter import *
import pandas as pd
import psycopg2


async def scrape_and_load_db(user_name, limit):
    ##input username and amount of tweets requested
    ##user_name = input("Input the username: ")
    ##limit = int(input("Input the amount of tweets to get: "))
    ## scrape
    result = await gettweets(user_name, limit)

    ## prepare to load in db
    df_tweets = pd.DataFrame(result)
    df_tweets.rename(columns={'url': 'tweet_url', 'date': 'publish_date','user': 'tweet_user'}, inplace=True)

    ## create db connection
    conn = psycopg2.connect(dbname="postgres",user="postgres", password="postgres", port="5432", host="localhost")
    conn.autocommit = True
    cursor = conn.cursor()

    ## insert into database
    for index, row in df_tweets.iterrows():
        try:
            cursor.execute('''INSERT INTO social_media.Tweets (
                                id,
                                id_str,
                                tweet_url,
                                publish_date,
                                tweet_user,
                                lang,
                                rawcontent,
                                replycount,
                                retweetcount,
                                likecount,
                                quotecount,
                                conversationid,
                                hashtags,
                                cashtags,
                                mentionedusers,
                                links,
                                viewcount,
                                retweetedtweet,
                                quotedtweet,
                                place,
                                coordinates,
                                inreplytotweetid,
                                inreplytouser,
                                source,
                                sourceurl,
                                sourcelabel,
                                media,
                                _type
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);''', 
                           (row.id,
                            row.id_str,
                            row.tweet_url,
                            row.publish_date,
                            str(row.tweet_user),
                            row.lang,
                            row.rawContent,
                            row.replyCount,
                            row.retweetCount,
                            row.likeCount,
                            row.quoteCount,
                            row.conversationId,
                            str(row.hashtags),
                            str(row.cashtags),
                            str(row.mentionedUsers),
                            str(row.links),
                            row.viewCount,
                            str(row.retweetedTweet),
                            str(row.quotedTweet),
                            str(row.place),
                            str(row.coordinates),
                            str(row.inReplyToTweetId),
                            str(row.inReplyToUser),
                            str(row.source),
                            str(row.sourceUrl),
                            str(row.sourceLabel),
                            str(row.media),
                            str(row._type)
                           )
            )
        
        except psycopg2.errors.UniqueViolation:
            print('Tweet already in database. Tweet ID: ', row.id)
        except BaseException as ex:
            print('Differen Error: ', ex)


## ToDo extract only username from tweet_user!!!!!