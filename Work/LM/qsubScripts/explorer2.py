#!/share/apps/epd/bin/python2.7

#	 To do:
#
#  find nn across spaces (n-grams) <<DONE for authors w/ spaces


import pdb
import pprint
from collections import Counter
import re
import sys
import os
import json
import csv
from debug import debug, init
from time import time

root = "/campusdata/panand/dialog/"
sys.path.append(os.path.join(root, 'persuasion/code/grab_data'))
import discussion as debate
data_root_dir = os.path.join(root, "persuasion/data")
debate.data_root_dir = data_root_dir
from discussion import Discussion as Debate

sys.path.append(os.path.join(root, 'utilities/nlp'))
sys.path.append(os.path.join(root, 'utilities'))

import post
from nltk.corpus import wordnet




init("debug_out")

stopWords = ['without','i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'let']

falsePositives = [ u'thermo', u'matthew',u'mathew',u'peter',u'charles', u'david',u'gods','god'
		 ,u'welcome', u'dr', u'hitler',u'linux', u'hunt', u"i'm", u'dont',u'call', u'started',u'calling',u'georgia', u"canada", u'montana', u'maine',u'maryland', u'missouri', u'ing', 'org']

isDigit = re.compile(r'\d')



def explore(directory, ids, site, func, pd = False):
    ret = []
    for threadId in ids:
        filename = threadId
        debug("Processing %s\n" % filename)

        try:
           debate = Debate("/"+ directory, filename, loadPostData = pd)
        except IOError:
           continue
#        if threadId != 3691:
#           continue       
#	pdb.set_trace() 

        if u'convinceme' in debate.metadata[u'url']:
            continue
        for argument in debate.get_posts():
            try:
               ret.append(func(argument, threadId))
            except:
                debug("Cannot process post %s\n" % threadId)
                continue
    return ret

def exp(argument, threadId):
            id = argument.id
            try:
                text = argument.text
            except:
                text = ""
            try:
                author = argument.author
            except:
                author = "!!UNKNOWN"
            if author == None:
                author = "!!UNKNOWN"
            try:
            	if type(argument.parent_id) in [unicode] : # we are dealing with a text parent, so it's an orphan post; consider it a root post
		        	parent_author = argument.parent_id
            	else: 
	                parent_author = None
            except:
		            parent_author = None
		
            try:
                timestamp = argument.timestamp
            except:
                timestamp = 0

            try:
                tokens = argument.tokens
            except:
                tokens = None
	    

#            pdb.set_trace()

	    #if tokens:							#pause this seach while tyring NickName algo...
            #    names = hasNameTok(tokens, text)
	    #    findNickNames(authors,text,id, tokens)
            #else:
            #    names = hasNameText(text)
            #if names != []:
            #    record(id, names, text, tokens)
	    
	    # Remove quote to avoid duplicate nn returns
	    quoteRanges = argument.get_ranges('quotes')
	    # For all posts with a quote
        #PA 0802012: I am changing this to filter by quoteRanges, not remove them, since we want to highlight
	#    if len(quoteRanges) > 0:
		# Pranav's elegant solution
		# Remove quotes starting from the back of the post
		# So the ranges in quoteRanges are preserved 
	#	quoteRanges.reverse()
	#	for quote in quoteRanges:
	#	 text = text[:quote.start] + text[quote.end:]
	    

	    findNickNames(authors, text, id, tokens, threadId, quotes=[(x.start, x.end) for x in quoteRanges])

def record(post, names, text, tokens):
    if tokens:
       t = "byTok"
    else:
       t = "byString"
    print "%s %s %s\n%s\n" % (post, str(names), t, text)
    
    
def getAuthor(argument):
    try:
      author = argument.author
    except:
      author = "!!UNKNOWN"
    if author == None:
      author = "!!UNKNOWN"
    return author

def hasNameTok(tokens, text):
    toks= [x.text for x in tokens]
    seen = list(set(toks), set(authors))

    spaceAuthors = filter(lambda x: " " in author, authors)
    for author in spaceAuthors:
       if author in text:
          seen.append(author)
    return seen

def hasNameText(text):
    ret = []
    for author in authors:
        if re.search(r'\b%s\b' % author, text):
          ret.append(author)
    return ret

def findNickNames(authors, text, postid, tokens, threadId, quotes = []):
#    print postid
    # this puts all the words of a post into a list
    words = re.findall(r'\w+',text)
    #words = [x.text for x in tokens]   this did the same as the line above, but not all posts are tokenized
    for author in set(authorsByThread[unicode(threadId)]): #convert to unicode because the dic is like that(FIX LATER)
#      find authors with spaces
#        if postid != 330582:
#             continue       
#       CC 11/2 >> fixed issue truncation of authors  with spaces (finds full name now) 
        if ' ' in author and author in text:
#             pdb.set_trace()
             reg = r'%s'%(lower(str(author)))
             nnInstances=[(nnInstance.start(),nnInstance.end()) for nnInstance in re.finditer(reg,lower(str(text)))]
             nnInstances = removeNamesInQuotes(nnInstances, quotes)
             for instance in nnInstances:
                         csvFile.writerow((author, author, postid, int(instance[0]), int(instance[1])))
             spaceAuthor = re.compile(author)
             textSub = spaceAuthor.sub('^', text)
#            replace space author with carrot to avoid duplicates in tokenized search
             words = re.findall(r'\w+',textSub)
        newAuthor = True
	for nn in words:
	    nnSmall=lower(str(nn))
            if newAuthor == True:
#                accuracy = jaro_winkler(author.lower(),nn.lower(),.115)
#                pdb.set_trace()
#		if postid != 330582:
#		    continue
#		pdb.set_trace()
                if nnSmall not in wordnetShort and len(nn) > 2 and nnSmall in lower(str(author)):
#                   starts/ends with word boundry or starts with word boundry ends with digit(s
#		    pdb.set_trace()
                    reg = r'\b%s(\b|\d+)'%(nnSmall)
		    nnInstances=[(nnInstance.start(),nnInstance.end()) for nnInstance in re.finditer(reg,lower(str(text)))]
#		    pdb.set_trace()

#		    and now filter this list to exclude anything in a quote

#		    nnInstances = filter(lambda x: x not in quotes, nnInstances)
                    nnInstances = removeNamesInQuotes(nnInstances, quotes)

#                    if postid != 76765:
#                        continue

#                    pdb.set_trace()    

#                       if int(postid) in [308611, 329866, 327661]:
#		            pdb.set_trace()
                    for instance in nnInstances:
                        csvFile.writerow((author, nn, postid, int(instance[0]), int(instance[1]))) 
                    newAuthor = False

    

def examineAllPosts(directory = '../../data/parsed_debates/', ids=[-1], site='fourforums', func=exp, postData = False):
    global debate
    if ids[0] == -1:
        realIds = [int(os.path.splitext(file)[0]) for file in os.listdir(os.path.join(debate.data_root_dir, directory, "discussions"))]
    else:
        realIds = ids
    return explore(directory, realIds, site, func, postData)


# note that authorFilter is no longer used by findNickNames
# using  wordnetShort from json file
def authorFilter(author):
  if len(wordnet.synsets(author))== 0: 					
    return True	                       					# probably a unique word, keep
  else:
    for syns in range(len(wordnet.synsets(author))):            
      if len(wordnet.synsets(author)[syns].instance_hypernyms()) > 0 :  # use instance_hypernyms becuase they appear only in names
        return True							
      else:
        return False							# probably a common word, throw away


def Expand(a_list):
    ret=[]
    for i in a_list:
        ret.append(range(i[0],i[1]+1))
    return ret

# this is probably a dumb way to do this...
def removeNamesInQuotes(names,quotes):
    """names/quotes are list of tuples of indices
    of names & quotes"""
    for quote in Expand(quotes):
        for name in Expand(names):
            for i in name:
                if i in quote:
                    names.remove((name[0],name[-1]))
                    break 
    return names




if __name__ == '__main__':
     global authors 
     authors = []
     
     global nickNames
     nickNames = []

     lower=str.lower


     if len(sys.argv) > 1:
        start = int(sys.argv[1])
        end = int(sys.argv[2])
        r = range(start,end+1)
     else:
        r=range(3690,3692)


#     auth = examineAllPosts(directory = 'fourforums', site='fourforums', ids=[-1], func=getAuthor, postData = False)
#     authorsC = Counter(auth)
#     f = open("authorCounts.json", "w")
#     json.dump(authorsC, f)
#     authors = authorsC.keys()
#     f.close()

     #f = open("topAuthors.json", "r")
     #topAuths = json.load(f)
     #authors = topAuths
     
#    creates filtered author list (authors that aren't words but keeping proper nouns)
     #authors = filter(lambda x: authorFilter(x), topAuths)
     
     #authors += [u'archangel', u'lurch', u'calli', u'ungerdunn',u'selasphorus', u'calligirl'] # make these words safe, don't filter them
 
    # this removes the digits from authors in the list, but causes problems
    # because now it can't tell if an author is a nickname or just the author's
    # complete name. It also caused me to realize that in cases where author names
    # differ only in final digits, it's nearly impossible to determine who the nickname
    # is refering to unless we look at the tread history.
    #
    # authors = [isDigit.sub("", author) for author in authors] 
    
     authorsByThread = open('/campusdata/panand/dialog/persuasion/code/indepStudy/authorsByThread.json', 'r')
     authorsByThread = json.load(authorsByThread)

     wordnetShort = open('/campusdata/panand/dialog/persuasion/code/indepStudy/wordnet/wordnet.json.1500Threads', 'r')
     wordnetShort = json.load(wordnetShort)
     wordnetShort.extend(falsePositives)
     wordnetShort.extend(stopWords)
     wordnetShort = set(wordnetShort)

     if len(sys.argv) > 1:
         csvf  = open('/campusdata/panand/dialog/persuasion/code/indepStudy/output/out'+str(sys.argv[1]), 'w')
#     debug mode    
     else:
         csvf  = open('/campusdata/panand/dialog/persuasion/code/indepStudy/output/out'+'TEST', 'w')
     csvFile = csv.writer(csvf, delimiter='|', quoting=csv.QUOTE_NONE)


#   writes filtered author list 
#     g = open("authorList.json", "w")
#     json.dump(authors, g)
     t=time()
    # print "Starting search ..."
     postList = examineAllPosts(directory = 'fourforums', site='fourforums', ids=r, postData=True)
    # print nickNames
     print "End seach after",(time()-t)/60, 'minutes'
     csvf.close()
     

    # wf=open("nickNames.json", 'w' )
     #json.dump(nickNames, wf)
     #wf.close()
     #db.close()
