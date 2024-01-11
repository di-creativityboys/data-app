from datetime import datetime
import pytz

def transform(articles: dict) -> dict:
    transformed_articles={}#list to collect only good articles
    germany_timezone = pytz.timezone("Europe/Berlin")
    counter=0
    for article in articles.values():
        content=article["contents"]
        lines = content.split("\n")
        if not "Let us know you agree to cookies" in lines[:35]:
                article_info_i = {
                    "headline": article["headline"],
                    "url": article["url"],
                    "date": article["date"],
                    "authors": article["authors"],
                    "ImageURL": article["ImageURL"],
                    "ImageDescription": article["ImageDescription"],
                    "scrapingTimeStamp": article["scrapingTimeStamp"],
                    "source": article["source"],
                    "topics": article["topics"],
                    "contents": article["contents"],
        }
                transformed_articles[counter] = article_info_i
                counter=counter+1
    return transformed_articles
