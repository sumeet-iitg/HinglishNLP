# -*- coding: utf-8 -*-

import tweepy
import csv
import sys
import time
import codecs


consumer_key= '0FwPy04vOpzNdi7CCEXEnDmSI'
consumer_secret = 'bPtFRye33nemEk9uMvTS97QLDHTTDtWunrLoKNHZeBLE1qaKsC'
auth_token = '175123301-g3NCDkOX6GPhMTha8wnPquSZGvNUChPSZRMX5M4h'
auth_token_secret = '8NknUXUXHDkl86sYEuYC2jBYVSRRqZSwvedgFESw7pfPE'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(auth_token, auth_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def batchTweetCollection():
    tweetIds = []
    with open("C:/Users/Sumeet Singh/Documents/Code-Mixed/EMNLPDataSetAllThatsEnglish.csv", 'r') as f:
        reader = csv.reader(f)
        for tweet in reader:
            tweetIds.append(tweet[0])
            # batch 100 tweet Ids before making a tweet collection request
            if tweetIds.__len__() == 100:
                successDownload = False
                while not successDownload:
                    try:
                        statuses = api.statuses_lookup(tweetIds)
                        successDownload = True
                    except tweepy.TweepError:
                        print("Encountered Tweepy error... sleeping for 300")
                        # sleep for sometime to overcome request drop by twitter.
                        time.sleep(60*5)
                with open("C:/Users/Sumeet Singh/Documents/Code-Mixed/EMNLPTweetsFull.csv", 'a') as w:
                    writer = csv.writer(w, lineterminator='\n')
                    for status in statuses:
                        writer.writerow((status.id, status.text.encode("utf-8")))
                tweetIds = []

tweetId = ["567692604976820224"]
statuses = api.statuses_lookup(tweetId)
with codecs.open("./MixedTweet.csv", 'a', encoding='utf-8') as w:
    writer = csv.writer(w, lineterminator='\n')
    text = statuses[0].text
    tokens = text.split()
    for word in tokens:
        try:
            word.encode('ascii')
        except UnicodeEncodeError:
            t_text = t.transliterate(text, "hi_IN")
            print("Non-Latin", t_text)
        else:
            print("Latin")
    #writer.writerow((statuses[0].id, statuses[0].text))