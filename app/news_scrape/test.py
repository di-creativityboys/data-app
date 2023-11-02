import asyncio
import psycopg2
from bbc.bbc import get_bbc_news

def manual_db_init():
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", port="5432", host="localhost")
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute(open("./database.sql", "r").read())

    conn.close()
    print("DB initialized")

async def main():
    manual_db_init()
    await get_bbc_news()


if __name__ == "__main__":
    asyncio.run(main())

