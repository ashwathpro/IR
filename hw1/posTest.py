import sys
import os
import re
from collections import defaultdict
import cmd

class HelloWorld(cmd.Cmd):
    """Simple command processor example."""
    
    index = defaultdict(set)
    kgramIndex = defaultdict(set)

    def do_greet(self, person):
        """greet [person]
        Greet the named person"""

	print self.kgramIndex["w$"]
        if person:
            print "hi,", person
        else:
            print 'hi'
	
	str="ashwath"
	#if str.startswith("ash") and str.endswith("ashwath"): print str
	str = 'this is a " phrase start" in the middle "phrase ends"'
	matches = re.findall('\"[^"]*\"',str)
	phraseQueries = []
	for  match in matches:
		phraseQueries.append(match.replace('"',''))
	q= 'this is a " phrase start" in the mid*dle "phrase ends" how yo*u doin'
	print "phrase query: ",phraseQueries
	queryWithoutPhrases = re.sub('\"[^"]*\"','',q)
	restOfQuery= queryWithoutPhrases.split()
	simpleQueryWords = []
	simpleWildCardWords = []
	for word in restOfQuery:
		if '*' in word:
			simpleWildCardWords.append(word)
		else:
			simpleQueryWords.append(word)
	
	#simpleQueryWords = re.sub(r'.*[\*].*','',queryWithoutPhrases)
	print "query wildcards: ",simpleWildCardWords
	print "query simple: ",simpleQueryWords

	#print re.sub('\"[^"]*\"','' ,str)


    def do_EOF(self,line):
        return True
    
    def do_printIndexLength(self,aodsufbtribun):
        try:
            print "index created with length: ",len(self.index)
        except TypeError:
            print "please run buildIndex first before accessing the index \n"
        #return True
    def widlCardSingleWordQuery(self,q):
    	# split query to k-grams
	queryKgrams=[]
	
	tmp = "$" + q + "$"
	j=0
	tmp=tmp.split('*')
	#print "printing tmp query:",tmp
	
	for tm in tmp:
		if tm == "$": 
			continue
		j=0
		while j<len(tm)-1:
			queryKgrams.append(tm[j:j+2])
			j+=1
	print queryKgrams
	intermediateResult=set()
	for word in queryKgrams:
		intermediateResult.update(self.kgramIndex[word])
	print intermediateResult
	print len(list(intermediateResult))

	result = []
	(prefix, suffix) = q.split('*')
	for res in list(intermediateResult):
		if res.startswith(prefix) and res.endswith(suffix):
			result.append(list(self.index[res]))
	
	print result,len(result)




#	for res in intermediateResult:
#	if tmp[0] != "$" and (tmp[-1] !="$" and tmp )





    def do_buildIndex(self,asgbtrh):
        # Get the name from the command line, using 'World' as a fallback.
        dir = "./books/books/"
        fw=open("indexFile.txt",'w')
        fw.close()
        filenames = os.listdir(dir)
        #print filenames
        
        #for file in filenames:
        f=open(os.path.join(dir, "19.txt"),'rU')
        cleanWords = re.sub('\W+',' ', f.read())
        #tmp=open("tmpFile.txt",'w')
        posIndex = defaultdict(lambda:defaultdict(set)) # {word : {1:[1,21,4] }}
        words = cleanWords.split()
        i=0
        while i<len(words):
		posIndex[words[i].lower()]["19"].add(i)
                self.index[words[i].lower()].add('19')
                words[i] = words[i].lower()
		tmpWord = "$" + words[i] + "$"
		j=0
		while j<len(words[i])+1:
			self.kgramIndex[tmpWord[j:j+2]].add(words[i])
			j+=1
		i+=1
        #print self.kgramIndex
	
        
        """
        for word in words:
            inbetweenwords = cleanWords.split(word)     # ["as erhg werh edh", "asfdgg wtrh wsh shf swh", "asfd rh asd"]
            posCnt=1
            docInd=defaultdict(list)
	for phrase in inbetweenwords:
	atoms = phrase.split()              # ["as","erhg", "werh" .. ]
                posCnt += len(atoms)
                docInd["19"].append(posCnt)
            posIndex[word]=docInd
        print posIndex["leaf"]["19"]
        
        for word in words:
          fileparts = words.split('.')
          self.index[word.lower()].add(fileparts[0])
        f.close()
        print "index created with length: ",len(self.index)
        """
        #fw=open("indexFile.txt",'w')
        #for key in index:
        #  s= key + " : " + ' '.join(index[key]) + "\n"
        #  fw.write(s)
        #fw.close()
    def do_query(self,line):
        q=raw_input("Enter a query: ")
	if q:
		res = self.widlCardSingleWordQuery(q.lower())
        #wordList = []
        #words = q.split()
        #for word in words:
        #    wordList.append(self.index[word])
        #print wordDict
        #print set(wordList[0]).intersection(*wordList[1:])
        
    def default(self,line):
        print "enter a valid command\n"
    
    def postloop(self):
        print

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    HelloWorld().cmdloop()
