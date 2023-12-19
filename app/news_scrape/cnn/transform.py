import pandas as pd
from sqlalchemy import create_engine

from database.models.article import Article


def transform(articles: list[Article]) -> list[Article]:
    # filtered against existing articles in database
    new_articles = filter_articles(articles, get_engine())

    # this dictionary only contains the articles that are not in the database already
    article_dicts = [article.__dict__ for article in new_articles]

    # this dataframe contains the data to be inserted to the articles table

    articles_dataframe = pd.DataFrame(article_dicts)
    # change the name of url to urlid
    articles_dataframe["urlid"] = articles_dataframe["url"]
    articles_dataframe = articles_dataframe.drop(columns=["url"])
    # change the name of description to image description
    articles_dataframe["imagedescription"] = articles_dataframe["description"]
    articles_dataframe = articles_dataframe.drop(columns=["description"])
    # change the name of upload_timestamp to uploadtimestamp
    articles_dataframe["uploadtimestamp"] = articles_dataframe["upload_timestamp"]
    articles_dataframe = articles_dataframe.drop(columns=["upload_timestamp"])
    # change the name of upload_timestamp to uploadtimestamp
    articles_dataframe["scrapingtimestamp"] = articles_dataframe["scraping_timestamp"]
    articles_dataframe = articles_dataframe.drop(columns=["scraping_timestamp"])
    # fix imageurl, for some reason this column is not recognized correctly
    articles_dataframe["imageurl"] = articles_dataframe["imageUrl"]
    articles_dataframe = articles_dataframe.drop(columns=["imageUrl"])
    # drop the read_time column
    articles_dataframe = articles_dataframe.drop(columns=["read_time"])
    print(articles_dataframe["urlid"])
    # filtered the duplicates out
    print(articles_dataframe.shape)
    articles_dataframe.drop_duplicates(subset=["urlid"], keep="first", inplace=True)
    print(articles_dataframe.shape)

    return articles

def filter_articles(articles: list[Article], engine) -> list[Article]:
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

def get_engine():
    return create_engine(f'postgresql://postgres:postgres@localhost:5432/postgres')