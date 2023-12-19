from article import Article

from extract import extract
from transform import transform
from load import load


def cnn_etl():
    extracted_articles = extract()
    transformed_articles = transform(extracted_articles)
    print(transformed_articles)
    load(transformed_articles)

cnn_etl()
