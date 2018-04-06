from collections import defaultdict, Counter
import csv
import os, sys, re
import ast

#read  from the tweet file and hash on tweet id
def load_data(tweetFile):
    tweetHash = {}
    with open(tweetFile) as f:
        for tweet in f.readlines():
            key,value = tweet.split(",",1)
            value = value.strip("b \' \" \n")
            tweetHash[key] = value
    return tweetHash

if __name__=='__main__':
    data_folder_path = sys.argv[1]
    tweetFile = os.path.join(data_folder_path, "Tweets.csv")
    tweet_Hash = load_data(tweetFile)
    annotatedTweetFile = os.path.join(data_folder_path, "AnnotatedTweets.csv")
    cntHI = Counter()
    cntEN = Counter()
    with open(annotatedTweetFile) as f:
        for tweetAnnotation in f.readlines():
            tweetTokens = tweetAnnotation.split(",")
            tweetId = tweetTokens[0]
            sentenceLabel = tweetTokens[1] #ignored for now
            tweetAnnotation = tweetTokens[2:-1]
            if tweetId in tweet_Hash:
                for wordAnnot,word in zip(tweetAnnotation, tweet_Hash.get(tweetId).split(" ")):
                    wordStart,wordEnd,wordType,phraseType = wordAnnot.split(":")
                    if wordType == "HI":
                        cntHI[word] += 1
                    elif wordType == "EN":
                        cntEN[word] += 1

    with open(os.path.join(data_folder_path, "TopHI.txt"), "w") as w:
        for topHI,val in cntHI.most_common():
            w.write("{}\n".format(topHI))

    with open(os.path.join(data_folder_path, "TopEN.txt"), "w") as w:
        for topEN,val in cntEN.most_common():
            w.write("{}\n".format(topEN))
