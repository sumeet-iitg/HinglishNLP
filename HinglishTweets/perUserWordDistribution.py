from collections import defaultdict, Counter
import csv
import os, sys, re
import ast
import numpy as np

#read  from the tweet file and hash on tweet id
def load_data(tweetFile):
    tweetHash = {}
    with open(tweetFile) as f:
        for tweet in f.readlines():
            key,value = tweet.split(",",1)
            value = value.strip("b \' \" \n")
            tweetHash[key] = value
    return tweetHash

def compute_burstiness(languageSpan): #input is a dictionary
    burstiness = -2
    if len(languageSpan) > 0:
        spanLenArr = np.array(list(languageSpan.values()))
        meanSpan = np.mean(spanLenArr)
        stddevSpan = np.std(spanLenArr)
        burstiness = (stddevSpan - meanSpan)/(float)(stddevSpan + meanSpan)
    return burstiness

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

# def computeM_Index(languageCounts):
#     p_SqrSum = 0
#     totalCount = sum(languageCounts)
#     for count in languageCounts:
#         p = count/float(totalCount)
#         p_SqrSum += (p*p)
#     m_index = (1 + p_SqrSum)/(len(languageCounts) - 1)*

if __name__=='__main__':
    data_folder_path = sys.argv[1]
    user_tweet_folder_path = sys.argv[2]
    user_tweet_stats_folder_path = sys.argv[3]
    annotatedTweetFile = os.path.join(data_folder_path, "EMNLPAnnotatedUserDataSet.csv")
    with open(annotatedTweetFile) as f:
        skipUserId = ""
        currentUserId = ""
        cntHI = Counter()
        cntEN = Counter()
        cntOT = Counter()
        spanHI = Counter()
        spanEN = Counter()
        cntTot = 0
        tweet_Hash = {}
        userHIFile = ""
        userENFile = ""
        userOTFile = ""
        userStatFile = ""
        for tweetAnnotation in f.readlines():
            tweetTokens = tweetAnnotation.split(",")
            userId = tweetTokens[0]
            if userId == skipUserId: continue
            # looking at a different user now
            # persist last user's stats
            # open new user's tweet, refresh tweet hash and word counters
            if not userId == currentUserId:
                if not cntTot == 0: #in this case we've got no stats to write
                    userHIFile = os.path.join(user_tweet_stats_folder_path, userId + "_TopHI.txt")
                    userENFile = os.path.join(user_tweet_stats_folder_path, userId + "_TopEN.txt")
                    userOTFile = os.path.join(user_tweet_stats_folder_path, userId + "_TopOTHER.txt")
                    userStatFile = os.path.join(user_tweet_stats_folder_path, userId + "_Metrics.txt")
                    burstinessEN = compute_burstiness(spanEN)
                    burstinessHI = compute_burstiness(spanHI)
                    with open(userStatFile, "w") as w:
                        w.write("TotalCount:{0}, CountEN:{1}, CountHI:{2}, CountOT:{3} \n"
                                .format(cntTot,sum(cntEN.values()), sum(cntHI.values()), sum(cntOT.values())))
                        w.write("BurstinessHI:{0}, BurstinessEN:{1} \n"
                                .format(burstinessHI,burstinessEN))
                    with open(userHIFile, "w") as w:
                        for topHI, val in cntHI.most_common():
                            w.write("{}\n".format(topHI))
                    with open(userENFile, "w") as w:
                        for topEN, val in cntEN.most_common():
                            w.write("{}\n".format(topEN))
                userTweetFile = os.path.join(user_tweet_folder_path, "User_" + userId + ".csv")
                if not os.path.isfile(userTweetFile) or os.stat(userTweetFile).st_size == 0:
                    skipUserId = userId
                    continue
                currentUserId = userId
                tweet_Hash = load_data(userTweetFile) #dictionary indexed by tweet id
                cntHI = Counter()
                cntEN = Counter()
                cntOT = Counter()
                spanEN = Counter()
                spanHI = Counter()
                cntTot = 0
            tweetId = tweetTokens[1]
            sentenceLabel = tweetTokens[2] #overall sentence label, ignored for now
            tweetAnnotation = tweetTokens[3:-1]
            if tweetId in tweet_Hash:
                prevWordType = ""
                spanLength = 0 # number of continuous words in one language
                for wordAnnot,word in zip(tweetAnnotation, tweet_Hash.get(tweetId).split(" ")):
                    wordStart,wordEnd,wordType,phraseType = wordAnnot.split(":")
                    if is_ascii(word): #exclude unicode devanagri words
                        if prevWordType == wordType:
                            spanLength += 1
                        else:
                            if prevWordType == "HI":
                                spanHI[spanLength] += 1
                            elif prevWordType == "EN":
                                spanEN[spanLength] += 1
                            elif prevWordType == "":
                                prevWordType = wordType
                            spanLength = 1
                        cntTot += 1
                        if wordType == "HI":
                            cntHI[word] += 1
                        elif wordType == "EN":
                            cntEN[word] += 1
                        elif wordType == "OTHER":
                            cntOT[word] += 1
                    else:
                        print("Unicode encountered")
                if prevWordType == "HI":
                    spanHI[spanLength] += 1
                elif prevWordType == "EN":
                    spanEN[spanLength] += 1