from sklearn.cluster import KMeans
import numpy as np
import csv
import os, sys, re
import ast
import matplotlib.pyplot as plt
import shutil
import decimal

def getPercentages(read_line):
    user_stat_tokens = read_line.split(",")
    total = float(user_stat_tokens[0].split(":")[1])
    totalEN = round(float(user_stat_tokens[1].split(":")[1]) * 100 / total, 2)
    totalHI = round(float(user_stat_tokens[2].split(":")[1]) * 100 / total, 2)
    totalOT = round(float(user_stat_tokens[3].split(":")[1]) * 100 / total, 2)
    dataPoint = [totalEN, totalHI, totalOT]
    return dataPoint

def getBurstiness(read_line):
    user_stat_tokens = read_line.split(",")
    burstHI = round(float(user_stat_tokens[0].split(":")[1]), 2)
    burstEN = round(float(user_stat_tokens[1].split(":")[1]), 2)
    dataPoint = [burstEN, burstHI]
    return dataPoint

#load the usage patterns as 2-D objects Hindi % vs English %
if __name__=='__main__':
    user_data_folder_path = sys.argv[1]
    usagePercentPoints = []
    userBurstiness = dict()
    usageToUserDict = dict()
    burstinessToUserDict = dict()
    for filename in os.listdir(user_data_folder_path):
        if "Metrics" in filename:
            userId = os.path.splitext(filename)[0].split("_")[0]
            with open(os.path.join(user_data_folder_path, filename), "r") as r:
                readLines = 0
                for user_stats in r.readlines():
                    if readLines == 0:
                        dataPoint = getPercentages(user_stats)
                        usagePercentPoints.append([dataPoint[0], dataPoint[1]])
                        key = str(dataPoint[0]) + "_" + str(dataPoint[1])
                        userIdList = [userId]
                        if key in usageToUserDict:
                            usageToUserDict[key].append(userId)
                        else:
                            usageToUserDict[key] = userIdList
                    elif readLines == 1:
                        dataPoint = getBurstiness(user_stats)
                        # userBurstiness.append(dataPoint)
                        # key = str(dataPoint[0]) + "_" + str(dataPoint[1])
                        # userIdList = [userId]
                        # if key in burstinessToUserDict:
                        #     burstinessToUserDict[key].append(userId)
                        # else:
                        #     burstinessToUserDict[key] = userIdList
                        userBurstiness[userId] = dataPoint
                    else: break
                    readLines +=1
    X = np.array(usagePercentPoints)
    estimator = KMeans(n_clusters=10, init='k-means++', n_init=10, max_iter=300, tol=0.0001, precompute_distances='auto',
                       verbose=0, random_state=None, copy_x=True, n_jobs=1, algorithm='auto')
    estimator.fit(X)

    # Y = np.array(userBurstiness)
    # estimatorY= KMeans(n_clusters=10, init='k-means++', n_init=10, max_iter=300, tol=0.0001, precompute_distances='auto',
    #                    verbose=0, random_state=None, copy_x=True, n_jobs=1, algorithm='auto')
    # estimatorY.fit(Y)
    #clusteredUsers = {i: X[np.where(estimator.labels_ == i)] for i in range(estimator.n_clusters)}

    # centroids = {}
    # for clusterId in range(estimator.n_clusters):
    #     clusterCenter = estimator.cluster_centers_[clusterId]
    #     centroids[clusterId] = [clusterCenter]
        # plt.plot(clusterCenter[0], clusterCenter[1], 'o')
        # newpath = os.path.join(user_data_folder_path, "Cluster_" + str(clusterId) + "_" + str(clusterCenter[0])+ "," + str(clusterCenter[1]))
        # if not os.path.exists(newpath): os.makedirs(newpath)
        # #print("ClusterId={0}\n", clusterId)
        # for usageKey in X[np.where(estimator.labels_ == clusterId)]:
        #     #print("{0}\n".format(usageKey))
        #     usageKeyStr = str(usageKey[0]) + "_" + str(usageKey[1])
        #     if usageKeyStr in usageToUserDict:
        #         for userId in usageToUserDict[usageKeyStr]:
        #             enCountFilePath = os.path.join(user_data_folder_path, userId +"_TopEN.txt")
        #             hiCountFilePath = os.path.join(user_data_folder_path, userId +"_TopHI.txt")
        #             statsFilePath = os.path.join(user_data_folder_path, userId + "_Metrics.txt")
        #             shutil.copy2(enCountFilePath, newpath)
        #             shutil.copy2(hiCountFilePath, newpath)
        #             shutil.copy2(statsFilePath, newpath)
    #Plot the results
    clusterLabels = []
    for i in set(estimator.labels_):
        index = estimator.labels_ == i
        clusterLabel = "Cluster_" + str(i)
        clusterLabels.append(clusterLabel)
        plt.plot(X[index, 0], X[index, 1], 'o')
        newpath = os.path.join(user_data_folder_path, clusterLabel)
        if not os.path.exists(newpath): os.makedirs(newpath)
        for usageKey in X[np.where(estimator.labels_ == i)]:
            usageKeyStr = str(usageKey[0]) + "_" + str(usageKey[1])
            if usageKeyStr in usageToUserDict.keys():
                #plt.annotate(i, xy=(usageKey[0], usageKey[1]), arrowprops=dict(facecolor='black'))
                userId = usageToUserDict[usageKeyStr][0]
                if userId in userBurstiness.keys():
                    print("Cluster ID: ", i ," BEn: ", userBurstiness[userId][0], "\t BHi: ", userBurstiness[userId][1])
                    break
        for usageKey in X[np.where(estimator.labels_ == i)]:
            usageKeyStr = str(usageKey[0]) + "_" + str(usageKey[1])
            if usageKeyStr in usageToUserDict.keys():
                for userId in usageToUserDict[usageKeyStr]:
                    enCountFilePath = os.path.join(user_data_folder_path , userId +"_TopEN.txt")
                    hiCountFilePath = os.path.join(user_data_folder_path, userId +"_TopHI.txt")
                    statsFilePath = os.path.join(user_data_folder_path, userId + "_Metrics.txt")
                    shutil.copy2(enCountFilePath, newpath)
                    shutil.copy2(hiCountFilePath, newpath)
                    shutil.copy2(statsFilePath, newpath)

    # for centroid in estimator.cluster_centers_:
    #     plt.annotate(str("c"), xy=(centroid[0],centroid[1]), arrowprops=dict(arrowstyle="->"))
    plt.xlabel("English %")
    plt.ylabel("Hindi %")
    plt.legend(clusterLabels)
    plt.title("Hindi vs English Usage%")
    plt.show()
    # for i in set(estimatorY.labels_):
    #     index = estimatorY.labels_ == i
    #     plt.plot(Y[index, 0], Y[index, 1], 'o', label="Cluster_"+str(i))
    # TODO