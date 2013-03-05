How to run the file: 

Note: Algorithm is explained below these steps. At any point of time, type help to see the list of command and "help <command_name> for their documentation"

0) First run "parseFile" command. This will automatically call another command to calculate the PageRank for all the users. Result of part2 will be displayed in the first step itself. Takes roughly 30-45 seconds or so.
1) part1: run the "part1" command. Enter any query to search using cosine similarity using TF-IDF values
2) part2: part2 or pagerank results are displayed in step 1.
3) part3: run the "part1" command. Enter any query to search using cosine similarity using TF-IDF values and the user's pagerank (of who tweeted the tweet)
4) bonus: run the "part5_bonus" command. Enter any query to find the topic sensitive pageranks
5) type EOF to exit the prompt


Part1: 
Calculating TF is same as discussed in class. 
Calculating IDF is slightly modified. I calculated the retweet_count of each tweet in the tweet corpus. 
So, here is my logic: If a tweet is re-tweeted 1000 times, it means that, there are 1000 more virtual tweets to consider. 
In this way, the idf values of those words in the most re-tweeted tweets will go down. This is a very small change that has resulted in better output when compared to ignoring the tweets.

Part2: 
Calculating page rank scores using the power method (NOT matrix). Calculating to a precision of 0.01 or 150 iterations (whichever is lesser)

Part3: part 3 combines part1 and part 2 into a combined score. I calculate it with this formula: 

result_score = alpha*tf-idf_cosine_result + (1-alpha)*pageRank_score

The search results evaluates to something like, "the tweets matched with cosine score and also biased with the pagerank score of that user"
I normalized the tf-idf_cosine and pageRank scores AGAIN to make them look like similar values in a different way. I normalized each value with this formula:

value = (value-minValue)/(maxValue-minValue)

The above normalisation doesn't gaurentee to sum up to 1. But it makes sure that every value takes a value between zero and one. Thus the above result_score makes sense. 

I tried calculating with various values of alpha and obtained different results. I left the program to run with alpha = 0.2 This value can be adjusted and various experiments can be performed.

I observed that, even when I vary the alpha value from 0.2 to 0.8 , the pagerank score was more biased than the cosine score value on the actual documents with the query.

For eg: 
for the query : red planet , (explanation below)

results for 0.2 were: 
(Cmd) part3
Enter a query: red planet
printing with formula: [alpha*tweetResults + (1-alpha)*pagerank ] with alpha as  0.2

tweetID:  232333164423548928 Tweet:  #MSL: One hour until the landing of @MarsCuriosity on the red planet. Are you watching? http://t.co/qMeFERLo #MSL  User:  NASA
tweetID:  232332665796313088 Tweet:  @MarsCuriosity
Mars rover Curiosity closing in on red planet at 8,000 mph  User:  Patti0713
tweetID:  232303837799665664 Tweet:  Planet Mars =)  User:  WindaPuspita06
tweetID:  232321793803829249 Tweet:  Is Mars red?  User:  The_Red_Twin_
tweetID:  232322366053691392 Tweet:  Mars landing soon!! #Ready #Red planet  User:  Sallyzar2
tweetID:  232326083746349056 Tweet:  90 minutes to #MSL and #Curiosity lands on the Red Planet.  User:  drtgrav
tweetID:  232327071781756929 Tweet:  #Curiosity #NASA ...we are getting closer to landing on the Red planet!!!  User:  carasorrell09
tweetID:  232322062075719680 Tweet:  When @MarsCuriosity lands, we'll get to see more of how the Red Planet isn't all that red  User:  RaphaelShepard
tweetID:  232333448923201536 Tweet:  RT @NASA: #MSL: One hour until the landing of @MarsCuriosity on the red planet. Are you watching? http://t.co/qMeFERLo #MSL  User:  thatdrew
tweetID:  232315008057495552 Tweet:  Red planet rover, red planet rover, let curiosity come over #fb  ( @marscuriosity live at http://t.co/jIq6o1Ln)  User:  CliveTheDog
tweetID:  232333327745548290 Tweet:  RT @NASA: #MSL: One hour until the landing of @MarsCuriosity on the red planet. Are you watching? http://t.co/qMeFERLo #MSL  User:  Cardoso



