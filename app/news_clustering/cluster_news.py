# Clustering of articles from database (as they origin from different sources e.g. CNN, BBC)

# 1 Preprocess content
# 2 Cluster based on content
# 3 Per cluster: majority vote on topic as a clusterTopic

# goal: only show one news article per cluster in frontend (on demand show more)


# ------------- IMPORT --------------------

# ensure path for database module works
import sys
sys.path.insert(0,'/workspaces/data-app/app/database')

# basic imports
import psycopg2
import pandas as pd
import numpy as np
import pandas.io.sql as sqlio
from database import Database # type: ignore

# imports preprocessing
import re
import sys
import nltk
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk import word_tokenize
from collections import Counter
import time

# download nltk packages if needed
# nltk.download('stopwords')
# nltk.download('wordnet')

# imports TFIDF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# imports clustering

from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score



# -------------- EXTRACT -----------------

def extract_articles():
    # open database connection
    database = Database()
    database.open_connection()

    # get articles table into datframe
    sql = "SELECT * FROM articles;"
    articles = sqlio.read_sql_query(sql, database.connection)
    database.close_connection()

    return articles



# ------------- TRANSFORM ---------------

# Preprocessing content attribute (Option B from notebook)
def preprocess_lemmatizer(text):
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = text.lower()  # Convert to lowercase
    words = text.split()
    words = [word for word in words if word not in stopwords.words("english")]  # Remove stopwords
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]  # Stem words
    return ' '.join(words)


def transform_and_cluster_articles(articles):
    # apply preprocessing on articles
    preprocessed_lemmatized_articles = articles.content.apply(lambda x: preprocess_lemmatizer(x))

    # TFIDF vectorizing
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(preprocessed_lemmatized_articles)

    # dimensionality reduction (100 is known to be good approximation)
    pca = TruncatedSVD(n_components=100)
    tfidf_matrix_pca = pca.fit_transform(tfidf_matrix)

    # determine best k for Kmeans clustering
    silhouette_avg = []
    for num_clusters in list(range(2,len(articles))):
        kmeans = KMeans(n_clusters=num_clusters, init = "k-means++", n_init = 10)
        kmeans.fit_predict(tfidf_matrix_pca)
        score = silhouette_score(tfidf_matrix_pca, kmeans.labels_)
        silhouette_avg.append(score)
    best_k = np.argmax(silhouette_avg) + 2 # type: ignore

    # clustering
    clf = KMeans(n_clusters=best_k, verbose = 0)
    clf.fit(tfidf_matrix_pca)
    articles['clusterId'] = clf.labels_

    # majority voting for topic per cluster
    articles['clusterTopic'] = None
    for index, article in articles.iterrows():
        cluster = article['clusterId']
        currentdf = articles.loc[articles['clusterId'] == cluster]
        articles['clusterTopic'][index] = currentdf.topic.mode()[0]
    
    return articles



# -------------- LOAD ----------------

def load_clusters_into_db(articles):
    # new database connection
    database = Database()
    database.open_connection()

    # write clusterIds and clusterTopics into database
    for index, row in articles.iterrows():
        try:
            database.execute('''UPDATE articles
                                SET clusterId = %s, clusterTopic = %s
                                WHERE urlid = %s''',
                                (row.clusterId,
                                 row.clusterTopic,
                                 row.urlid
                                )
                            )
        except BaseException as ex:
            print('Error: ', ex)
    database.close_connection()
   


# ------------- MAIN -------------------- 

async def cluster_articles_in_db():

    articles = extract_articles()
    clustered_articles = transform_and_cluster_articles(articles)
    load_clusters_into_db(clustered_articles)
