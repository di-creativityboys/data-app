from news_clustering.extract import extract_articles
from news_clustering.transform import transform_and_cluster_articles
from news_clustering.load import load_clusters_into_db



async def cluster_articles_in_db():

    articles = extract_articles()
    clustered_articles = transform_and_cluster_articles(articles)
    load_clusters_into_db(clustered_articles)