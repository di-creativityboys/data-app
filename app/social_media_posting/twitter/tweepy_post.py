import tweepy
import asyncio


async def post_tweet(contents):
    # Your app's bearer token can be found under the Authentication Tokens section
    # of the Keys and Tokens tab of your app, under the
    # Twitter Developer Portal Projects & Apps page at
    # https://developer.twitter.com/en/portal/projects-and-apps
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAEwBrAEAAAAApCxylAsb7QHHl036ZVfpBgCTzjc%3DVlvWB14WqMidgIaIuoPWldLdrA66oEiUcNOdz8QlhrVXlo5dsQ"

    # Your app's API/consumer key and secret can be found under the Consumer Keys
    # section of the Keys and Tokens tab of your app, under the
    # Twitter Developer Portal Projects & Apps page at
    # https://developer.twitter.com/en/portal/projects-and-apps
    consumer_key = "uC22Dsn8SBXK0zUEa3N7qOQCB"
    consumer_secret = "dFGGNuHU353jWzpQvW1kNQsnTvyjt4hZ9zEq0CZ0eJ1l5871q9"

    # Your account's (the app owner's account's) access token and secret for your
    # app can be found under the Authentication Tokens section of the
    # Keys and Tokens tab of your app, under the
    # Twitter Developer Portal Projects & Apps page at
    # https://developer.twitter.com/en/portal/projects-and-apps
    access_token = "1722599919104499712-eTx0A2DVWqhsPsMjF0jLs6HNgSziOF"
    access_token_secret = "ii3AIaTO1ccyQjzhuIS8iRqsFZqxpa3GDvoHy19hKEp7o"

    # You can authenticate as your app with just your bearer token
    client = tweepy.Client(bearer_token=bearer_token)

    # You can provide the consumer key and secret with the access token and access
    # token secret to authenticate as a user
    client = tweepy.Client(
        consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret
    )
    # Create Tweet

    # The app and the corresponding credentials must have the Write permission

    # Check the App permissions section of the Settings tab of your app, under the
    # Twitter Developer Portal Projects & Apps page at
    # https://developer.twitter.com/en/portal/projects-and-apps

    # Make sure to reauthorize your app / regenerate your access token and secret
    # after setting the Write permission

    response = client.create_tweet(text=contents)
    print(f"https://twitter.com/user/status/{response.data['id']}")


async def main():
    tweet = input("Input the tweet that you want to post.\n")
    await post_tweet(tweet)


if __name__ == "__main__":
    asyncio.run(main())
