from social_media_scraping.twitter.extract import extract
from social_media_scraping.twitter.transform import transform
from social_media_scraping.twitter.load import load


async def twitter_etl(username, limit):
    extracted = await extract(username, limit)
    transformed = transform(extracted)
    load(transformed)
