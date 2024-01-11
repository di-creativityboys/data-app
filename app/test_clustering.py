import sys

sys.path.insert(0, "/workspaces/data-app/app/")

import asyncio

from news_clustering.cluster_news_etl import cluster_articles_in_db


async def main():
    await cluster_articles_in_db()


if __name__ == "__main__":
    asyncio.run(main())
