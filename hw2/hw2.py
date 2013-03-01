import sys
import os
import re
from collections import defaultdict
import cmd
import json
from pprint import pprint 
import math

class HelloWorld(cmd.Cmd):
    """Simple command processor example."""
    actualTweets = defaultdict()  # {tweetID: tweet text}
    termFreq = defaultdict(lambda:defaultdict()) # {word : {1:2 }}
    idfList = defaultdict(set)
    idf = defaultdict()
    tfIdfWeight = defaultdict(lambda:defaultdict()) # {document : {word : tf-idf }}

    
    def do_EOF(self,line):
        return True
        
    
    def do_test(self,asgbtrh):
        testList=[(1,2),(3,4),(5,6)]
        asd = [1]*6
        qwe = [1.0]*6
        for i in range(0,6):
          print qwe[i]
        print [i-j for i,j in zip(asd ,qwe)]
            
    def do_parseFile(self,asdfrtg):
        fr=open('mars_tweets_medium.json','r')
        lines = fr.readlines()
        numDocs=float(len(lines))
        #numDocs = 4.0
        for line in lines:
        #for i in range(0,4):
          json_data=json.loads(line)
          rawTweetText = json_data['text']

          tweetID = json_data['id']
          tweetText = re.split('[\W]+',rawTweetText,flags=re.UNICODE)

          self.actualTweets[tweetID] =rawTweetText 
          words = tweetText
          docTermFreq = defaultdict()
          for word in words:
            word = word.lower()
            self.idfList[word].add(tweetID)
        
            if word in docTermFreq:
              docTermFreq[word] = docTermFreq[word]+1
            else:
              docTermFreq[word] = 1
          
          self.termFreq[tweetID]=docTermFreq
          #print self.termFreq[tweetID]
        #print len(self.idf)
        for word in self.idfList:
          self.idf[word] = math.log(numDocs/len(self.idfList[word]),2)

        print self.idf['mars']
        for doc in self.termFreq:
          sumNorm=0
          for word in self.termFreq[doc]:
            if self.termFreq[doc][word] > 0:
              self.termFreq[doc][word] = 1 + math.log(self.termFreq[doc][word] ,2)
            else:
              self.termFreq[doc][word] = 0
            self.tfIdfWeight[doc][word] = self.termFreq[doc][word]*self.idf[word]
            sumNorm = sumNorm + self.tfIdfWeight[doc][word]*self.tfIdfWeight[doc][word] 
          for word in self.tfIdfWeight[doc]:
            self.tfIdfWeight[doc][word] =  self.tfIdfWeight[doc][word]/math.sqrt(sumNorm) 


        fr.close()

    def do_query(self,lineadfsggh):
        q=raw_input("Enter a query: ")

        queryWeight = defaultdict()

        queryText = re.split('[\W]+',q,flags=re.UNICODE)
        #print queryText
        queryTermFreq = defaultdict()
        for word in queryText:
          word = word.lower()
          if word in queryTermFreq:
            queryTermFreq[word] = queryTermFreq[word]+1
          else:
            queryTermFreq[word] = 1
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
        for doc in self.termFreq:
          value=0
          commonTerms = set()
          commonTerms = set(queryWeight.keys()).intersection(set(self.termFreq[doc]))
          for word in commonTerms:
            value = value + queryWeight[word]*self.termFreq[doc][word]
            #print word
          if len(commonTerms)>0:  
            resultSet[doc]=value
          #print (doc,value)
        
        results=[(key,val) for key, val in sorted(resultSet.iteritems(), key=lambda (k,v): (v,k))]
              #print "%s: %s" % (key, value)
              #results.append(tuple(key,value))
        print len(results),"Results found"
        finalResultsSorted=results[-50:]
        finalResultsSorted.reverse()
        #print finalResultsSorted
        for key in range(0,len(finalResultsSorted)):
          print (finalResultsSorted[key][0],self.actualTweets[finalResultsSorted[key][0]],finalResultsSorted[key][1])





    def do_pageRank(self,qwertrgrvm):
      fr=open('mars_tweets_medium.json','r')
      lines = fr.readlines()
      numDocs=float(len(lines))
      into = defaultdict(set) # {word : {1:2 }}
      outOf = defaultdict(set) # {word : {1:2 }}
      allUsers = set()
      for line in lines:
      #for i in range(0,10):
       # line = lines[i]
        json_data=json.loads(line)
        rawTweetText = json_data['text']
        userID = json_data['user']['id']
        tweetID = json_data['id']
        tweetText = re.split('[\W]+',rawTweetText,flags=re.UNICODE)
        mentions = json_data['entities']['user_mentions']
        
        allUsers.add(userID)
        for m in mentions:
          if m['id'] != userID:
            outOf[userID].add(m['id'])
            allUsers.add(m['id'])

        #for user in outOf[userID]:


        for mention in mentions:
          if mention['id'] != userID:
            into[mention['id']].add(userID)
            allUsers.add(mention['id'])
          #print mention['id'] , json_data['user']['id']

          #print mentions
      print len(into)

      properUsers = set((set(outOf.keys())|set(into.keys())))
      oldUserToPR = defaultdict(float)
      newUserToPR = defaultdict(float)
      for user in properUsers:
        oldUserToPR[user]=1.0
        newUserToPR[user]=1.0

    
      d = 0.1
      N= len(properUsers)
      breakLimit = 0.001
      while True:
        for user in newUserToPR:
          degree = float(len(outOf[user]))
          valToSplit = oldUserToPR[user]/degree

          for outUser in outOf[user]:
            newUserToPR[outUser] = (1.0-d)*(oldUserToPR[outUser] + valToSplit) + d

        
        diffPR = [i-j for i,j in zip(oldUserToPR ,newUserToPR)] 
        if all([math.fabs(indivPR) <= breakLimit for indivPR in diffPR ]): 
          break

      # sort PR and print

      sortedUsersByPR=[(key,val) for key, val in sorted(newUserToPR.iteritems(), key=lambda (k,v): (v,k))]
      print len(sortedUsersByPR),"Results found"
      finalResultsSorted=sortedUsersByPR[-50:]
      finalResultsSorted.reverse()
      #print finalResultsSorted
      for item in finalResultsSorted:
        print item 

















       








      
    def default(self,line):
        print "enter a valid command\n"
    
    def postloop(self):
        print

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    HelloWorld().cmdloop()
