from twython import Twython
import csv

keys=[]
values=[]
with open("C:/Users/Sumeet Singh/PycharmProjects/HinglishTweets/secrets.txt", 'r') as f:
    reader = csv.reader(f, delimiter=':')
    for key, value in reader:
        key.strip
        value.replace(" ", "")
        keys.append(key)
        values.append(value)

consumer_key = values[0]
consumer_secret = values[1]
auth_token = values[2]
auth_token_secret = values[3]
twitter = Twython(
    consumer_key, consumer_secret)
auth = twitter.get_authentication_tokens(callback_url='https://sites.google.com/site/sumeetiitg/')
access_token = twitter.obtain_access_token()
#access_token = twitter.obtain_access_token()
#tweet = twitter.show_status(id=567809947645255680)
#print(tweet['text'])
