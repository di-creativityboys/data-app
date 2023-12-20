# from article import Article

from news_scrape.cnn.extract import extract
from news_scrape.cnn.transform import transform
from news_scrape.cnn.load import load


def cnn_etl():
    extracted_articles = extract()
    transformed_articles = transform(extracted_articles)
    print(transformed_articles)
    load(transformed_articles)
