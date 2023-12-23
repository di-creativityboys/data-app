import sys
sys.path.insert(0, "/workspaces/data-app/app/")

import asyncio

from database.database import Database
from news_scrape.cnn.cnn_etl import cnn_etl


def manual_db_init():
    database = Database()
    database.open_connection()
    database.initialize_schema()
    database.close_connection()
    print("DB initialized")


async def main():
    manual_db_init()

    await cnn_etl()


if __name__ == "__main__":
    asyncio.run(main())
