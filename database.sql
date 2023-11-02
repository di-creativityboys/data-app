/*markdown
 # Database setup for DevContainer
 */

CREATE TABLE IF NOT EXISTS Articles (
    URLId text Constraint primary_key Primary Key,
    Headline text,
    Contents text,
    Authors text,
    UploadDate text,
    ReadTime text,
    ImageURL text,
    ImageDescription text,
    ScrapingTimeStamp text
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
    replyCount int,
    retweetCount int,
    likeCount int,
    quoteCount int,
    conversationId bigint,
    hashtags text, -- list of hastags (interesting?)
    cashtags text,
    mentionedUsers text, -- list of users (interesting?)
    links text,
    viewCount int,
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
