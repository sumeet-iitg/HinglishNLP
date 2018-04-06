import tweepy
import csv
import sys
import time

consumer_key= '0FwPy04vOpzNdi7CCEXEnDmSI'
consumer_secret = 'bPtFRye33nemEk9uMvTS97QLDHTTDtWunrLoKNHZeBLE1qaKsC'
auth_token = '175123301-g3NCDkOX6GPhMTha8wnPquSZGvNUChPSZRMX5M4h'
auth_token_secret = '8NknUXUXHDkl86sYEuYC2jBYVSRRqZSwvedgFESw7pfPE'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(auth_token, auth_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
tweetIds = []
with open("C:/Users/Sumeet Singh/Documents/Code-Mixed/EMNLPUserDataSet.csv", 'r') as f:
    reader = csv.reader(f)
    currentuserid = ""
    for tweet in reader:
        # tweet annotation TweetId, English,
        if currentuserid == "":
            currentuserid = tweet[0]
        userSeqId = tweet[0]
        if userSeqId != currentuserid or tweetIds.__len__() == 100:
            successDownload = False
            if tweetIds.__len__() > 0:
                while not successDownload:
                    try:
                        statuses = api.statuses_lookup(tweetIds)
                        successDownload = True
                    except tweepy.TweepError:
                        print("Encountered Tweepy error... sleeping for 300")
                        time.sleep(60 * 5)
                filePath = 'C:/Users/Sumeet Singh/Documents/Code-Mixed/User_{0}.csv'.format(currentuserid)
                with open(filePath, 'a') as w:
                    writer = csv.writer(w, lineterminator='\n')
                    for status in statuses:
                        writer.writerow((status.id, status.text.encode("utf-8")))
            tweetIds = []
            currentuserid = userSeqId
        tweetIds.append(tweet[1])
