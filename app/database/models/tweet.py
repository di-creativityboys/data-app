import pandas as pd


class Tweet:
    def __init__(
        self,
        id: int,
        tweet_url: str | None,
        publish_datetime: pd.Timestamp | None,
        tweet_user: str | None,
        language_code: str | None,
        raw_content: str | None,
        reply_count: int | None,
        retweet_count: int | None,
        like_count: int | None,
        quote_count: int | None,
        hashtags: list[str] | None,
        cashtags: list[str] | None,
        mentioned_users: list[str] | None,
        links_in_tweet: list[str] | None,
        view_count: int | None,
        retweeted_tweet_id: str | None,
        quoted_tweet_id: str | None,
        in_reply_to_user: str | None,
        photo_links: list[str] | None,
        video_links: list[str] | None,
        animated_links: list[str] | None,
        scraping_timestamp: pd.Timestamp,
        cluster_id: int | None,
        cluster_topic: str | None,
    ):
        self.id: int = id
        self.tweet_url: str | None = tweet_url
        self.publish_datetime: pd.Timestamp | None = publish_datetime
        self.tweet_user: str | None = tweet_user
        self.language_code: str | None = language_code
        self.raw_content: str | None = raw_content
        self.reply_count: int | None = reply_count
        self.retweet_count: int | None = retweet_count
        self.like_count: int | None = like_count
        self.quote_count: int | None = quote_count
        self.hashtags: list[str] | None = hashtags
        self.cashtags: list[str] | None = cashtags
        self.mentioned_users: list[str] | None = mentioned_users
        self.links_in_tweet: list[str] | None = links_in_tweet
        self.view_count: int | None = view_count
        self.retweeted_tweet_id: str | None = retweeted_tweet_id
        self.quoted_tweet_id: str | None = quoted_tweet_id
        self.in_reply_to_user: str | None = in_reply_to_user
        self.photo_links: list[str] | None = photo_links
        self.video_links: list[str] | None = video_links
        self.animated_links: list[str] | None = animated_links
        self.scraping_timestamp: pd.Timestamp = scraping_timestamp
        self.cluster_id: int | None = cluster_id
        self.cluster_topic: str | None = cluster_topic

    def __str__(self):
        return f"{self.raw_content}"
