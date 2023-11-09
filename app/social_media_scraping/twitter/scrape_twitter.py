import asyncio
import brotli
from twscrape import API, gather
from twscrape.logger import set_log_level

async def gettweets(user_login, limit):
    api = API()  # or API("path-to.db") - default is `accounts.db`
    # ADD ACCOUNTS 
    await api.pool.add_account("BingBong2397074", "BingBong", "", "")
    await api.pool.add_account("BBong20237297", "BingBong", "", "")
    await api.pool.add_account("bong220059128", "BingBong", "", "")
    await api.pool.add_account("Bong2021Bi31407", "BingBong", "", "")
    await api.pool.add_account("BBong20223868", "BingBong", "", "")
    await api.pool.add_account("BBong202380929", "BingBong", "", "")
    await api.pool.add_account("BBong202320783", "BingBong", "", "")
    await api.pool.add_account("BBong202339368", "BingBong", "", "")
    await api.pool.add_account("BBong202355016", "BingBong", "", "")
    await api.pool.add_account("BBong202338320", "BingBong", "", "")
    await api.pool.login_all()
    await api.pool.relogin_failed()
    await api.pool.reset_locks()
    
    #get user by login
    user_login = await api.user_by_login(user_login)  # User
    #print("user login:", user_login, "\n")
    # user info
    user_id = user_login.id
    #print("user id:", user_id, "\n")
    out = await gather(api.user_tweets(user_id, limit))  # list[Tweet]
    #print(out) # - print the actual response 
    # change log level, default info
    ##set_log_level("DEBUG")
    ##tweetno = 1
    ##for tweet in out:
    ##    print("This is tweet number", tweetno, ":")
    ##    tweetno += 1
    ##    print(tweet.rawContent, "\n")
    return out