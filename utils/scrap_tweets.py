import tweepy
import re
import csv

def removeURLs(text):
    return re.sub(r"http\S+", "", text)
    
def deEmojify(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'',text)

csv.register_dialect('twitter_dialect', delimiter='|', quoting=csv.QUOTE_NONE, escapechar='\\')

consumer_key=""
consumer_secret=""

access_token=""
access_token_secret=""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.user_timeline(user_id='algo_diver', count=1000, tweet_mode="extended")

with open('twitter.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, dialect='twitter_dialect')
    for page in range(1, 5):
        public_tweets = api.user_timeline(user_id='algo_diver', count=200, tweet_mode="extended", page=page)

        for tweet in public_tweets:
            if hasattr(tweet, 'retweeted_status'):
                author = "@" + deEmojify(tweet.retweeted_status.author.name)
                result = author + " " + deEmojify(tweet.retweeted_status.full_text.replace("\n", " ").replace("  ", " ").strip())
                result = result.replace("|", "&")
                result = removeURLs(result)
                print("- " + result)
                print("--------------------------------------------------------------")
                writer.writerow([result, '0'])
"""
with open('twitter.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, dialect='twitter_dialect')
#    writer.writerow(['text', 'category'])

    for tweet in public_tweets:
        if hasattr(tweet, 'retweeted_status'):
            author = "@" + deEmojify(tweet.retweeted_status.author.name)
            result = author + " " + deEmojify(tweet.retweeted_status.full_text.replace("\n", " ").replace("  ", " ").strip())
            result = result.replace("|", "&")
            result = removeURLs(result)
            print("- " + result)
            print("--------------------------------------------------------------")
            writer.writerow([result, '0'])
"""
