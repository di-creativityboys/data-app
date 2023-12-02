from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import psycopg2
import os
from datetime import datetime
import pytz
from urllib.parse import urlparse

DB_PORT = os.environ.get("DATABASE_PORT", "5432")
DB_HOST = os.environ.get("DATABASE_HOST", "localhost")


async def get_bbc_news():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get("https://www.bbc.com/news")

    news_urls = []

    def get_urls():
        elements_for_url = driver.find_elements(
            By.CLASS_NAME, "gs-c-promo-heading")
        for element in elements_for_url:
            news_urls.append(element.get_attribute("href"))

    get_urls()

    def remove_numbers(category):
        # Find the position of the first digit in the category
        digit_index = next(
            (index for index, char in enumerate(category) if char.isdigit()), None)

    # Remove everything after the first digit
        category_without_number = category[:
                                           digit_index] if digit_index is not None else category

    # Remove trailing hyphen
        if category_without_number.endswith('-'):
            category_without_number = category_without_number[:-1]

        return category_without_number

    def get_topic(url):
        try:
            parsed_url = urlparse(url)
            path_segments = parsed_url.path.split('/')

# Find the segment after "news"
            category_segment_index = path_segments.index("news") + 1
            category = path_segments[category_segment_index]

            category_without_number = remove_numbers(category)

            return category_without_number
        except:

            try:
                parsed_url = urlparse(url)
                path_segments = parsed_url.path.split('/')
                category_segment_index = path_segments.index("sport") + 1
                category = path_segments[category_segment_index]

                category_without_number = remove_numbers(category)

                return category_without_number

            except:

                return "no info"

    def extract_contents(text_contents):
        try:
            article = driver.find_element(By.TAG_NAME, "article")
            text_contents.append(article.text)
        except:  # exception if no article element is there. doesn´t happen often, but has to be handled
            article = driver.find_element(By.TAG_NAME, "body")
            text_contents.append(article.text)
            # in this test, 3 of 73 articels had no article element.
            print("article not found")

    # here are a few exceptions, because the bbc articles have different html structures

    def get_headers(headers):
        try:
            header = driver.find_element(By.ID, "main-heading")
            headers.append(header.text)
        except:
            try:
                header = driver.find_element(
                    By.CLASS_NAME, "qa-story-headline")
                headers.append(header.text)
            except:
                try:
                    header = driver.find_element(
                        By.CLASS_NAME, "article-headline__text"
                    )
                    headers.append(header.text)
                except:
                    header = "unknown"
                    headers.append(header)
                    print("no header")

    def get_timestamps(time):
        try:
            time_element = driver.find_element(By.TAG_NAME, "time")
            date = time_element.get_attribute("datetime")
            time.append(date)
        except:
            date = "unknown"
            time.append(date)
            print("no date")

    def get_Image(imageURL, ImageDesc):
        try:
            image_element = driver.find_element(By.TAG_NAME, 'img')
            url = (image_element.get_attribute('src'))
            desc = (image_element.get_attribute('alt'))
            imageURL.append(url)
            ImageDesc.append(desc)
        except:
            url = None
            desc = None
            imageURL.append(url)
            ImageDesc.append(desc)
    print('no image')

    # main method to extract all contents except the authors(might follow later). Runs way faster than the different smaller methods before
    text_contents = []
    time = []
    headers = []
    imageURL = []
    imageDesc = []
    topic = []

    def extract_all():
        for i in range(len(news_urls)):
            # we go to the specific article by using the url
            driver.get(news_urls[i])
            parsed_url = urlparse(news_urls[i])
            extract_contents(text_contents)
            get_timestamps(time)
            get_headers(headers)
            get_Image(imageURL, imageDesc)
            topic_result = get_topic(news_urls[i])
            topic.append(topic_result)

        for i in range(len(time)):
            if time[i] == None:
                time[i] = "unknown"

    extract_all()

   

    def get_authors(article):
        authors = []
        lines = article.split("\n")
        for line in lines[:13]:  # Loop through lines from lines[0] to lines[10]
            if "By" in line:
                authors.append(line.replace('By', ''))
        return authors

    all_authors = []

    def get_all_authors():
        for article in text_contents:
            authors = get_authors(article)
            if not authors:  # Check if authors is an empty list
                all_authors.append("no author")
            else:
                all_authors.extend(authors)

    get_all_authors()

    germany_timezone = pytz.timezone("Europe/Berlin")

    articles_info = {}
    for i in range(len(news_urls)):
        article_info_i = {
            "headline": headers[i],
            "url": news_urls[i],
            "date": time[i],
            "authors": [all_authors[i]],
            "ImageURL": imageURL[i],
            "ImageDescription": imageDesc[i],
            "scrapingTimeStamp": (datetime.now(germany_timezone).isoformat()).split(".")[0],
            "source": "bbc",
            "topics": topic[i],
            "contents": text_contents[i]
        }
        articles_info[i] = article_info_i
    print(articles_info[20])
# URLId, Headline, Contents, Authors, UploadDate, ReadTime, ImageURL, ImageDescription

    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        port=DB_PORT,
        host=DB_HOST,
    )
    conn.autocommit = True
    cursor = conn.cursor()

    for article in articles_info.values():
        try:
            cursor.execute('''INSERT INTO Articles(URLId, Headline, Content, Authors, UploadTimestamp, ImageURL, ImageDescription,scrapingTimeStamp, source, topic) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s);''',
                           (article["url"], article["headline"], article["contents"], article["authors"], article["date"],
                            article["ImageURL"], article["ImageDescription"], article["scrapingTimeStamp"], article["source"], article["topics"])
                           )
        except psycopg2.IntegrityError as e:
            if "duplicate key value violates unique constraint" in str(e):
                print(
                    f"Article with URLId {article['url']} already exists in the database.")
