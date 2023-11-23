# %% [markdown]
# ##### This part implements an entire workflow which scrapes the news articles.

# %%
# ToDos for 27.10.2002
"""
Get all articles from the mainpage

From the articles, get everything you can get your hands on.

Turn the article to dictionary form
"""

# %%
from bs4 import BeautifulSoup, Tag
import requests
from typing import List
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
import os
#from getpass import getpass

DB_PASSWORD = "postgres"
DB_PORT = os.environ.get("DATABASE_PORT", "5432")
DB_HOST = os.environ.get("DATABASE_HOST", "localhost")

# %%
MAINPAGE = "edition.cnn.com"
HTTPS_SUFFIX = "https://"
MAINPAGE_LINK = f"{HTTPS_SUFFIX}{MAINPAGE}"

# %%
class Image():
    def __init__(self, url : str, description : str):
        self.url = url
        self.description = description

    def __str__(self):
        return f'Photo description: {self.description}'

class Article():
    def __init__(self, headline : str, content : str, authors : List[str], upload_timestamp : pd.Timestamp, read_time : int, url : str, image : Image):
        self.headline = headline
        self.content = content
        self.authors = authors
        self.upload_timestamp = upload_timestamp
        self.read_time = read_time
        self.url = url
        self.imageUrl = image.url
        self.description = image.description


        self.scraping_timestamp = pd.to_datetime(datetime.now())

    
    def __str__(self):
        string : str = ""
        return f"{self.headline}  by {self.authors}  {self.read_time}\n {self.content} \n"

# %%
def get_soup(url : str)-> BeautifulSoup | None:
    article = requests.get(url).text
    if article:
        return BeautifulSoup(article)
    else:
        print("Error fetching the soup object")

def get_content(article_soup : BeautifulSoup):
    paragraphs = [paragraph.text for paragraph in article_soup.find_all(is_paragraph)]
    string = ""
    for paragraph in paragraphs:
        string = f"{string} {paragraph}"
    return string

def get_article_links(mainpage_soup : BeautifulSoup) -> list:
    results = mainpage_soup.find_all(name="a", attrs={"data-link-type" : "article"})
    results = [f'{MAINPAGE_LINK}{result.attrs["href"]}' for result in results]
    print(results)
    return results

def get_headline(article_soup : BeautifulSoup):
    return article_soup.find("h1").text

def get_authors(article_soup : BeautifulSoup) -> List[str]:
    author_tags = article_soup.find_all(is_author)
    names = [tag.string for tag in author_tags]
    return names

def get_date(article_soup : BeautifulSoup) -> pd.Timestamp:
    date_tag = article_soup.find(is_date)
    date_string = date_tag.text

    # the following code just extracts the datetime from the given date
    splitted_date = date_string.split(",")
    unstructured_time = splitted_date[0].split("\n") # the time is in the 3rd index, look down
    time = unstructured_time[2].lstrip()
    datetime_string_format = f"{time.split(' ')[0]} {time.split(' ')[1]},{splitted_date[-2]},{splitted_date[-1].rstrip()}"
    print(datetime_string_format)
    datetime_correct = pd.to_datetime(datetime_string_format)
    
    return datetime_correct

# since the read time is not stored in the database, this line is obsolete
def get_read_time(article_soup : BeautifulSoup):
    # a read time of 0 is used to signify an article whose reading time could not be fetched.
    read_time_tag = article_soup.find("div", attrs={"class" : ["headline__sub-description"]})  #[15:28] the slicing caused an error so I removed it for testing purposes
    if read_time_tag is None:
        return ""
    read_time : int = extract_read_time_from_string(read_time_tag.text)
    return read_time

def get_image(article_soup : BeautifulSoup) -> Image:
    image_tag = article_soup.find(is_image)
    if image_tag is not None:
        return Image(url=image_tag['src'], description=image_tag['alt']) # modify this
    else:
        return Image("", "")

