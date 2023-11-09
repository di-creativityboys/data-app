import asyncio
from twitter.load_tweets_db import scrape_and_load_db

async def main():
    await scrape_twitter('barackobama',10)

if __name__ == "__main__":
     asyncio.run(main())