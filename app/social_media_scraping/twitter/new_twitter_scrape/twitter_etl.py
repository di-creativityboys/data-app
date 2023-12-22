from social_media_scraping.twitter.new_twitter_scrape.extract import extract
from social_media_scraping.twitter.new_twitter_scrape.load import load
from social_media_scraping.twitter.new_twitter_scrape.transform import transform


async def twitter_etl(steps, user):
    extracted: dict = extract(steps=steps, user=user)
    transformed: dict = transform(tweets=extracted)
    load(transformed_tweets=transformed)
