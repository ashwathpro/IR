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
    
    def do_test(self,asgbtrh):
        #if !o: print "!o"
            
    def do_parseFile(self,line):
	fr=open("mars_tweets_medium.json",'r')
        
            
    def default(self,line):
        print "enter a valid command\n"
    
    def postloop(self):
        print

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    HelloWorld().cmdloop()
