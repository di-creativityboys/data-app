import sys
sys.path.insert(0, "/workspaces/data-app/app/")

import asyncio

# from social_media_scraping.twitter.load_tweets_db import scrape_twitter
from social_media_scraping.twitter.twitter_etl import twitter_etl


async def main():
    await twitter_etl(username="barackobama", limit=10)


if __name__ == "__main__":
    asyncio.run(main())
