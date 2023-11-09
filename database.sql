-- Create table for scraped news articles
CREATE TABLE IF NOT EXISTS Articles (
    urlId text PRIMARY KEY,
    headline text,
    content text,
    authors text[],
    uploadDate timestamp,
    imageURL text,
    imageDescription text,
    scrapingTimeStamp timestamp NOT NULL
);
-- Create Table for scraped Tweets
CREATE TABLE IF NOT EXISTS Tweets (
    id bigint PRIMARY KEY,
    tweetUrl varchar,
    publishDatetime timestamp,
    tweetUser varchar,
    languageCode varchar,
    rawContent text,
    replyCount int,
    retweetCount int,
    likeCount int,
    quoteCount int,
    hashtags varchar[], -- list of hastags (interesting?)
    cashtags varchar[], -- hashtag with $
    mentionedUsers varchar[], -- list of users (interesting?)
    linksInTweet varchar[],
    viewCount int,
    retweetedTweetId bigint,
    quotedTweetId bigint,  -- ToDo: select id only??? tweet is probably not in our db anyways
    -- place varchar,
    -- coordinates varchar,
    -- inReplyToTweetId varchar,
    inReplyToUser varchar,
    photoLinks varchar[],
    videoLinks varchar[],
    animatedLinks varchar[],
    scrapingTimeStamp timestamp NOT NULL
);
