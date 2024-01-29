from selenium.webdriver import Chrome, ChromeOptions, ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import pytz
import spacy
import re



def extract() -> dict:
    # Setup Selenium
    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    # Scraping
    driver.get("https://www.bbc.com/news")

    # Stores the urls from the articles, that we will extract in the future
    news_urls = []

    elements_for_url = driver.find_elements(By.CLASS_NAME, "gs-c-promo-heading")

    for element in elements_for_url:
        url_to_article = element.get_attribute("href")
        if url_to_article is None:
            continue

        news_urls.append(url_to_article)

    # main method to extract all contents. Runs way faster than the different smaller methods before
    text_contents = []
    time = []
    headers = []
    imageURL = []
    imageDesc = []
    topic = []
    all_authors = []

    # loop through all urls of the articles
    for i in range(len(news_urls)):
        # we go to the specific article by using the url
        driver.get(news_urls[i])
        get_contents(text_contents, driver)
        get_timestamps(time, driver)
        get_headers(headers, driver)
        get_image(imageURL, imageDesc, driver)
        get_authors(all_authors,driver)
    get_topics(text_contents,topic)


    germany_timezone = pytz.timezone("Europe/Berlin")

    articles_info = {}
    for i in range(len(news_urls)):
        print("iteration", i)
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
            "contents": text_contents[i],
        }
        articles_info[i] = article_info_i

    return articles_info


def extract_text_before_first_number(text):
    match = re.search(r'^(.*?)(\d)', text)
    if match:
        return match.group(1).strip()
    else:
        return text.strip()


def get_contents(text_contents, driver):
    try:
        article = driver.find_element(By.ID, "main-content")
        text_blocks=article.find_elements(By.CSS_SELECTOR, '[data-component="text-block"]')
        merged_text = '\n'.join([text_block.text for text_block in text_blocks])
        text_contents.append(merged_text)
    except:
        try:
            article=driver.find_element(By.CLASS_NAME, 'qa-story-body')
            text_contents.append(article.text)
        except:
            try:
                article=driver.find_element(By.CLASS_NAME, 'body-text-card')
                text_contents.append(article.text)
            except:
                    # exception if no article element is there. doesn´t happen often, but has to be handled
                    article = driver.find_element(By.TAG_NAME, "body")
                    text_contents.append(article.text)
                    print('body')
        # in this test, 3 of 73 articels had no article element.


def get_headers(headers, driver):
    try:
        header = driver.find_element(By.ID, "main-heading")
        headers.append(header.text)
    except:
        try:
            header = driver.find_element(By.CLASS_NAME, "qa-story-headline")
            headers.append(header.text)
        except:
            try:
                header = driver.find_element(By.CLASS_NAME, "article-headline__text")
                headers.append(header.text)
            except:
                header = None
                headers.append(header)

def get_authors(all_authors, driver):
    try:
        authors_text = driver.find_element(By.CSS_SELECTOR, '[data-component="byline-block"]').text
        if "BBC" in authors_text:
            authors_first_step=authors_text.split("BBC")[0].strip()#remove unnecessary text
        elif "Culture" in authors_text:
            authors_first_step=authors_text.split("Culture")[0].strip()#remove unnecessary text
        else:
            authors_first_step=authors_text.split("Business")[0].strip()#remove unnecessary text
        authors=authors_first_step.split("By")[1].strip()
        all_authors.append(authors)
    except:
        try:
            authors_first = driver.find_element(By.CLASS_NAME, "author-unit")
            authors = extract_text_before_first_number(authors_first)
            all_authors.append(authors)
        except:
                authors = None
                #all_authors.append(authors)


def get_timestamps(time, driver):
    try:
        time_element = driver.find_element(By.TAG_NAME, "time")
        date = time_element.get_attribute("datetime")
        # ignore the error, it works when it´s accessed by the main function
        time.append(date.split(".")[0])
    except:
        date = None
        time.append(date)


def get_image(imageURL, ImageDesc, driver):
    try:
        main_content = driver.find_element(By.ID, "main-content")
        image_element = main_content.find_element(By.TAG_NAME, "img")
        url = image_element.get_attribute("src")
        desc = image_element.get_attribute("alt")
        imageURL.append(url)
        ImageDesc.append(desc)
    except:
        try:
            # doesnt work yet
            main_content = driver.find_element(By.TAG_NAME, "picture")
            image_element = main_content.find_element(By.TAG_NAME, "img")
            url = image_element.get_attribute("src")
            desc = image_element.get_attribute("alt")
            imageURL.append(url)
            ImageDesc.append(desc)
        except:
            url = None
            desc = None
            imageURL.append(url)
            ImageDesc.append(desc)


# here we extract the keywords from the contents
def get_topics(contents, topic):
    for article in contents:
        # IMPORTANT: ASK BEFORE CHANGING THE MODEL!!!!!!!!!!!!!!!!!!
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(article)
        if doc.ents:
            for ent in doc.ents:
                topic.append(ent.text)
        else:
            topic.append(None)
