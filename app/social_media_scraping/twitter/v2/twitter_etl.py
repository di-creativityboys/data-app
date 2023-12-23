from social_media_scraping.twitter.v2.extract import extract
from social_media_scraping.twitter.v2.load import load
from social_media_scraping.twitter.v2.transform import transform


async def twitter_etl(steps, user):
    extracted: dict = extract(steps=steps, user=user)
    transformed: dict = transform(tweets=extracted)
    load(transformed_tweets=transformed)
