from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import psycopg2
import os

DB_PORT = os.environ.get("DATABASE_PORT", "5432")
DB_HOST = os.environ.get("DATABASE_HOST", "localhost")


async def get_bbc_news():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

    driver.get("https://www.bbc.com/news")

    news_urls = []

    def get_urls():
        elements_for_url = driver.find_elements(By.CLASS_NAME, "gs-c-promo-heading")
        for element in elements_for_url:
            news_urls.append(element.get_attribute("href"))

    get_urls()

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
                header = driver.find_element(By.CLASS_NAME, "qa-story-headline")
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

    # main method to extract all contents except the authors(might follow later). Runs way faster than the different smaller methods before
    text_contents = []
    time = []
    headers = []

    def extract_all():
        for i in range(len(news_urls)):
            # we go to the specific article by using the url
            driver.get(news_urls[i])
            extract_contents(text_contents)
            get_timestamps(time)
            get_headers(headers)
        for i in range(len(time)):
            if time[i] == None:
                time[i] = "unknown"

    extract_all()

    def get_authors(article):
        authors = []
        lines = article.split("\n")
        for line in lines[:13]:  # Loop through lines from lines[0] to lines[10]
            if "By" in line:
                authors.append(line)
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

    import datetime;
    current_time = datetime.datetime.now()
    time_stamp = current_time.timestamp()

    # dictionary with all infos, ordered after attributes
    articles_info = {}
    for i in range(len(news_urls)):
        article_info_i = {
            "headline": headers[i],
            "url": news_urls[i],
            "date": time[i],
            "authors": all_authors[i],
            "read-time": 0, # no info
            "ImageURL": "not yet",
            "ImageDescription": "not yet",
            "contents": text_contents[i],
            "scrapingTimeStamp": time_stamp,
        }
        articles_info[i] = article_info_i

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
            cursor.execute(
                """INSERT INTO Articles(urlId, headline, contents, authors, uploadDate, readTime, imageURL, imageDescription, scrapingTimeStamp) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s);""",
                (
                    article["url"],
                    article["headline"],
                    article["contents"],
                    article["authors"],
                    article["date"],
                    article["read-time"],
                    article["ImageURL"],
                    article["ImageDescription"],
                    article["scrapingTimeStamp"]
                )
            )
        except psycopg2.IntegrityError as e:
            if "duplicate key value violates unique constraint" in str(e):
                print(
                    f"Article with URLId {article['url']} already exists in the database."
                )
