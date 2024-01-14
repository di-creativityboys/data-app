from selenium.webdriver import Chrome, ChromeOptions, ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import pytz
import spacy



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
    all_authors=[]

    # loop through all urls of the articles
    for i in range(len(news_urls)):
        # we go to the specific article by using the url
        driver.get(news_urls[i])
        get_contents(text_contents, driver)
        get_timestamps(time, driver)
        get_headers(headers, driver)
        get_image(imageURL, imageDesc, driver)
    
    get_all_authors(text_contents,all_authors)
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


# function, that preprocesses the urls, so that the topic can be extracted later


# def url_preprocessing(category):
#     # Find the position of the first digit in the category
#     digit_index = next((index for index, char in enumerate(category) if char.isdigit()), None)

#     # Remove everything after the first digit
#     category_without_number = category[:digit_index] if digit_index is not None else category

#     # Remove trailing hyphen
#     if category_without_number.endswith("-"):
#         category_without_number = category_without_number[:-1]

#     index_of_hyphen = category_without_number.rfind("-")  # search starting from the right
#     if index_of_hyphen != -1:  # if there was a hyphen
#         # cut everything to the left
#         result_string = category_without_number[index_of_hyphen + 1 :]
#         return result_string
#     else:
#         return category_without_number


# def get_topic(url, topic):
#     try:
#         parsed_url = urlparse(url)
#         path_segments = parsed_url.path.split("/")

#         # Find the segment after "news"
#         category_segment_index = path_segments.index("news") + 1
#         category = path_segments[category_segment_index]

#         category_without_number = url_preprocessing(category)

#         topic.append(category_without_number)
#     except:
#         try:
#             parsed_url = urlparse(url)
#             path_segments = parsed_url.path.split("/")
#             category_segment_index = path_segments.index("sport") + 1
#             category = path_segments[category_segment_index]

#             category_without_number = url_preprocessing(category)

#             topic.append(category_without_number)

#         except:
#             topic.append(None)
   
def get_contents(text_contents, driver):
    try:
        article = driver.find_element(By.TAG_NAME, "article")
        text_contents.append(article.text)
    except:  # exception if no article element is there. doesn´t happen often, but has to be handled
        article = driver.find_element(By.TAG_NAME, "body")
        text_contents.append(article.text)
        # in this test, 3 of 73 articels had no article element.

    # here are a few exceptions, because the bbc articles have different html structures


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
            #doesnt work yet
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

            


def get_authors(article):
    authors = []
    lines = article.split("\n")
    for line in lines[:13]:  # Loop through lines from lines[0] to lines[10]
        if "By" in line:
            input = line.replace("By", "")
            authors.append(input)
    return authors

# in this section, we extract the authors from the contents
def get_all_authors(contents,all_authors):
    for article in contents:
        authors = get_authors(article)
        if not authors:  # Check if authors is an empty list
            all_authors.append(None)
        else:
            all_authors.extend(authors)

#here we extract the keywords from the contents
def get_topics(contents,topic):
    for article in contents:
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(article)
        if doc.ents:
         for ent in doc.ents:
            topic.append(ent.text)
        else:
            topic.append(None)
