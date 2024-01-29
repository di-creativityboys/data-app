import pandas as pd
from sqlalchemy import create_engine
import os

DATABASE_PORT: str = os.environ.get("DATABASE_PORT", "5432")
DATABASE_HOST: str = os.environ.get("DATABASE_HOST", "localhost")


def load(articles: pd.DataFrame):
    engine = create_engine(f"postgresql://postgres:postgres@{DATABASE_HOST}:{DATABASE_PORT}/postgres")
    articles.to_sql(name="articles", con=engine, if_exists="append", index=False)
