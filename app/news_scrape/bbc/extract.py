from selenium.webdriver import Chrome, ChromeOptions, ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def extract():
    ########## Setup Selenium
    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options
    )
    
    ########## Scraping
    driver.get("https://www.bbc.com/news")
    
    # Stores the urls from the articles, that we will extract in the future
    news_urls = []

    elements_for_url = driver.find_elements(By.CLASS_NAME, "gs-c-promo-heading")
    
    for element in elements_for_url:
        news_urls.append(element.get_attribute("href"))