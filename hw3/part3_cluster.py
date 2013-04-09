import sys
import os
import re
from collections import defaultdict
import cmd
import json
from pprint import pprint 
import math
import random
import requests

class HelloWorld(cmd.Cmd):
    """Simple command processor example."""
    actualTweets = defaultdict()  # {tweetID : tweet text}
    whoTweeted = defaultdict()    # {tweetID : userID  }
    termFreq = defaultdict(lambda:defaultdict()) # {word : {1:2 }}
    idfList = defaultdict(set)
    idf = defaultdict()
    UIDtoScreenName = defaultdict()     # {ID: screen_name}
    tfIdfWeight = defaultdict(lambda:defaultdict()) # {document : {word : tf-idf }}
    into_links = defaultdict(set) # {word : {1:2 }}
    outOf_links = defaultdict(set) # {word : {1:2 }}
    allUsers_set = set()
    pageRankUsers = defaultdict()   # {userID, pageRank}
    topics = set()
    assignedClass = defaultdict()   # { docID , query }
    assignedCluster = defaultdict()   # { docID , query }
    initCentroids = list()    # list of the random initial centroids
    query1 = ""
    query2 = ""
    query3 = ""
    query4 = ""
    query5 = ""
 
    def do_myTests(self,ter):
        filename= "bingOP.txt"
        fr = open(filename)
        request5 = 'https://user:tDPxzhwtkNX2hYu72irEhlPpFzg36bAcsX3fqbRiGS4=@api.datamarket.azure.com/Bing/Search/News?Query=%27dallas%20mavericks%27&$format=json&'
        query5 = "dallas mavericks"
        self.bingRequest(request1,query5, 'a');
       
    def do_test(self,asgbtrh):
        """
        A dummy function to test small pieces of code
        """
        testList=[(1,2),(3,4),(5,6)]
        asd = [1]*6
        #print sum(asd)
        qwe = [1.0]*64
        #for i in range(0,6):
          #print qwe[i]
        #print [i-j for i,j in zip(asd ,qwe)]
        mypageRank = defaultdict()  # {userID : PR}   normalized
        minValPR = min(self.pageRankUsers.values())
        maxValPR = max(self.pageRankUsers.values())
        for user in self.pageRankUsers:
          mypageRank[user] = (self.pageRankUsers[user]-minValPR)/(maxValPR-minValPR)  # normalize pagerank values
        #print self.pageRankUsers['16692597']
        #print mypageRank['16692597']

    def do_intermediateTest(self,apfoitjhmno):
        fr = open("bing_all_OP.txt", 'r')
        fw = open("bing_all_OP1.txt", 'w')
        lines = fr.readlines()
        count = 1
        for line in lines: 
          if count <=30:
            line = line + " === " + self.query1
          elif count >30 and count <=60:
            line = line + " === " + self.query2
          elif count >60 and count <=90:
            line = line + " === " + self.query3
          elif count >90 and count <=120:
            line = line + " === " + self.query4
          elif count >120 and count <=150:
            line = line + " === " + self.query5
          count +=1
          fw.write(line)
          fw.write('\n')

        fw.close()
        fr.close()

   
    def bingRequest(self,req,query, fileMode ):
        r = requests.get(req + '$skip=0')
        json_data=json.loads(r.text)
        rawResultsList = json_data['d']['results']

        fw = open("bing_all_OP.txt", fileMode)
        queryFile = open("bing_OP_"+query, 'w')
        for result in rawResultsList:
          resultText = result['ID']+" === "+result['Title']+" === "+result['Description']
          queryResultText = result['ID']+" === "+result['Title']+" === "+result['Description']
          queryFile.write(queryResultText.encode('utf8'))
          queryFile.write('\n')
          fw.write(resultText.encode('utf8'))
          fw.write("\n")
        r = requests.get(req + '$skip=15')
        json_data=json.loads(r.text)
        rawResultsList = json_data['d']['results']
        for result in rawResultsList:
          resultText =result['ID']+" === "+ result['Title']+" === "+result['Description']
          queryResultText = result['ID']+" === "+result['Title']+" === "+result['Description']
          queryFile.write(queryResultText.encode('utf8'))
          queryFile.write('\n')
          fw.write(resultText.encode('utf8'))
          fw.write("\n")
        fw.close()
        queryFile.close()

    def do_callBingAPI(self, arbit):
        request1 = 'https://user:tDPxzhwtkNX2hYu72irEhlPpFzg36bAcsX3fqbRiGS4=@api.datamarket.azure.com/Bing/Search/News?Query=%27texas%20aggies%27&$format=json&'
        request2 = 'https://user:tDPxzhwtkNX2hYu72irEhlPpFzg36bAcsX3fqbRiGS4=@api.datamarket.azure.com/Bing/Search/News?Query=%27texas%20longhorns%27&$format=json&'
        request3 = 'https://user:tDPxzhwtkNX2hYu72irEhlPpFzg36bAcsX3fqbRiGS4=@api.datamarket.azure.com/Bing/Search/News?Query=%27duke%20blue%20devils%27&$format=json&'
        request4 = 'https://user:tDPxzhwtkNX2hYu72irEhlPpFzg36bAcsX3fqbRiGS4=@api.datamarket.azure.com/Bing/Search/News?Query=%27dallas%20cowboys%27&$format=json&'
        request5 = 'https://user:tDPxzhwtkNX2hYu72irEhlPpFzg36bAcsX3fqbRiGS4=@api.datamarket.azure.com/Bing/Search/News?Query=%27dallas%20mavericks%27&$format=json&'
        self.query1 = "texas aggies"
        self.query2 = "texas longhorns"
        self.query3 = "duke blue devils"
        self.query4 = "dallas cowboys"
        self.query5 = "dallas mavericks"

        self.bingRequest(request1, self.query1, 'w');
        self.bingRequest(request2, self.query2, 'a');
        self.bingRequest(request3, self.query3, 'a');
        self.bingRequest(request4, self.query4, 'a');
        self.bingRequest(request5, self.query5, 'a');


            
    def do_parseFile(self,asdfrtg):
        """
        Parse the entire tweet corpus for tf-idf and for pagerank [Run this command first before running any other command]
        """
        self.query1 = "texas aggies"
        self.query2 = "texas longhorns"
        self.query3 = "duke blue devils"
        self.query4 = "dallas cowboys"
        self.query5 = "dallas mavericks"


        print "Parsing file.. please wait.."
        fr=open('bing_all_OP.txt','r')
        lines = fr.readlines()
        numDocs=float(len(lines))
        into = defaultdict(set) # {word : {1:2 }}
        outOf = defaultdict(set) # {word : {1:2 }}
        allUsers = set()
        #retweetCount = defaultdict() # {tweetID : num of retweets}
        idf = defaultdict()

        #numDocs = 4.0
        for line in lines:
        #for i in range(0,4):
          #json_data=json.loads(line)
          json_data = re.split(' === |\n', line, flags = re.UNICODE)
          rawTweetText = json_data[1] + " === " + json_data[2] + " === " + json_data[3]

          tweetID = json_data[0]
          #print "for assigned class: ",json_data[0] , " , " ,json_data[3]
          self.assignedClass[json_data[0]] = json_data[3]
          #print "raw tweetText: " , rawTweetText
          #print "tweetID: ", tweetID

          """
          tweetID = json_data['id']
          userScreenName = json_data['user']['screen_name']
          retweetCount = json_data['retweet_count']
          numDocs += retweetCount 
          self.UIDtoScreenName[userID] = userScreenName
          self.whoTweeted[tweetID] = userID
          """

          tweetText = re.split('[\W]+',rawTweetText,flags=re.UNICODE)
          #mentions = json_data['entities']['user_mentions']

          #allUsers.add(userID)
          self.actualTweets[tweetID] =rawTweetText 
          words = tweetText
          docTermFreq = defaultdict()
          for word in words:
            word = word.lower()
            self.idfList[word].add(tweetID)
            # """
            if word in idf:
              idf[word] = idf[word]+1
            else:
              idf[word] = 1
            # """
            if word in docTermFreq:
              docTermFreq[word] = docTermFreq[word]+1
            else:
              docTermFreq[word] = 1
          
          self.termFreq[tweetID]=docTermFreq
          #print "term frequency of ", tweetID, " is : ",self.termFreq[tweetID]
        #print len(self.idf)
        for word in self.idfList:
          self.idf[word] = math.log(numDocs/(idf[word]),2)
          self.idf[word] = math.log(numDocs/len(self.idfList[word]),2)
          if self.idf[word] < 0:
            print "idf: ", self.idf[word], word , " " , idf[word]

        #print self.idf['mars']
        for doc in self.termFreq:
          sumNorm=0
          for word in self.termFreq[doc]:
            if self.termFreq[doc][word] > 0:
              self.termFreq[doc][word] = 1 + math.log(self.termFreq[doc][word] ,2)
            else:
              self.termFreq[doc][word] = 0
            self.tfIdfWeight[doc][word] = self.termFreq[doc][word]*self.idf[word]

          for word in self.tfIdfWeight[doc]:
            sumNorm = sumNorm + self.tfIdfWeight[doc][word]*self.tfIdfWeight[doc][word]
          for word in self.tfIdfWeight[doc]:
            self.tfIdfWeight[doc][word] /=  float(math.sqrt(sumNorm))


        fr.close()
        #fw.close()
        #print self.tfIdfWeight
        """
        print "Calculating page rank....... "
        self.do_part2(self)
        """

    def findDistance(self, ptA , cent):
          """
          finds cosine similarity as between pt A and pt B
          Assumes ptA and ptB are both normalized
          """
          value=0
          commonTerms = set()
          commonTerms = set(self.tfIdfWeight[ptA].keys()).intersection(set(cent))
          for word in commonTerms:
            value = value + self.tfIdfWeight[ptA][word]*cent[word]
            #print word
          return value
    #def calculateRSS(self, ):

    def do_runKmeans(self, K):
        """ 
        This file calls kMeans function with the desired value of K
        """
        #for k in range(2,10):
        minRange = 0
        maxRange = 10
        for k in range(3,9):
          print "*******************************************  Running k-means for k = ", k ,"************************************************************"
          maxPurity = 0
          avgPurity = 0
          avgRI = 0
          maxRI = 0
          maxRSS = 0
          bestList = []
          avgRSS = 0
          for i in range(minRange,maxRange):
            (val,RI,RSS , initCentroids) = self.kMeans(k,0)
            avgRSS += RSS
            avgPurity += val
            avgRI += RI
            if val > maxPurity:
              maxPurity = val
              maxRI = RI
              maxRSS = RSS
              bestList = initCentroids
          self.initCentroids = bestList   # set the class's random initial centroids to the best result's random initialization
          
          # if the above line is commented, then the self.initCentroids will already have the centroids from the prev value
          (val,RI,RSS , initCentroids) = self.kMeans(k,1)
          print "\n\n \n For K = ",k,", purity = ", avgPurity/float(maxRange-minRange+1), ", RI : ", avgRI/float(maxRange-minRange+1), ", RSS: ", avgRSS/float(maxRange-minRange+1)
          (val,RI,RSS , initCentroids) = self.kMeans(k,1)

          print "\n For K = ",k,", modified cluster:  purity = ", val, ", RI : ", RI, ", RSS: ", RSS

    def findEucledianDist(self, ptA, cent):
          """
          finds eucledian distance as between pt A and pt B
          Assumes ptA and ptB are both normalized
          """
          value=0
          commonTerms = set()
          commonTerms = set(self.tfIdfWeight[ptA].keys()).union(set(cent.keys()))
          for word in commonTerms:
            if word in self.tfIdfWeight[ptA]:
              if word in cent:
                value += (cent[word]-self.tfIdfWeight[ptA][word] )*(cent[word]-self.tfIdfWeight[ptA][word] )
              else:
                value += (self.tfIdfWeight[ptA][word]*self.tfIdfWeight[ptA][word] )
            else:
              value += cent[word]*cent[word]
            #print word

          return (value)
  


    def kMeans(self,K , output):
        RSSprev = 1000000
        RSS = 0
        #K=5
        allDocuments = [item for item in self.tfIdfWeight]  # a list of all the documents 
        if output == 0:
          initialCentroids =  random.sample(allDocuments , K) # list of all initial centroids
        else:
          initialCentroids = self.initCentroids
        allClusters = defaultdict(list)

        RSS=0
        # calculate the initial clusters with the initial Centroids
        for doc in allDocuments:
          minVal=0 
          closestCentroid = ""
          for centroid in initialCentroids:
            if centroid == doc: 
              continue
            val = self.findDistance(doc, self.tfIdfWeight[centroid]) 
            if val > minVal:
              minVal = val
              closestCentroid = centroid

          allClusters[closestCentroid].append(doc)
          dist =  self.findEucledianDist(doc,self.tfIdfWeight[closestCentroid] )
          RSS = RSS + dist

        #print allClusters
        #print "initial RSS: " , RSS


        RSS = 0
        # create a flat list of lists from a dict of lists
        allClustersList = list()  # [ [list of 1st cluster points], [list of 2nd cluster points]... ]
        for centroid in allClusters:
          allClustersList.append(allClusters[centroid])

        #print allClustersList
        numIterations = 0

        while math.fabs( RSSprev - RSS ) > 0.0001:
          RSSprev = RSS
          numIterations +=1
          # recalculate the clusters and assign the RSSprev = RSS
          
          """
          calculate centroid of each cluster now
          I am creating a list of centroids corresponding to the list of clusters.
          So allClustersList will have all the clusters in different lists, and allClusterCentroids will have all corresponding centroids
          """
          allClusterCentroids = [0]*K
          for i in range(0, len(allClustersList)):
            cluster = allClustersList[i]    # each cluster points as a list
            centroid = defaultdict()
            numPoints = len(cluster)        # number of points in each cluster. This will be divided in the end after the centroid terms are added
          
            for point in cluster:
              pointTerms = self.tfIdfWeight[point]    # this will ideally contain {word1: tf-idf score, word2: tf-idf}
              for term in pointTerms:                 # for every word in the above dict, add it to the centroid's value
                if term in centroid:
                  centroid[term] += pointTerms[term]
                else:
                  centroid[term] = pointTerms[term]
              # normalize centroids
            sumNorm=0
            for term in centroid:
              centroid[term] = centroid[term]/float(numPoints)
              sumNorm += centroid[term]*centroid[term]
            for term in centroid:
              centroid[term] = centroid[term]/math.sqrt(sumNorm)
            bestCent=centroid
            """ mediod calculation
            minDist = 10000
            bestCent = defaultdict()
            for point in cluster:
              dist = self.findEucledianDist(point , centroid)
              if minDist > dist:
                minDist = dist
                bestCent = self.tfIdfWeight[point]

            #"""
            #print centroid


   

            allClusterCentroids[i] = bestCent
           
          #print allClusterCentroids[0]
          
          # calculate the new RSS and then perform the new clustering based on the new centroids 
          newAllClustersList = [[] for i in range(K)]  # this will store all the new clusters ... Data structure is similar to allClustersList
          #print newAllClustersList
          newClusterCentroids = []
          newClusterCentroids = [item for item in allClusterCentroids]
          
          #print "length of newClusterCentroids: " , newClusterCentroids
          RSS=0
          # calculate the initial clusters with the initial Centroids
          #print "allDocuments size: ", len(allDocuments)
          for doc in allDocuments:
            minVal=0 
            closestCentroidIndex = 0
            for i in range(0,len(newClusterCentroids)):
              centroid = newClusterCentroids[i]
              #if centroid == doc: 
              #  continue
              val = self.findDistance(doc, centroid) 
              #print 
              #print "val: ",val
              if val > minVal:
                minVal = val
                #print "minVal: ",minVal
                closestCentroidIndex = i
                              #print "closest index: ",closestCentroidIndex
            #print "final closest index: ",closestCentroidIndex
            #print "newAllClustersList: ",newAllClustersList[closestCentroidIndex]
            newAllClustersList[closestCentroidIndex].append(doc)
            dist =  self.findEucledianDist(doc,newClusterCentroids[closestCentroidIndex] )
            RSS = RSS + dist

            #x = input("press to continue")
          #print newAllClustersList
          
          #print "RSS new: " , RSS, "RSS old : ", RSSprev
          #print "clusters sizes: "
          #for i in range(0,K):
          #  print len(newAllClustersList[i]), " , "

          allClustersList = []
          for item in newAllClustersList:
            tmpList = []
            for ele in item: 
              tmpList.append(ele)
            allClustersList.append(tmpList)
          #allClustersList = newAllClustersList

        """ printing all the clusters here
        if output == 1:
          for i in range(0,len(newAllClustersList)):
            cluster = newAllClustersList[i]
            print "\n\n\ncluster ", i , " : number of documents in this cluster: " ,len(cluster) 
            for ID in cluster:
              text = re.split(' === |\n ', self.actualTweets[ID], flags = re.UNICODE)
              #print len(text)
              print text[2], " : ", text[0]
        #"""


        #print "====================================  Calculating Purity: ======================================="
        self.initCentroids = []
        for cluster in allClustersList:
          somePt = random.sample(cluster , 1)
          self.initCentroids.append(somePt[0])
        #print "self.initCentroids : ",self.initCentroids
        #print "initial Centroids : ",initialCentroids


        purity = 0
        for i in range(0,len(newAllClustersList)):
          cluster = newAllClustersList[i]
          purityScale = defaultdict()
          for item in cluster:
            text = re.split(' === |\n', self.actualTweets[item], flags = re.UNICODE)
            word = text[2]
            self.assignedCluster[item] = i
            if word in purityScale:
              purityScale[word] += 1
            else:
              purityScale[word] = 1
          maxVal = 0
          #print purityScale

          for item in purityScale:
            if purityScale[item] > maxVal:
              maxVal = purityScale[item]
          #print maxVal
          purity += maxVal
        
        purityPercent =  100*purity/float(len(allDocuments))


        #print "====================================  Calculating RI: ======================================="
        TP=0
        FN=0
        FP=0
        TN=0

        for doc1 in allDocuments:
          for doc2 in allDocuments:
            #print "d1 class: ",self.assignedClass[doc1] , " d2 class: ",self.assignedClass[doc2] 
            #print "d1 cluster: ",self.assignedCluster[doc1] , " d2 cluster: ",self.assignedCluster[doc2] 

            if self.assignedClass[doc1] == self.assignedClass[doc2]:
              if self.assignedCluster[doc1] == self.assignedCluster[doc2]:
                TP +=1
              else:
                FN +=1
            elif self.assignedClass[doc1] != self.assignedClass[doc2] :
              if self.assignedCluster[doc1] == self.assignedCluster[doc2]:
                FP +=1
              else:
                TN +=1
            #y = input("enter")

        #print "TP: ", TP , ' TN: ', TN, ' FP: ', FP, ' FN: ', FN
        RI = (TP+TN)/float(TP+TN+FP+FN)
        #if output == 1:
          #print "purity percent: ",purityPercent, "% , RI: ", RI," RSS: ", RSS, " number of iterations to converge: ", numIterations
        #self.initCentroids = newClusterCentroids



        
        print "purity percent: ",purityPercent, "% , RI: ", RI," RSS: ", RSS, " number of iterations to converge: ", numIterations
        return (purityPercent, RI, RSS, initialCentroids)




        







    def do_part3(self,aohudskvhfcjfjh):
        """
        Enter a query to search using tf-idf and then apply pageRank to influence the result. Run Parsefile command before running this command
        """
        q=raw_input("Enter a query: ")

        queryWeight = defaultdict()

        queryText = re.split('[\W]+',q,flags=re.UNICODE)
        #print queryText
        idfkeys = self.idf.keys()
        queryTermFreq = defaultdict()
        for word in queryText:
          word = word.lower()
          if word not in idfkeys:
            print "query word ",word," is not found in the tweet corpus"
            return
          if word in queryTermFreq:
            queryTermFreq[word] = queryTermFreq[word]+1.0
          else:
            queryTermFreq[word] = 1.0
        #print queryTermFreq
        sumNorm=0
        for word in queryTermFreq:
          if queryTermFreq[word] > 0:
            queryTermFreq[word] = 1 + math.log(queryTermFreq[word] ,2)
          else:
            queryTermFreq[word] = 0
          queryWeight[word] = queryTermFreq[word] * self.idf[word]
          sumNorm = sumNorm + queryWeight[word]*queryWeight[word]
        for word in queryWeight:
          queryWeight[word]= queryWeight[word]/math.sqrt(sumNorm)

        #print queryWeight
        resultSet = defaultdict()
        for doc in self.tfIdfWeight:
          value=0
          commonTerms = set()
          commonTerms = set(queryWeight.keys()).intersection(set(self.termFreq[doc]))
          for word in commonTerms:
            value = value + queryWeight[word]*self.tfIdfWeight[doc][word]
            #print word
          if len(commonTerms)>0:  
            resultSet[doc]=value
          #print (doc,value)

        """
        sumToNorm = sum(resultSet.values())
        print "sumToNorm: ", sumToNorm
      
        for user in resultSet:
          resultSet[user] = resultSet[user]/sumToNorm
        """

        properUsers = set((set(self.outOf_links.keys())|set(self.into_links.keys())))
        deletedUsers = set(set(self.allUsers_set)-set(properUsers))

        minValTFIDF = min(resultSet.values())
        maxValTFIDF = max(resultSet.values())
 
        mypageRank = defaultdict()  # {userID : PR}   normalized
        minValPR = min(self.pageRankUsers.values())
        maxValPR = max(self.pageRankUsers.values())
        for user in self.pageRankUsers:
          mypageRank[user] = (self.pageRankUsers[user]-minValPR)/(maxValPR-minValPR)  # normalize pagerank values

        for user in deletedUsers:
          mypageRank[user] = 0.0

        #print "lenth of PR : ",len(mypageRank) , len(self.pageRankUsers) 
        myresultSet = defaultdict()
        for doc in resultSet:
          myresultSet[doc] = (resultSet[doc]-minValTFIDF)/(maxValTFIDF-minValTFIDF)     # normalize TF-IDF values
 
        prKeys = mypageRank.keys()
        for alpha in [0.8]:
          myresultSet1 = defaultdict()
          myresultSet1 = myresultSet 
          #alpha = 0.3
          print "printing with formula: [alpha*tweetResults + (1-alpha)*pagerank ] with alpha as ", alpha
         
           #actual technique of merging pagerank score of user to his tweet
          for doc in resultSet:
            #print doc
            userid = self.whoTweeted[doc]
            #if userid in prKeys:
            myresultSet1[doc] = (alpha)*myresultSet[doc] + (1.0-alpha)*mypageRank[userid]
            #else:
            #  myresultSet[doc] = 0.0
          #print "out of loop"
          results=[(key,val) for key, val in sorted(myresultSet1.iteritems(), key=lambda (k,v): (v,k))]
          #print len(results),"Results found"
          finalResultsSorted=results[-50:]
          finalResultsSorted.reverse()
          #print finalResultsSorted
          L = len(finalResultsSorted)
          for key in range(0,L):
            print "tweetID: ",finalResultsSorted[key][0],"Tweet: ",self.actualTweets[finalResultsSorted[key][0]]," User: ",self.UIDtoScreenName[self.whoTweeted[finalResultsSorted[key][0]]]

    def do_part1(self,lineadfsggh):
        """
        Enter a query to search using tf-idf and finding the cosine 
        """
        q=raw_input("Enter a query: ")

        queryWeight = defaultdict()

        queryText = re.split('[\W]+',q,flags=re.UNICODE)
        #print queryText
        idfkeys = self.idf.keys()
        queryTermFreq = defaultdict()
        for word in queryText:
          if word not in idfkeys:
            print "query word ",word," is not found in the tweet corpus"
            return
          word = word.lower()
          if word in queryTermFreq:
            queryTermFreq[word] = queryTermFreq[word]+1.0
          else:
            queryTermFreq[word] = 1.0
        #print queryTermFreq
        sumNorm=0
        for word in queryTermFreq:
          if queryTermFreq[word] > 0:
            queryTermFreq[word] = 1 + math.log(queryTermFreq[word] ,2)
          else:
            queryTermFreq[word] = 0
          queryWeight[word] = queryTermFreq[word] * self.idf[word]
          sumNorm = sumNorm + queryWeight[word]*queryWeight[word]
        for word in queryWeight:
          queryWeight[word]= queryWeight[word]/math.sqrt(sumNorm)

        print queryWeight
        resultSet = defaultdict()
        for doc in self.tfIdfWeight:
          value=0
          commonTerms = set()
          commonTerms = set(queryWeight.keys()).intersection(set(self.termFreq[doc]))
          for word in commonTerms:
            value = value + queryWeight[word]*self.tfIdfWeight[doc][word]
            #print word
          if len(commonTerms)>0:  
            resultSet[doc]=value
          #print (doc,value)

        sumToNorm = sum(resultSet.values())
        #print "sumToNorm: ", sumToNorm
      
        print initialCentroids
        for user in resultSet:
          resultSet[user] = resultSet[user]/sumToNorm

       
        results=[(key,val) for key, val in sorted(resultSet.iteritems(), key=lambda (k,v): (v,k))]
        #print len(results),"Results found"
        finalResultsSorted=results[-50:]
        finalResultsSorted.reverse()
        #print finalResultsSorted
        for key in range(0,len(finalResultsSorted)):
          print "TweetID: ",finalResultsSorted[key][0],"Tweet: ",self.actualTweets[finalResultsSorted[key][0]]," User: ",self.UIDtoScreenName[self.whoTweeted[finalResultsSorted[key][0]]]




    def do_part2(self,qwertrgrvm):
      """
      Performs a page ranking on the users [run the parseFile command before running this command]     
      """
      
      into = self.into_links # {word : {1:2 }}
      outOf = self.outOf_links  # {word : {1:2 }}
      allUsers = self.allUsers_set
      
      #### Page rank algorithm

      print len(self.UIDtoScreenName)

      properUsers = set((set(outOf.keys())|set(into.keys())))
      oldUserToPR = defaultdict(float)
      newUserToPR = defaultdict(float)
      for user in properUsers:
        oldUserToPR[user]=1.0
        newUserToPR[user]=1.0
    
      d = 0.1
      N= len(properUsers)
      breakLimit = 0.01
      iterEle=0
      while True:
        iterEle+=1
        #print "At iteration: ", iterEle
        for user in newUserToPR:
          #degree = float(len(outOf[user]))
          #print "degree" , degree , "len of out user:", len(outOf[user])
          #if degree ==0.0:
           # continue
          valSum =0.0
          for inUser in into[user]:
            degree = float(len(outOf[inUser]))
            valToSplit = oldUserToPR[inUser]/degree
            valSum = valSum+valToSplit
           
          #print "val to split: " , valToSplit
          newUserToPR[user] =d+ (1.0-d)*valSum
          """
          for outUser in outOf[user]:
            newUserToPR[outUser] = (1.0-d)*(oldUserToPR[outUser] + valToSplit) + d
          """
        
        diffPR = [float(j-i) for i,j in zip(oldUserToPR.values() ,newUserToPR.values())] 
        """
        #print diffPR
        print "old values: ",oldUserToPR.values()
        print "new values: ",newUserToPR.values()
        print
        #"""
        if all([math.fabs(indivPR) <= breakLimit for indivPR in diffPR ]) or iterEle>=500: 
          break
        #oldUserToPR=newUserToPR

        for user in newUserToPR:
          oldUserToPR[user] = newUserToPR[user]

        #sumToNorm = sum(newUserToPR.values())
        #print "sumToNorm: ", sumToNorm

      # sort PR and print
      #print "out of the loop\n"
  
      sumToNorm=0.0

      sumToNorm = sum(newUserToPR.values())
      #print "sumToNorm: ", sumToNorm
      
      for user in newUserToPR:
        newUserToPR[user] = newUserToPR[user]/sumToNorm

      sortedUsersByPR=[(key,val) for key, val in sorted(newUserToPR.iteritems(), key=lambda (k,v): (v,k))]
      #print len(sortedUsersByPR),"Length of sorted users after PR"
      finalResultsSorted=sortedUsersByPR[-50:]
      L = len(sortedUsersByPR)
      for i in range(0,L):
        self.pageRankUsers[sortedUsersByPR[i][0]] = sortedUsersByPR[i][1]


      finalResultsSorted.reverse()
      #print finalResultsSorted
      print "num iter: ",iterEle
      for key in range(0,len(finalResultsSorted)):
        print "userID: ",finalResultsSorted[key][0],"user name:",self.UIDtoScreenName[finalResultsSorted[key][0]],"page Rank: ",finalResultsSorted[key][1]
      
    def default(self,line):
        print "enter a valid command\ntype help to see the list of commands. type help <command> to view the documentation of that command"
    
    def postloop(self):
        print


    def do_EOF(self,line):
        """
        End program and return to command line.
        """
        return True
        
    

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    HelloWorld().cmdloop()
