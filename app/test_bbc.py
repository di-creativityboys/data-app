import sys
sys.path.insert(0, "/workspaces/data-app/app/")

import asyncio

from database.database import Database
from news_scrape.bbc.bbc_etl import bbc_etl


def manual_db_init():
    database = Database()
    database.open_connection()
    database.initialize_schema()
    database.close_connection()
    print("DB initialized")


async def main():
    manual_db_init()

    await bbc_etl()


if __name__ == "__main__":
    asyncio.run(main())
