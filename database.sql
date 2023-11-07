/*markdown
 # Database setup for DevContainer
 */




CREATE TABLE IF NOT EXISTS Articles (
    urlId varchar(200) Constraint primary_key Primary Key,
    headline varchar(200),
    contents text,
    authors varchar(200),
    uploadDate date,
    readTime int,
    imageURL varchar(200),
    imageDescription varchar(200),
    scrapingTimeStamp timestamp
);

-- Create Schema for tables of social media sources (Twitter, Instagram, etc.)
CREATE SCHEMA IF NOT EXISTS social_media;

-- Create Table for scraped Tweets
CREATE TABLE IF NOT EXISTS social_media.Tweets (
    id bigint NOT NULL UNIQUE Constraint primary_key Primary Key,
    id_str text,
    tweet_url text,
    publish_date timestamp,
    tweet_user text,
    lang text,
    rawContent text,
    replyCount numeric,
    retweetCount numeric,
    likeCount numeric,
    quoteCount numeric,
    conversationId text,
    hashtags text, -- list of hastags (interesting?)
    cashtags text,
    mentionedUsers text, -- list of users (interesting?)
    links text,
    viewCount numeric,
    retweetedTweet text,
    quotedTweet text,  -- ToDo: select id only??? tweet is probably not in our db anyways
    place text,
    coordinates text,
    inReplyToTweetId text,
    inReplyToUser text,
    source text,
    sourceUrl text,
    sourceLabel text,
    media text,
    _type text
);

-- Index on id for fast inserting or searching
CREATE UNIQUE INDEX IF NOT EXISTS idx_tweet_id
ON social_media.Tweets (id);
