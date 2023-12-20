-- Create table for scraped news articles
CREATE TABLE IF NOT EXISTS Articles (
    urlId text PRIMARY KEY,
    headline text,
    content text,
    authors text[],
    uploadTimestamp timestamp, -- should be called instead
    imageURL text,
    imageDescription text,
    scrapingTimestamp timestamp NOT NULL,
    source text,
    topic text
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
    clusterId int,
    clusterTopic text
);

CREATE TABLE IF NOT EXISTS TweetsNew (
    rawContent text PRIMARY KEY,
    publishDatetime text,--should be timestamp later!!!
    tweetUser varchar,
    replyCount int,
    retweetCount int,
    likeCount int,
    profilImage text,
    scrapingTimeStamp timestamp NOT NULL
    
);