def is_paragraph(tag : Tag) -> bool:
    return tag.has_attr("data-component-name") and tag.name == "p"

def is_author(tag : Tag) -> bool:
    return tag.get_attribute_list("class")[0] == "byline__name"

def is_date(tag : Tag):
    return tag.get_attribute_list("class")[0] == "timestamp"

def is_image(tag : Tag) -> bool:
    return tag.has_attr("src") and tag.has_attr("alt") and tag.name == "img"

def extract_read_time_from_string(read_time_string : str) -> int:
    # returns 0 if the read_time integer cannot be successfully extracted
    read_time = 0
    for character in read_time_string:
        try:
            read_time = int(character)
        except:
            pass
    return read_time

def extract_upload_time(upload_time_string : str)-> datetime:
    print(upload_time_string)

def create_article_from_link(link : str) ->Article:
    article_soup = get_soup(link)
    headline = get_headline(article_soup)
    content = get_content(article_soup)
    author = get_authors(article_soup)
    date = get_date(article_soup)
    read_time = get_read_time(article_soup)
    url = link
    image = get_image(article_soup)

    return Article(headline, content, author, date, read_time, url, image)

# %%
def filter_articles(articles : List[Article], engine) -> List[Article]:
    new_articles = []
    articles_already_present = pd.read_sql_table("articles", con=engine)
    #  print(articles_already_present.info()) # logging
    urls_of_old_articles = list(articles_already_present["urlid"])
    # print(urls_of_old_articles) # logging
    count_of_old_articles = 0
    for article in articles:
        if article.url[8:] not in urls_of_old_articles:
            new_articles.append(article)
        else:
            count_of_old_articles = count_of_old_articles + 1
    print(f"Count of old articles: {count_of_old_articles}")

    return new_articles

async def scrape_from_cnn():
    mainpage_soup = get_soup(MAINPAGE_LINK)
    links = get_article_links(mainpage_soup)
    articles = []
    for link in links:
        try:
            article = create_article_from_link(link)
            articles.append(article)
        except Exception as e:
            print(f"Following error: {str(e)}")
    
    engine = create_engine(f'postgresql://postgres:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres')
    
    new_articles = filter_articles(articles, engine) # filtered against existing articles in database
    article_dicts = [article.__dict__ for article in new_articles] # this dictionary only contains the articles that are not in the database already

    #this dataframe contains the data to be inserted to the articles table

    articles_dataframe = pd.DataFrame(article_dicts)
    #change the name of url to urlid
    articles_dataframe["urlid"] = articles_dataframe["url"]
    articles_dataframe = articles_dataframe.drop(columns=["url"])


    # change the name of description to image description
    articles_dataframe["imagedescription"] = articles_dataframe["description"]
    articles_dataframe = articles_dataframe.drop(columns=["description"])

    #change the name of upload_timestamp to uploadtimestamp
    articles_dataframe["uploadtimestamp"] = articles_dataframe["upload_timestamp"]
    articles_dataframe = articles_dataframe.drop(columns=["upload_timestamp"])

    #change the name of upload_timestamp to uploadtimestamp
    articles_dataframe["scrapingtimestamp"] = articles_dataframe["scraping_timestamp"]
    articles_dataframe = articles_dataframe.drop(columns=["scraping_timestamp"])

    # fix imageurl, for some reason this column is not recognized correctly
    articles_dataframe["imageurl"] = articles_dataframe["imageUrl"]
    articles_dataframe = articles_dataframe.drop(columns=["imageUrl"])


    # drop the read_time column
    articles_dataframe = articles_dataframe.drop(columns=["read_time"])
    #filtered the duplicates out
    print(articles_dataframe.shape)
    new_articles_dataframe = articles_dataframe.drop_duplicates(subset=["urlid"], keep="first", inplace=True)

    print(articles_dataframe.shape)

    articles_dataframe.to_sql(name = "articles", con=engine, if_exists="append", index=False)

# scrape_from_cnn()