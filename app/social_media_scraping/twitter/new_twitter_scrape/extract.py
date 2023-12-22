# %%
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import pytz

def extract(steps,user):#steps=how far do we want to scroll
# %%
   options = Options()
   options.add_argument('--headless')
   options.add_argument('--no-sandbox')
   options.add_argument('--disable-dev-shm-usage')
   driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

   url=f"https://twitter.com/{user}"
   driver.get(url)
   time.sleep(5)
   print(driver.title)

   # %%

   # find all tweet elements

   #gets the text from the tweets of the current scroll page
   def get_tweetText(elements):
      contents=[]
      # get tweet text
      for element in elements:
         try:
            div_element = element.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]')
            contents.append(div_element.text)
         except:
            contents.append(None)
      return contents

   # %%
   # find all tweet elements
   #gets the text from the tweets of the current scroll page
   def get_tweetDate(elements):
      tweets_dates=[]
      # the format of the input date
      date_format = "%b %d, %Y"
      # the format of the output date date
      date_format_output= "%Y-%m-%d"
      # get tweet date
      for element in elements:
         try:
            div_element = element.find_element(By.TAG_NAME, 'time')
            date_objekt = datetime.strptime(div_element.text, date_format)
            timestamp_date = date_objekt.strftime(date_format_output)
            tweets_dates.append(timestamp_date)
         except:
               tweets_dates.append(None)
      return tweets_dates



   # %%
   #elements = driver.find_elements(By.CSS_SELECTOR, '[data-testid="cellInnerDiv"]')#get divs of the elements


   def get_tweetImage(elements):
      images=[]
      # get tweet text
      for element in elements:
         try:
            div_element = element.find_element(By.CSS_SELECTOR, '[data-testid="Tweet-User-Avatar"]')#div of profil image
            image_element = div_element.find_element(By.TAG_NAME, 'img')#img class of profil image
            image=image_element.get_attribute("src")#url of image
            images.append(image)
         except:
            images.append(None)
      return images

   # %%
   #elements = driver.find_elements(By.CSS_SELECTOR, '[data-testid="cellInnerDiv"]')#get divs of the elements

   def get_icons(elements):
      tweets_comments=[]
      tweets_shares=[]
      tweets_likes=[]
      # get tweet date
      for element in elements:
         try:
            div_elements = element.find_elements(By.CSS_SELECTOR, '[data-testid="app-text-transition-container"]')
            comment_count=div_elements[0].text
            comment_count_int=int(comment_count.replace('K', '000').replace('M', '00000').replace('.',''))
            share_count = div_elements[1].text
            share_count_int=int(share_count.replace('K', '000').replace('M', '00000').replace('.',''))
            likes_count = div_elements[2].text
            likes_count_int=int(likes_count.replace('K', '000').replace('M', '00000').replace('.',''))
            tweets_comments.append(comment_count_int)
            tweets_shares.append(share_count_int)
            tweets_likes.append(likes_count_int)

         except:
            tweets_comments.append(None)
            tweets_shares.append(None)
            tweets_likes.append(None)

      return tweets_comments,tweets_shares,tweets_likes

   #test1,test2,test3=get_icons(elements)
   #print(test1,test2,test3)

   # %%


   germany_timezone = pytz.timezone("Europe/Berlin")
   def get_everything(steps):
      dict_tweets={}
      scroll_value=0
      for _ in range(steps):
            help_dict_tweets={}
            driver.execute_script(f"window.scrollTo(0, {scroll_value})")
            time.sleep(3)
            elements = driver.find_elements(By.CSS_SELECTOR, '[data-testid="cellInnerDiv"]')#get divs of the elements

            tweetTexts=get_tweetText(elements)
            tweetDates=get_tweetDate(elements)
            tweetImages=get_tweetImage(elements)
            tweetComments,tweetShares,tweetLikes=get_icons(elements)

            for i in range(len(tweetTexts)):
               dict_tweets_one_scroll={#one tweet
                  "content":tweetTexts[i],
                  "date":tweetDates[i],
                  "image":tweetImages[i],
                  "comment":tweetComments[i],
                  "scrapingTimeStamp":(datetime.now(germany_timezone).isoformat()).split(".")[0],
                  "share":tweetShares[i],
                  "likes":tweetLikes[i],
                  "user":user
            }
               help_dict_tweets[i]=dict_tweets_one_scroll

            #annoying and complicating steps in order to fill the dict without overwriting values
            length=len(help_dict_tweets)
            length2=len(dict_tweets)#length of current dict

            e=0
            for k in range(length2,(length2+length)-1):
               dict_tweets[k]=help_dict_tweets[e]
               e+=1


            scroll_value+=3500#prepare scroll for next iteration, this has proven to be a good value
      return dict_tweets

   tweet_info=get_everything(steps)
   print(tweet_info)
   print(len(tweet_info))

   # %%
   def remove_duplicates(tweets):

   # Create a set to store unique content strings
      unique_contents = set()

      # Create a new dictionary to store non-duplicate entries
      filtered_data = {}

      # Iterate through the original dictionary
      for key, value in tweets.items():
         content = value.get('content')
         
         # Check if content already exists in the set
         if content not in unique_contents:
            # If not, add it to the set and the filtered dictionary
            unique_contents.add(content)
            filtered_data[key] = value
      return filtered_data

   filtered_tweets=remove_duplicates(tweet_info)
   print(filtered_tweets)
   print(len(filtered_tweets))

   return filtered_tweets

#extract(2,'BarackObama')