and results for 0.8 were: 

printing with formula: [alpha*tweetResults + (1-alpha)*pagerank ] with alpha as  0.8
tweetID:  232333164423548928 Tweet:  #MSL: One hour until the landing of @MarsCuriosity on the red planet. Are you watching? http://t.co/qMeFERLo #MSL  User:  NASA
tweetID:  232332665796313088 Tweet:  @MarsCuriosity
Mars rover Curiosity closing in on red planet at 8,000 mph  User:  Patti0713
tweetID:  232303837799665664 Tweet:  Planet Mars =)  User:  WindaPuspita06
tweetID:  232321793803829249 Tweet:  Is Mars red?  User:  The_Red_Twin_
tweetID:  232333448923201536 Tweet:  RT @NASA: #MSL: One hour until the landing of @MarsCuriosity on the red planet. Are you watching? http://t.co/qMeFERLo #MSL  User:  thatdrew
tweetID:  232322366053691392 Tweet:  Mars landing soon!! #Ready #Red planet  User:  Sallyzar2
tweetID:  232326083746349056 Tweet:  90 minutes to #MSL and #Curiosity lands on the Red Planet.  User:  drtgrav
tweetID:  232327071781756929 Tweet:  #Curiosity #NASA ...we are getting closer to landing on the Red planet!!!  User:  carasorrell09
tweetID:  232333327745548290 Tweet:  RT @NASA: #MSL: One hour until the landing of @MarsCuriosity on the red planet. Are you watching? http://t.co/qMeFERLo #MSL  User:  Cardoso
tweetID:  232322062075719680 Tweet:  When @MarsCuriosity lands, we'll get to see more of how the Red Planet isn't all that red  User:  RaphaelShepard
tweetID:  232333354291298305 Tweet:  RT @NASA: #MSL: One hour until the landing of @MarsCuriosity on the red planet. Are you watching? http://t.co/qMeFERLo #MSL  User:  CCantuQ

Cardoso,thatdrew users' tweets are coming up in the search slowly. Their pageranks were initially less affecting the results, but as we change the alpha value, it started coming up in the results.



Part 4: SEO!! 

For the SEO contest, I created the page http://urjnaswxkfjjknow.wordpress.com/ and started writing blogs in it. I made sure I improve the site regularly so that the blog looks fresh for the search engines to crawl. 
Steps taken : 
1. Used Google and Bing webmaster tools and included the site as my personal site. 
2. Added meta tags that verify the website to the search engines. Added it for Google, Bing and Pinterest.
3. Created a pinterest board with a few pins in it pointing to my blog :P 
4. Made sure all the images were properly labelled and captions contained the search term urjnasw xkfjjkn. All file names contained the search term. 
5. The anchor text had search terms in or around them. 
6. Gave links to famous basketball players and other celebrities. 
7. It is a static page - makes it easier for the crawler.
8. Suggested that my website exists in bing. When others were contesting in google, I was shown as the first few results in bing. Infact, I tried my best to optimize it for bing
9. Convinced friends with blogs of heavy traffic to add links to my site. This would boost the pagerank of my page.
10. Social media: tweeted, shared in facebook, pinned in pinterest, gtalk, friends and what not to publicise my site. 

PS: Ultimately after all these efforts I ended up in the last position in the waiting list :P Must add sitemap


Part 5 [BONUS]: Topic Sensitive PageRank

Here, I divided the problem into 3 parts:
1. Create the topics: I used 17 different categories found on www.dmoz.org/
2. Assign users to topics: For every user, pick a random topic on the 17 topics and assign it to them. Pick all the users who mention this user, and who are mentioned by this user into the set. This way we get a set of users into every category. Also, Note that one user can be in more than 1 category. I tried one aproach to assign users to particular topics (instead of random topics). I tried reading the description of the user and then classifying them on the basis of their frequency in that description. The results did not turn out impressive and hence I thouht I will go with the random assignment itself.
3. Perform the page rank algorithm in these seperate topics and generate results with part2 code!! 
