from news_scrape.bbc.extract import extract
from news_scrape.bbc.transform import transform
from news_scrape.bbc.load import load


def bbc_etl() -> None:
    print("[BBC] Extracting...")
    extracted_articles: dict = extract()
    print("[BBC] Transforming...")
    transformed_articles: dict = transform(articles=extracted_articles)
    print("[BBC] Loading...")
    load(transformed_articles=transformed_articles)
    print("[BBC] Scraping finished")
