# from article import Article

from news_scrape.cnn.extract import extract
from news_scrape.cnn.transform import transform
from news_scrape.cnn.load import load


async def cnn_etl():
    print("[CNN] Extracting...")
    extracted_articles = extract()
    print("[CNN] Transforming...")
    transformed_articles = transform(extracted_articles)
    print(transformed_articles)
    print("[CNN] Loading...")
    load(transformed_articles)
    print("[CNN] Scraping finished")