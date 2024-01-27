from social_media_scraping.twitter.scrape_twitter import gettweets


async def extract(user_name, limit):
    # scrape
    scraped_tweets = await gettweets(user_name, limit)
    return scraped_tweets
