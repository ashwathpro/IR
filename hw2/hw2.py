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
    
    termFreq = defaultdict(lambda:defaultdict()) # {word : {1:[1,21,4] }}
    idfList = defaultdict(list)
    idf = defaultdict()
    
    
    def do_EOF(self,line):
        return True
    
    def do_test(self,asgbtrh):
        if o: print "!o"
            
    def do_parseFile(self,asdfrtg):
        fr=open('mars_tweets_medium.json','r')
        allWords = set()
        lines = fr.readlines()
        #line = lines[0]
        numDocs=len(lines)
        numDocs = 4
        #for line in lines[0:4]:
        for i in range(0,3):
          #print line
          line= lines[i]
          json_data=json.loads(line)
          rawTweetText = json_data['text']

          tweetID = json_data['id']
          tweetText = re.split('[\W]+',rawTweetText,flags=re.UNICODE)
          words = tweetText
          docTermFreq = defaultdict()
          for word in words:
            word = word.lower()
            allWords.add(word)
            self.idfList[word].append(tweetID)
            if word in self.idf:
              self.idf[word] = self.idf[word] + 1 
            else:
              self.idf[word] = 1 


            if word in docTermFreq:
              docTermFreq[word] = docTermFreq[word]+1
            else:
              docTermFreq[word] = 1
          
          self.termFreq[tweetID]=docTermFreq

          #print self.termFreq[tweetID]
        print len(self.idf)
        
        print(self.idf['mars'])
        for doc in self.termFreq: 
          for word in self.termFreq[doc]:
            if self.termFreq[doc][word] > 0:
              self.termFreq[doc][word] = 1 + math.log(self.termFreq[doc][word] ,2)
            else:
              self.termFreq[doc][word] = 0

        for word in self.idf:
          self.idf[word] = math.log(numDocs/self.idf[word],2)
          print self.idf[word]

        print(self.idf['mars'])

        fr.close()

    def do_query(self,lineadfsggh):

        q=raw_input("Enter a query: ")

    def default(self,line):
        print "enter a valid command\n"
    
    def postloop(self):
        print

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    HelloWorld().cmdloop()
