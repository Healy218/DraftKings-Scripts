import tweepy
import datetime

# Twitter API keys
consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"


# Authenticate to Twitter

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Current date and time
current_date = datetime.datetime.today().strftime("%Y-%m-%d")

# Filter tweets from today
today_tweets = []
for tweet in tweepy.Cursor(api.user_timeline, screen_name="earnings_whispers").items():
    if tweet.created_at.strftime("%Y-%m-%d") == current_date:
        today_tweets.append(tweet)

# Find tweets mentioning earnings after the close
earnings_after_close = []
for tweet in today_tweets:
    if "earnings" in tweet.text.lower() and "after close" in tweet.text.lower():
        earnings_after_close.append(tweet)

# Print the results
if earnings_after_close:
    print("**Earnings Whispers - After Close Releases:**")
    for tweet in earnings_after_close:
        print(f"\n- {tweet.text}")
else:
    print("No earnings releases after the close found.")
