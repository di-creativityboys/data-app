from gettext import translation
import pandas as pd
from sqlalchemy import create_engine

from news_scrape.cnn.article import Article

engine = create_engine(f"postgresql://postgres:postgres@localhost:5432/postgres")


def transform(articles: list[Article]) -> pd.DataFrame:
    # filtered against existing articles in database
    new_articles = filter_articles(articles)

    # this dictionary only contains the articles that are not in the database already
    article_dicts = [article.__dict__ for article in new_articles]

    # this dataframe contains the data to be inserted to the articles table

    articles_dataframe = pd.DataFrame(article_dicts)
    articles_dataframe.columns = articles_dataframe.columns.str.lower()
    # change the name of url to urlid
    articles_dataframe.rename(columns={"upload_timestamp": "uploadtimestamp"})
    print(articles_dataframe.info())
    articles_dataframe.drop_duplicates(subset=["urlid"], keep="first", inplace=True)

    return articles_dataframe


def filter_articles(articles: list[Article]) -> list[Article]:
    new_articles = []
    articles_already_present = pd.read_sql_table("articles", con=engine)
    #  print(articles_already_present.info()) # logging
    urls_of_old_articles = list(articles_already_present["urlid"])
    # print(urls_of_old_articles) # logging
    count_of_old_articles = 0
    for article in articles:
        if article.urlId[8:] not in urls_of_old_articles:
            new_articles.append(article)
        else:
            count_of_old_articles = count_of_old_articles + 1
    print(f"Count of old articles: {count_of_old_articles}")

    return new_articles
