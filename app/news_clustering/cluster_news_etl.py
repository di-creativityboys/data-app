from news_clustering.extract import extract_articles
from news_clustering.transform import transform_and_cluster_articles
from news_clustering.load import load_clusters_into_db



async def cluster_articles_in_db():
    print("[Cluster] Extracting...")
    articles = extract_articles()
    print("[Cluster] Transforming...")
    clustered_articles = transform_and_cluster_articles(articles=articles)
    print("[Cluster] Loading...")
    load_clusters_into_db(articles=clustered_articles)
    print("[Cluster] Cluster finished")