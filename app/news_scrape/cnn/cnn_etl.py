from database.models.article import Article

from news_scrape.cnn.extract import extract
from news_scrape.cnn.transform import transform
from news_scrape.cnn.load import load

def cnn_etl():
    extracted_articles: list[Article] = extract()
    transformed_articles: list[Article] = transform(extracted_articles)
    load(transformed_articles)