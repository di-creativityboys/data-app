import asyncio

# from social_media_scraping.twitter.load_tweets_db import scrape_twitter
from social_media_scraping.twitter.new_twitter_scrape.twitter_etl import twitter_etl


async def main():
    await twitter_etl(5,'BarackObama')#how far do we want to scroll down

if __name__ == "__main__":
    asyncio.run(main())
