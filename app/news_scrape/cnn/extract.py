from bs4 import BeautifulSoup, Tag
import pandas as pd
import requests

from news_scrape.cnn.article import Article


MAINPAGE = "edition.cnn.com"
HTTPS_SUFFIX = "https://"
MAINPAGE_LINK = f"{HTTPS_SUFFIX}{MAINPAGE}"


def extract() -> list[Article]:
    mainpage_soup = get_soup(MAINPAGE_LINK)
    # TODO: Rewrite maybe with try and catch
    
    links = get_article_links(mainpage_soup)

    articles: list[Article] = []

    for link in links:
        try:
            article = create_article_from_link(link)
            articles.append(article)
        except Exception as e:
            print(f"Following error: {str(e)}")

    return articles


def get_soup(url: str) -> BeautifulSoup:
    response = requests.get(url).text
    #if response:
    return BeautifulSoup(response, features="html.parser")
    # else:
    #    print("Error fetching the soup object")


def get_article_links(mainpage_soup: BeautifulSoup) -> list:
    results = mainpage_soup.find_all(name="a", attrs={"data-link-type": "article"})
    results = [f'{MAINPAGE_LINK}{result.attrs["href"]}' for result in results]

    return results

def create_article_from_link(link: str) -> Article:
    article_soup = get_soup(link)
    headline = get_headline(article_soup)
    content = get_content(article_soup)
    authors = get_authors(article_soup)
    date = get_date(article_soup)
    #read_time = get_read_time(article_soup)
    url = link
    image_tuple = get_image_tuple(article_soup)
    topic = get_topic(article_soup)

    # TODO:
    return Article(urlId=url,
                   headline=headline,
                   content=content,
                   authors=authors, # where is the get authors method
                   upload_timestamp=date, # the upload timestamp
                   imageURL=image_tuple[0], # the image url 
                   imageDescription=image_tuple[1], # the image description 
                   scrapingTimestamp=pd.Timestamp.now(),
                   source="cnn",
                   topic=topic)

def get_headline(article_soup: BeautifulSoup):
    headline = ""
    tag_or_navigatablestring = article_soup.find("h1")
    if tag_or_navigatablestring is not None:
        headline = tag_or_navigatablestring.text
    return headline

def get_content(article_soup: BeautifulSoup):
    paragraphs = [
        paragraph.text for paragraph in article_soup.find_all(is_paragraph)]
    string = ""
    for paragraph in paragraphs:
        string = f"{string} {paragraph}"
    return string

def get_authors(article_soup: BeautifulSoup) -> list[str]:
    author_tags = article_soup.find_all(is_author)
    names = [tag.string for tag in author_tags]
    return names

def get_date(article_soup: BeautifulSoup) -> pd.Timestamp:
    date_string = ""
    # TODO: Why do you search for a boolean? In "get_headline" you searched for an HTML Tag
    tag_or_navigatablestring = article_soup.find(is_date)
    if tag_or_navigatablestring is not None:
        date_string = tag_or_navigatablestring.text

    # the following code just extracts the datetime from the given date
    splitted_date = date_string.split(",")
    # the time is in the 3rd index, look down
    unstructured_time = splitted_date[0].split("\n")
    time = unstructured_time[2].lstrip()
    datetime_string_format = f"{time.split(' ')[0]} {time.split(' ')[1]},{splitted_date[-2]},{splitted_date[-1].rstrip()}"
    print(datetime_string_format)
    datetime_correct = pd.to_datetime(datetime_string_format)

    return datetime_correct

def get_read_time(article_soup: BeautifulSoup):
    # a read time of 0 is used to signify an article whose reading time could not be fetched.
    # [15:28] the slicing caused an error so I removed it for testing purposes
    read_time_tag = article_soup.find(
        "div", attrs={"class": ["headline__sub-description"]})
    if read_time_tag is None:
        return ""
    read_time: int = extract_read_time_from_string(read_time_tag.text)
    return read_time

def get_image_tuple(article_soup: BeautifulSoup) -> tuple:
    image_tag = article_soup.find(is_image)
    if image_tag is not None:
        # modify this
        return (image_tag['src'], image_tag['alt'])
    else:
        return ("", "")

def get_topic(article_soup : BeautifulSoup):
    topic_tag = article_soup.find("a", class_="brand-logo__theme-link")
    if type(topic_tag) == Tag:
        link = topic_tag["href"]
        if type(link) == str:
            link_list = link.split("/")
            return link_list[-1]
    return ''

def is_topic(tag : Tag):
    return tag.get_attribute_list("class")[0] == "brand-logo__theme-link"
    
def is_paragraph(tag: Tag) -> bool:
    return tag.has_attr("data-component-name") and tag.name == "p"


def is_author(tag: Tag) -> bool:
    return tag.get_attribute_list("class")[0] == "byline__name"

def is_date(tag: Tag):
    return tag.get_attribute_list("class")[0] == "timestamp"


def is_image(tag: Tag) -> bool:
    return tag.has_attr("src") and tag.has_attr("alt") and tag.name == "img"

def extract_read_time_from_string(read_time_string: str) -> int:
    # returns 0 if the read_time integer cannot be successfully extracted
    read_time = 0
    for character in read_time_string:
        try:
            read_time = int(character)
        except:
            pass
    return read_time
