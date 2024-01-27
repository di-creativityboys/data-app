from social_media_scraping.twitter.v2.extract import extract
from social_media_scraping.twitter.v2.load import load
from social_media_scraping.twitter.v2.transform import transform


async def twitter_etl(steps, user):
    print("[Twitter 2] Extracting...")
    extracted: dict = extract(steps=steps, user=user)
    print("[Twitter 2] Transforming...")
    transformed: dict = transform(tweets=extracted)
    print("[Twitter 2] Loading...")
    load(transformed_tweets=transformed)
    print("[Twitter 2] Scraping finished")
