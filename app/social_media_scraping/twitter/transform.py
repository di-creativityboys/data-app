import pandas as pd


def transform(extracted) -> pd.DataFrame:
    # prepare to load in db
    df_tweets = pd.DataFrame(extracted)

    # extract retweeted tweets from column
    retweetedTweets = df_tweets["retweetedTweet"].dropna().to_list()
    df_retweeted = pd.DataFrame(retweetedTweets)

    # extract retweeted tweets from column
    quotedTweets = df_tweets["quotedTweet"].dropna().to_list()
    df_quoted = pd.DataFrame(quotedTweets)

    # append retweeted
    df_combined = pd.concat([df_tweets, df_retweeted, df_quoted])

    # rename columns to prevent sql keywords
    df_combined.rename(columns={"url": "tweet_url", "date": "publish_date", "user": "tweet_user"}, inplace=True)
    df_combined["photoLinks"] = None
    df_combined["videoLinks"] = None
    df_combined["animatedLinks"] = None

    df_combined["tweet_user"] = df_combined["tweet_user"].apply(lambda x: str(x["username"]))
    df_combined["hashtags"] = df_combined["hashtags"].apply(lambda x: x if str(x) != "[]" else None)
    df_combined["cashtags"] = df_combined["cashtags"].apply(lambda x: x if str(x) != "[]" else None)
    df_combined["mentionedUsers"] = df_combined["mentionedUsers"].apply(
        lambda x: list(pd.DataFrame(x)["username"]) if str(x) != "[]" else None
    )
    df_combined["links"] = df_combined["links"].apply(lambda x: list(pd.DataFrame(x)["url"]) if str(x) != "[]" else None)
    df_combined["viewCount"] = df_combined["viewCount"].apply(lambda x: int(x) if str(x) != "nan" else None)
    df_combined["retweetedTweet"] = df_combined["retweetedTweet"].apply(lambda x: x["id"] if x != None else None)
    df_combined["retweetedTweet"] = df_combined["retweetedTweet"].apply(lambda x: x if x != "NaN" else None)
    df_combined["quotedTweet"] = df_combined["quotedTweet"].apply(lambda x: x["id"] if x != None else None)
    df_combined["quotedTweet"] = df_combined["quotedTweet"].apply(lambda x: x if x != "NaN" else None)
    df_combined["inReplyToUser"] = df_combined["inReplyToUser"].apply(lambda x: x["username"] if x != None else None)
    df_combined["photoLinks"] = df_combined["media"].apply(
        lambda x: list(pd.DataFrame(x["photos"])["url"]) if str(x["photos"]) != "[]" else None
    )
    df_combined["videoLinks"] = df_combined["media"].apply(
        lambda x: [pd.DataFrame(x["videos"])["variants"][0][0]["url"]] if str(x["videos"]) != "[]" else None
    )
    df_combined["animatedLinks"] = df_combined["media"].apply(
        lambda x: list(pd.DataFrame(x["animated"])["thumbnailUrl"]) if str(x["animated"]) != "[]" else None
    )

    return df_combined
