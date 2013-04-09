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
    TF  = defaultdict(lambda:defaultdict()) # {class: {word:count }} 
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
    allQueries = []
    allClasses = []
    dict_words=defaultdict(defaultdict)   # { word:  {category:count  }  }
    vocabulary=set()                      # unique count of words
    words_category=defaultdict()          # { category: words  }
    category_size=defaultdict()           # { category: numDocs  }
    numDocs  = float()  # total number of documents for training set

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
        qwe = [1.0]*6
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

    def bingRequest(self,req,query,category, fileMode ):
        r = requests.get(req + '&$skip=0')
        json_data=json.loads(r.text)
        rawResultsList = json_data['d']['results']

        fw = open("bing_all_OP_classifyTest.txt", fileMode)
        #every file contains IR === title === description === query === category
        queryFile = open("bing_OP_"+query, 'w')
        for result in rawResultsList:
          resultText = result['ID']+" === "+result['Title']+" === "+result['Description'] + " === "+query + " === "+category
          queryResultText = result['ID']+" === "+result['Title']+" === "+result['Description'] + " === "+query + " === "+category
          queryFile.write(queryResultText.encode('utf8'))
          queryFile.write('\n')
          fw.write(resultText.encode('utf8'))
          fw.write("\n")
        r = requests.get(req + '&$skip=15')
        json_data=json.loads(r.text)
        rawResultsList = json_data['d']['results']
        for result in rawResultsList:
          resultText =result['ID']+" === "+ result['Title']+" === "+result['Description']+ " === "+query + " === "+category
          queryResultText = result['ID']+" === "+result['Title']+" === "+result['Description']+ " === "+query + " === "+category
          queryFile.write(queryResultText.encode('utf8'))
          queryFile.write('\n')
          fw.write(resultText.encode('utf8'))
          fw.write("\n")
        fw.close()
        queryFile.close()

    def do_callBingAPI(self, arbit):
        request = 'https://user:tDPxzhwtkNX2hYu72irEhlPpFzg36bAcsX3fqbRiGS4=@api.datamarket.azure.com/Bing/Search/News?Query=%27'
        app = '%27&$format=json'
        query = [ 'apple', 'facebook', 'westeros', 'gonzaga', 'banana']
        classes = ['entertainment', 'business', 'politics']
        self.allQueries = query
        self.allClasses = classes
        for i in range(0,len(classes)):
          for q in query:
            if i==0:
              self.bingRequest( request + q+ app + "&NewsCategory=%27rt_Entertainment%27", q ,classes[i] , 'a' )
            elif i==1:
              self.bingRequest( request + q+ app + "&NewsCategory=%27rt_Business%27", q ,classes[i] , 'a' )
            elif i==2:
              self.bingRequest( request + q+ app + "&NewsCategory=%27rt_Politics%27", q ,classes[i] , 'a' )




            
    
    def do_trainSystem(self, classes):
        """
        Parse the entire tweet corpus for tf-idf and for pagerank [Run this command first before running any other command]
        """
        print "Training system.. please wait.."

        dict_words=defaultdict(defaultdict)   # { word:  {category:count  }  }
        vocabulary=set()                      
        words_category=defaultdict()          # { category: words  }
        category_size=defaultdict()           # { category: numDocs  }
        fr=open('bing_all_OP_classify.txt','r')
        lines = fr.readlines()
        numDocs=float(len(lines))
        for line in lines: 
          json_data = re.split(' === |\n', line, flags = re.UNICODE)
          rawTweetText = json_data[1] + " === " + json_data[2] + " === " + json_data[3]+ " === " + json_data[4]
          category = json_data[4]
          titleAndDesc = json_data[1]+json_data[2]
          words = re.split('[\W]+',titleAndDesc,flags=re.UNICODE)
          for word in words:
            if category in dict_words[word]:
              dict_words[word][category]=dict_words[word][category]+1
            else:
              dict_words[word][category]=1
            if category in words_category:
              words_category[category]=words_category[category]+1
            else:
              words_category[category]=1
              vocabulary.add(word)
          if category not in category_size:
            category_size[category]=1
          else:
            category_size[category]=category_size[category]+1


          tweetID = json_data[0]
          #print "for assigned class: ",json_data[0] , " , " ,json_data[3]
          self.assignedClass[json_data[0]] = json_data[4]
          #print "raw tweetText: " , rawTweetText
          #print "tweetID: ", tweetID

          tweetText = re.split('[\W]+',rawTweetText,flags=re.UNICODE)
          #mentions = json_data['entities']['user_mentions']

          #allUsers.add(userID)
          self.actualTweets[tweetID] =rawTweetText 
          words = tweetText
        fr.close()
        #fw.close()
        self.dict_words=dict_words
        self.vocabulary=vocabulary
        self.words_category=words_category
        self.category_size = category_size
        self.numDocs = numDocs
        """
        print "Calculating page rank....... "
        self.do_part2(self)
        """


    def do_classification(self, paoijnfrioune):
          
        print "performing classification"
        # P(C) = category_size[C] / numDocs
        fr=open('bing_all_OP_classifyTest.txt','r')
        #print self.dict_words

        lines = fr.readlines()
        numDocs=float(len(lines))
        for line in lines: 
          json_data = re.split(' === |\n', line, flags = re.UNICODE)
          rawTweetText = json_data[1] + " === " + json_data[2] + " === " + json_data[3]+ " === " + json_data[4]
          category = json_data[4]
          titleAndDesc = json_data[1]+json_data[2]
          words = re.split('[\W]+',titleAndDesc,flags=re.UNICODE)
          #print words
          score = defaultdict()
          maxScore =-100000
          finalCategory = ""
          #print self.words_category.keys()
          for category in self.words_category:
            if category not in score:
              score[category] = math.log( self.category_size[category]/self.numDocs , 2 )
            #print "score of category : ",score[category]
            for word in words:
              if category in score:
                if category in self.dict_words[word]:
                  score[category] += math.log( self.dict_words[word][category] , 2)
                else:
                  # add 1 smoothing for words that are not in the classifiction
                  score[category] += math.log( 1.0/( self.category_size[category]+len(self.vocabulary) ) ,2 )
              if score[category] > maxScore:
                maxScore = score[category]
                finalCategory = category
          print "max score : ", maxScore , " final category : ", finalCategory








        fr.close()


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
        for k in range(5,6):
          print "***********************  Running k-means for k = ", k ,"***************************"
          maxPurity = 0
          for i in range(0,10):
            val = self.kMeans(k)
            if val > maxPurity:
              maxPurity = val
          print "purity = ", maxPurity


    def kMeans(self,K):
        RSSprev = 1000000
        RSS = 0
        allClusters = []
        #K=5
        allDocuments = [item for item in self.tfIdfWeight]  # a list of all the documents 
        initialCentroids =  random.sample(allDocuments , K)
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
              RSS = RSS + val
          allClusters[closestCentroid].append(doc)
        #print allClusters
        #print "initial RSS: " , RSS


        RSS = 0
        # create a flat list of lists from a dict of lists
        allClustersList = list()  # [ [list of 1st cluster points], [list of 2nd cluster points]... ]
        for centroid in allClusters:
          allClustersList.append(allClusters[centroid])

        #print allClustersList
        numIterations = 0

        while math.fabs( RSSprev - RSS ) > 0.0000000001:
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
          
            for term in centroid:
              centroid[term] = centroid[term]/float(numPoints)
          
            allClusterCentroids[i] = centroid
          
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
                RSS = RSS + val
              #print "closest index: ",closestCentroidIndex
            #print "final closest index: ",closestCentroidIndex
            #print "newAllClustersList: ",newAllClustersList[closestCentroidIndex]
            newAllClustersList[closestCentroidIndex].append(doc)
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

        # printing all the clusters here
        #"""
        for i in range(0,len(newAllClustersList)):
          cluster = newAllClustersList[i]
          print "\n\n\ncluster ", i , " : number of documents in this cluster: " ,len(cluster) 
          for ID in cluster:
            text = re.split(' === |\n ', self.actualTweets[ID], flags = re.UNICODE)
            #print len(text)
            print text[2], " : ", text[0]
        #"""


        print "====================================  Calculating Purity: ======================================="
        
        purity = 0
        for cluster in newAllClustersList:
          purityScale = defaultdict()
          for item in cluster:
            text = re.split(' === |\n', self.actualTweets[item], flags = re.UNICODE)
            word = text[2]
            self.assignedCluster[item] = word
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


        print "====================================  Calculating RI: ======================================="
        TP=0
        FN=0
        FP=0
        TN=0

        for doc1 in allDocuments:
          for doc2 in allDocuments:
            if self.assignedClass[doc1] == self.assignedClass[doc2]:
              if self.assignedCluster[doc1] == self.assignedCluster[doc2]:
                TP +=1
              else:
                FN +=1
            if self.assignedClass[doc1] != self.assignedClass[doc2] :
              if self.assignedCluster[doc1] == self.assignedCluster[doc2]:
                FP +=1
              else:
                TN +=1

        print "TP: ", TP , ' TN: ', TN, ' FP: ', FP, ' FN: ', FN
        RI = (TP+TN)/(TP+TN+FP+FN)

        
        print "purity percent: ",purityPercent, "% , RI: ", RI," RSS: ", RSS, " number of iterations to converge: ", numIterations

        
        
        return purityPercent




        







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
