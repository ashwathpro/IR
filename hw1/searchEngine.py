import sys
import os
import re
from collections import defaultdict
import cmd

class HelloWorld(cmd.Cmd):
    """Simple command processor example."""
    
    index = defaultdict(set)
    posIndex = defaultdict(lambda:defaultdict(set)) # {word : {1:[1,21,4] }}
    kgramIndex = defaultdict(set)
    
    def do_EOF(self,line):
        return True
    
    def do_printIndexLength(self,aodsufbtribun):
        try:
            print "index created with length: ",len(self.index)
        except TypeError:
            print "please run buildIndex first before accessing the index \n"
        #return True
    def do_test(self,asgbtrh):
        str= "\"ash is a ash is \" a ash"
        splittd= str.split("\"")
	print splittd
        for word in splittd:
            print "splitting.. ",word.split("\""),"\n"
	p={}
	o=""
	if len(list(p))==0: print "!p"

	#if !o: print "!o"
            
    def wildCardSingleWordQuery(self,q):
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
	#print "query grams:",queryKgrams
	intermediateResult=set()
	for word in queryKgrams:
		intermediateResult.update(self.kgramIndex[word])
	#print "intermediate res:" , intermediateResult
	#print len(list(intermediateResult))

	result = set()
	(prefix, suffix) = q.split('*')
	#print "prefix,suffix: ",prefix,suffix
	for res in list(intermediateResult):
		if res.startswith(prefix) and res.endswith(suffix):
			result.update(self.index[res])
	#print "result: ",result	
        #result1 = set(result[0]).intersection(*result[1:])
	#print "final wildcard result: ",result1,len(result1)

	return result

    def do_writeToFile(self,line):
	fw=open("indexFile.txt",'w')
        for key in self.index:
          s= key + " : " + ' '.join(self.index[key]) + "\n"
          fw.write(s)
        fw.close()
	fw=open("kgramIndexFile.txt",'w')
	for key in self.kgramIndex:
          s= key + " : " + ' '.join(self.kgramIndex[key]) + "\n"
          fw.write(s)
        fw.close()

	fw=open("posIndexFile.txt",'w')
        for file in self.posIndex:
		for key in file:
			s= file + " : " + key + " : " + ' '.join(self.posIndex[file][key]) + "\n"
          		fw.write(s)
        fw.close()


    def do_buildIndex(self,asgbtrh):
        # Get the name from the command line, using 'World' as a fallback.
        dir = "./books/books/"
        fw=open("indexFile.txt",'w')
        fw.close()
        filenames = os.listdir(dir)
        #print filenames
        
        for file in filenames:
            f=open(os.path.join(dir, file),'rU')
            cleanWords = re.sub('[\W_]+',' ', f.read())
            words = (cleanWords.split())
	    i=0
            while i<len(words):
                fileparts= file.split('.')
                self.index[words[i].lower()].add(fileparts[0])
                self.posIndex[words[i].lower()][fileparts[0]].add(i)
		words[i]=words[i].lower()
                tmpWord = '$' + words[i] + '$'
		j=0
		while j<len(words[i])+1:
			self.kgramIndex[tmpWord[j:j+2]].add(words[i])
			j+=1
                i+=1
            f.close()
            
        print "created normal index with length: ",len(self.index)
        #print "created positional index with length: ",len(self.posIndex)
        #print self.posIndex["happen"]["19"]
        
    def simpleQuery(self,q):
        wordList = []
	if len(q)==0: return []
        words = q.split()
        for word in words:
            wordList.append(self.index[word])
        #print wordDict
        result = set(wordList[0]).intersection(*wordList[1:])
        #print result
        return result

    def phraseQuery(self,q):
        results=self.simpleQuery(q)
	#print "simple results: ", results
        finalResult=[]
	interRes=[]
        words = q.split()
        for result in results:
		i=0
		flag=1
		posList1=list(self.posIndex[words[i]][result])
		pos=0
		while pos<len(posList1):
			#if every other wordList[i] has correspondin pos + i then add this result to final result
			j=i+1
			flag=1
			otherPos=posList1[pos]+1
			while j < len(words) and flag==1:
				if otherPos in list(self.posIndex[words[j]][result]):
					flag=1
					j+=1
					otherPos +=1
				else : 
					flag=0
					j+=1
					otherPos +=1
					break
			if flag==1: 
				finalResult.append(result)
				break
			else:
				pos+=1
				continue
	#print "Phrase is found in: ",finalResult
	return finalResult

    def do_query(self,line):
        q=raw_input("Enter a query: ")
	matches = re.findall('\"[^"]*\"',q)
	phraseQueries = []
	simpleQueryWords = []
	simpleWildCardWords = []
	for  match in matches:
		phraseQueries.append(match.replace('"',''))
	#q= 'this is a " phrase start" in the mid*dle "phrase ends" how yo*u doin'
	print "phrase query: ",phraseQueries
	queryWithoutPhrases = re.sub('\"[^"]*\"','',q)
	restOfQuery= queryWithoutPhrases.split()
	for word in restOfQuery:
		if '*' in word:
			simpleWildCardWords.append(word)
		else:
			simpleQueryWords.append(word)
	
	#simpleQueryWords = re.sub(r'.*[\*].*','',queryWithoutPhrases)
	print "query wildcards: ",simpleWildCardWords
	print "query simple: ",simpleQueryWords

	phraseResults=set()
	wildcardResults=set()
	simpleResults=set()
	
	i=0
	for phrase in phraseQueries:
		if i==0:
			phraseResults.update(set(self.phraseQuery(phrase)))
			i=1
		else:
			phraseResults=phraseResults.intersection(set(self.phraseQuery(phrase)))
	print "The phrase query results: ",phraseResults

	i=0
	for word in simpleWildCardWords:
		if i ==0:
			wildcardResults.update(set(self.wildCardSingleWordQuery(word)))
			i=1
		else:
			wildcardResults= wildcardResults.intersection(set(self.wildCardSingleWordQuery(word)))
	print "Wild card results: ", wildcardResults
	
	simpleResults = set(self.simpleQuery(" ".join(simpleQueryWords)))
	print "the simple query results: ",simpleResults
	finalResult = set()
	master = list(set())
	if len(phraseQueries) >=1:
		master.append(phraseResults)
	if len(simpleWildCardWords) >=1:
		master.append(wildcardResults)
	if len(simpleQueryWords) >=1:
		master.append(simpleResults)
	
	if len(master)==1:
		finalResult = master[0]
	else:
		finalResult = master[0].intersection(*master[1:])
	
	print "Final Output is : ",finalResult
	print "number of documents found: ", len(list(finalResult))


	#print self.wildCardSingleWordQuery(q)

        #res=self.simpleQuery(q)
	#if q:
	#	res = self.phraseQuery(q.lower())
	#print res
        
    def default(self,line):
        print "enter a valid command\n"
    
    def postloop(self):
        print

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    HelloWorld().cmdloop()
