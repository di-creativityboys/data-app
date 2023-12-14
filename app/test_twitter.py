import asyncio
from social_media_scraping.twitter.load_tweets_db import scrape_twitter
from social_media_scraping.twitter.twitter_etl import twitter_etl

async def main():
    await twitter_etl('barackobama',10)

if __name__ == "__main__":
     asyncio.run(main())