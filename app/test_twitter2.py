import sys
sys.path.insert(0, "/workspaces/data-app/app/")

import asyncio

from social_media_scraping.twitter.v2.twitter_etl import twitter_etl


async def main():
    await twitter_etl(5,'BarackObama')#how far do we want to scroll down

if __name__ == "__main__":
    asyncio.run(main())
