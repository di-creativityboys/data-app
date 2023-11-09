from bs4 import BeautifulSoup, Tag, NavigableString
import requests
from typing import List
from datetime import datetime
import psycopg2
import pandas as pd
import os

DB_PORT = os.environ.get("DATABASE_PORT", "5432")
DB_HOST = os.environ.get("DATABASE_HOST", "localhost")

MAINPAGE = "edition.cnn.com"
HTTPS_SUFFIX = "https://"
MAINPAGE_LINK = f"{HTTPS_SUFFIX}{MAINPAGE}"

class Image():
    def __init__(self, url : str, description : str):
        self.url = url
        self.description = description

    def __str__(self):
        return f'Photo description: {self.description}'

class Article():
    def __init__(self, headline : str, contents : str, authors : List[str], date : datetime, read_time : int, url : str, image : Image):
        self.headline = headline
        self.contents = contents
        self.authors = authors
        self.date = date
        self.read_time = read_time
        self.url = url
        self.image = image


        self.timestamp = datetime.now()

    
    def __str__(self):
        string : str = ""
        return f"{self.headline}  by {self.authors}  {self.read_time}\n {self.contents} \n"
    
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

def get_date(article_soup : BeautifulSoup):
    date_tag = article_soup.find(is_date)
    date_string = date_tag.text
    date = extract_date_from_string(date_string)
    return date

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
            read_time =  int(character)
        except:
            pass
    return read_time

def extract_date_from_string(date_string : str):
    # returns 0 if no date could be extracted
    # python function to remove white spaces in front of word
    # FIX
    date = 0
    for i in range(0, len(date_string)+1):
        for j in range(i, len(date_string)+1):
            try:
                date = datetime.strptime(date_string[i:j], "%B %d, %Y")
                break
            except:
                pass
    return date

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

mainpage_soup = get_soup(MAINPAGE_LINK)
links = get_article_links(mainpage_soup)

articles = [create_article_from_link(link) for link in links.copy()]
#delay scraping intensity to not get banned

conn = psycopg2.connect(dbname="postgres",user="postgres", password="postgres", port=DB_PORT, host=DB_HOST)
conn.autocommit = True
cursor = conn.cursor()

def filter_articles(articles : List[Article]) -> List[Article]:
    new_articles = []
    articles_already_present = pd.read_sql(sql="SELECT * FROM Articles", con=conn)
    urls_of_old_articles = list(articles_already_present["urlid"])
    count_of_old_articles = 0
    for article in articles:
        if article.url[8:] not in urls_of_old_articles:
            new_articles.append(article)
        else:
            count_of_old_articles = count_of_old_articles + 1
    print(f"Count of old articles: {count_of_old_articles}")
    return new_articles

new_articles = filter_articles(articles)

article_dicts = [article.__dict__ for article in new_articles] # this dictionary only contains the articles that are not in the database already

for article_dictionary in article_dicts:
    try:
        cursor.execute('''INSERT INTO Articles(urlId, headline, contents, authors, uploadDate, readTime, imageURL, imageDescription, scrapingTimeStamp) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);''', 
                       (article_dictionary["url"][8:], 
                       article_dictionary["headline"], 
                       article_dictionary["contents"], 
                       article_dictionary["authors"], 
                       article_dictionary["date"], 
                       article_dictionary["read_time"], 
                       article_dictionary["image"].url[8:], 
                       article_dictionary["image"].description, 
                       article_dictionary["timestamp"])
                       )
        
    except Exception as ex:
        print("Duplicate detected, skipping to next article." + str(ex))

'''
Notes: The urls are saved without the https:// prefix, seeing as I got an error while doing so.
All textual datatypes have been saved as text, so that has to be done better in the future. Best solution is to convert
the attributes.
The execute statement does not check whether a record is present in the table or not.
The solution I can think of now is to export the data of the database into a json format.
After that, each time the program is started, the URLIDs are extracted and compared against
the news that are scraped and the articles found in both are removed from the scraped articles.
This ensures that the articles added to the database are the new ones.
'''