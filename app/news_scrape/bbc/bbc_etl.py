from database.models.article import Article

from news_scrape.bbc.extract import extract
from news_scrape.bbc.transform import transform
from news_scrape.bbc.load import load

def bbc_etl():
    extracted_articles: dict = extract()
    transformed_articles: dict = transform(extracted_articles)
    load(transformed_articles)