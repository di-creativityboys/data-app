def transform(articles: dict) -> dict:
    transformed_articles = {}  # list to collect only good articles
    counter = 0
    for article in articles.values():
        content = article["contents"]
        lines = content.split("\n")
        if "Let us know you agree to cookies" not in lines[:35] and content.strip() :
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
            counter = counter + 1
    return transformed_articles
