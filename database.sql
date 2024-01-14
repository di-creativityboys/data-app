-- Create table for scraped news articles
--drop table Articles;
CREATE TABLE IF NOT EXISTS Articles (
    id SERIAL PRIMARY KEY,
    urlId text,
    headline text,
    content text,
    authors text[],
    uploadTimestamp timestamp, -- should be called instead
    imageURL text,
    imageDescription text,
    scrapingTimestamp timestamp NOT NULL,
    source text,
    topic text,
    clusterId int,
    clusterTopic text
);

-- Create Table for scraped Tweets
CREATE TABLE IF NOT EXISTS Tweets (
    id SERIAL PRIMARY KEY,
    tweetUrl varchar,
    publishDatetime timestamp,
    tweetUser varchar,
    languageCode varchar,
    rawContent text,
    replyCount int,
    retweetCount int,
    likeCount int,
    quoteCount int,
    hashtags varchar [],
    -- list of hastags (interesting?)
    cashtags varchar [],
    -- hashtag with $
    mentionedUsers varchar [],
    -- list of users (interesting?)
    linksInTweet varchar [],
    viewCount int,
    retweetedTweetId text,
    quotedTweetId text,
    -- ToDo: select id only??? tweet is probably not in our db anyways
    -- place varchar,
    -- coordinates varchar,
    -- inReplyToTweetId varchar,
    inReplyToUser varchar,
    photoLinks varchar [],
    videoLinks varchar [],
    animatedLinks varchar [],
    scrapingTimeStamp timestamp NOT NULL,
    profileImageUrl varchar,
    clusterId int,
    clusterTopic text
);

CREATE TABLE IF NOT EXISTS PromptTemplate (
    id SERIAL PRIMARY KEY,
    name varchar,
    text0 varchar,
    text1 varchar,
    text2 varchar
)