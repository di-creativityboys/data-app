-- Create table for scraped news articles
CREATE TABLE IF NOT EXISTS Articles (
    urlId text NOT NULL PRIMARY KEY,
    headline text,
    contents text,
    authors text,
    uploadDate text,
    readTime int,
    imageURL text,
    imageDescription text,
    scrapingTimeStamp text
);

DROP TABLE tweets;

-- Create Table for scraped Tweets
CREATE TABLE IF NOT EXISTS Tweets (
    id bigint NOT NULL PRIMARY KEY,
    id_str varchar,
    tweet_url varchar,
    publish_date timestamp,
    tweet_user varchar,
    lang varchar,
    rawContent varchar,
    replyCount int,
    retweetCount int,
    likeCount int,
    quoteCount int,
    conversationId varchar,
    hashtags varchar[], -- list of hastags (interesting?)
    cashtags varchar[],
    mentionedUsers varchar[], -- list of users (interesting?)
    links varchar,
    viewCount float,
    retweetedTweet varchar,
    quotedTweet varchar,  -- ToDo: select id only??? tweet is probably not in our db anyways
    place varchar,
    coordinates varchar,
    inReplyToTweetId varchar,
    inReplyToUser varchar,
    source varchar,
    sourceUrl varchar,
    sourceLabel varchar,
    media varchar,
    _type varchar
);

-- Index on id for fast inserting or searching
CREATE UNIQUE INDEX IF NOT EXISTS idx_tweet_id
ON Tweets (id);
