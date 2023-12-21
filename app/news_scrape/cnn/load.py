from news_scrape.cnn.article import Article
import pandas as pd
from sqlalchemy import create_engine


def load(articles: pd.DataFrame):
    engine = create_engine(f"postgresql://postgres:postgres@localhost:5432/postgres")
    articles.to_sql(name="articles", con=engine, if_exists="replace", index=False)
