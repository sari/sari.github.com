#!/opt/local/bin/python2.7
'''
This script read in a list of Washington Post Review books,
load the chapter one and the chapter one review text,
and then runs a word frequency on the text.
Usage: python chap27.py [-x] [-q] [-vDEBUG]
where
-x --offline: Use offline data (do not connect to internet).
-v --loglevel[INFO|WARN|DEBUG]: Set the logging level
-1 --freq: Calculate the word frequence on the chapter and review.
'''

import argparse
import logging
import re
import sys
import urllib2
from string import punctuation

logger = logging.getLogger(__name__)
chaptext = {}       # Dictionary of chapter one text.
reviewtext = {}     # Dictionary of chapter one's review text.
errors = {}         # Count of errors
    
def config_logging(level):
    # configure logger to be used for script output
    logger.setLevel(level)
    # customize log output slightly
    ch = logging.StreamHandler(sys.stderr)
    ch.setLevel(level)
    logger.addHandler(ch)
    # don't propagate to root logger
    logger.propagate = False

def get_base_url(type='sumpage'):
    if type == 'sumpage': return 'http://www.washingtonpost.com/wp-srv/style/books/'
    elif type == 'review': return 'http://www.washingtonpost.com/wp-dyn/content/article/'
    else: return 'http://www.washingtonpost.com/wp-srv/style/longterm/books/chap1/'

def get_offline_path(key, review_url=None):
    '''Get the path and filename for opening offline files.
    Use the key for the base of the filename.'''
    if review_url is None: result = "../../data/chap_data/%s.htm" % key
    # If review_url is set for offline, append "_review" to the filename
    else: result = "../../data/chap_data/%s_review.htm" % key
    return result
        
def load_data(key, args, review_url=None):
    'Load html page data'
    open_url=None	# url or filename of the item opened
    if args.offline:
        open_url = get_offline_path(key, review_url)   
        text = open(open_url, 'rU').read()  # open the file, read into string
    else: # Access online data via urls
        try:
	        # if a review, then use the url parameter from the item dictionary.
            if review_url: open_url = review_url
            else:
	            # if the main chapter one list, use this specific base url
                if (key=='chapterone'): get_base_url('sumpage')
                else: base_url=get_base_url('chap1')
                open_url = "%s%s.htm" % (base_url, key)
            # open the page (url or local file)
            req = urllib2.urlopen(open_url)  # open the html url page
            # read the page into a string
            text = req.read()
        except Exception, err: # timed out internet connection, get offline file.
            logger.info("No online connection, getting loading offline file.")
            open_url = get_offline_path(key, review_url)
            text = open(open_url, 'rU').read()
            
    if review_url is None: logger.info("Chapter Page [%s] = [%d]    url[%s]" % (key, len(text), open_url))
    else: logger.info("Review Page  [%s] = [%d]    url[%s]" % (key, len(text), open_url))
    return text

def loadStopWords():
    'Create a list of words to ignore when calc word frequency.'
    stopWordsList = ['']    # Opens empty list
    stopWordsText = open("stopWords.txt", 'r') # reads stopWords.txt
    for words in stopWordsText:
        words = words.strip('\n')
        stopWordsList.append(words) # add word to stopWordsList
    logger.debug("\nStop Word List count = [%d]\n" % len(stopWordsList))
    return stopWordsList

def parse_data(data, args):
    '''load chapter book data into book dictionary'''
    
    books = {}

    logger.debug("Building book dictionary from website")
    
    # Extract chap_url, chap_file, key, title, author and review url from html source
    pattern = r'<b><a href="'
    pattern += '(%s)' % get_base_url('chap1') # group 1: Chap url prefix
    pattern += '(\w+).htm">' # group 2: key
    pattern += '([^<]+)<[^<]+[^,]*,' # group 3: title
    pattern += '" (non)?fiction ' # group 4: type
    pattern += 'by ([^<]+)<' # group 5: author
    pattern += '[aA <]+' # bad data in crashcourse
    pattern += 'href="(%s)' % get_base_url('review') # group 6: Review url prefix
    pattern += '([0-9]+/[0-9]+/[0-9]+/)' # group 7: date
    pattern += '(\w+.html)">' # group 8: review
    for match in re.finditer(pattern, data):
        
        if match.group(2)=='anninesghost': key='anniesghost'
        else: key=match.group(2)
        item = {}
        item['chap_url']=get_base_url('chap1') + key + '.htm'
        item['chap_file']=key + '.htm'
        item['key']=key
        item['title']=match.group(3)
        item['type']= "nonfiction" if match.group(4)=="non" else "fiction"
        item['author']=match.group(5).strip()
        item['review']=get_base_url('review') + match.group(7).strip() + match.group(8).strip()

        books[key]=item

    return books
    
def parse_chapter(key, data, books, args):
    '''load chapter data into book dictionary'''

    # Extract publisher, pages, cost and text from chapter one html source
    '''
	<!--plsfield:credit-->Three Rivers. 338 pp. Paperback, $15<br> #theannarchist
	<!--plsfield:credit-->Simon & Schuster. 640 pp., $30<br>  #star
	<!--plsfield:credit-->Free Press. 258 pp. $26<br> # somethingintheair
	<!--plsfield:credit-->Simon & Schuster. 320 pp., $26<br> #crashcourse
	<!--plsfield:credit-->Crown. 448 pp., $26.99<br> #bowie
	<!--plsfield:credit-->Farrar, Straus and Giroux. 592 pp., $35<br> #ayndrand
	<!--plsfield:credit-->Knopf. 273 pp. $25.95<br> #angeltime
    '''
    pattern = r'plsfield:credit-->'
    pattern += '([^\.0-9]+)\.??\s*' # group 1: Publisher
    pattern += '([\d]+)[^$]+' # group 2: pages
    pattern += '\$([^<]+)<' # group 3: cost
    pattern += '.*<!--plsfield:description-->(.*)<i>\(?Continues\.\.\.\)?' 
    
    books[key]['publisher']=''
    books[key]['pages']=''
    books[key]['cost']=''
    for match in re.finditer(pattern, data):
        books[key]['publisher']=match.group(1).strip()
        books[key]['pages']=match.group(2).strip()
        books[key]['cost']=match.group(3).strip()
        
        # Get text of chapter one, remove html tags and extra spaces
        chap_one_text = remove_html_tags(match.group(4).strip())
        chap_one_text = remove_extra_spaces(chap_one_text)
        chaptext[key]=chap_one_text        

    return books
    
def parse_review(data, args):    
    'Parse review data for reviewtext dictionary'

    # Extract text of review, do not include: tags or special chars
    pattern = r'<div id="body_after_content_column">([\W\S]*)<br clear="all">'
    review_text = ''
    for match in re.finditer(pattern, data):
        # Get text of chapter one review text, remove html tags and extra spaces
        review_text = remove_html_tags(match.group(1).strip())
        review_text = remove_html_chars(review_text)            
        review_text = remove_extra_spaces(review_text)    

    return review_text    
 
def find_frequent_words(title, data, stopWordsList):            
    logger.info("\nTitle: %s\n" % title) 
    # create a list of words separated at whitespaces
    wordList1 = data.split(None)

    # strip any punctuation marks and build modified word list
    # start with an empty list
    wordList2 = []
    for word1 in wordList1:
	    # filter lambda example:
		#   mult3 = filter(lambda x: x % 3 == 0, [1, 2, 3, 4, 5, 6, 7, 8, 9])
		#   sets mult3 to [3, 6, 9], those elements of the original list that are multiples of 3
		# below: set word1 to chars in word1 where char is not in char list specified
        word1 = filter(lambda c: c not in "\".?,;", word1)            
        # build a wordList of lower case modified words
        wordList2.append(word1.lower())

    # create a wordfrequency dictionary
    # start with an empty dictionary
    freqDict = {}
    for word2 in wordList2:
	    # get method syntax dict.get(key, default=None)
	    # return a value for the given key. 
	    # If key is not available then return returns default value.
        freqDict[word2] = freqDict.get(word2, 0) + 1

    logger.info("Word list length = [%d] before removal of stop words." % len(freqDict))

    # Delete all words frsom stopWordList
    for delword in stopWordsList:
        if delword in freqDict:
            del freqDict[delword]

    logger.info("Word list length = [%d] after removal of stop words.\n" % len(freqDict))

    logger.info("%-15s %s" % ("Word", "Frequency"))      
    for w in sorted(freqDict, key=freqDict.get, reverse=True):
        if freqDict[w] > 2: logger.info("%-15s %d" % (w, freqDict[w]))

def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def remove_html_chars(data):
    p = re.compile(r'&[^;]+;')
    return p.sub('', data)            

def remove_extra_spaces(data):
    p = re.compile(r'\s+')
    return p.sub(' ', data)
            
def sort_items(x, y):
    '''Sort by value first, and by key (reverted) second.'''
    return cmp(x[1], y[1]) or cmp(y[0], x[0])        
	
if __name__ == "__main__":
	
    '''Load command line arguments'''
    parser = argparse.ArgumentParser(epilog="Example: chap.py -x -q -v Debug")
    parser.add_argument('-q', '--freq', default=None, help='Find word frequence in chapter and review text.', action='store_true')  
    parser.add_argument('-x', '--offline', default=None, help='use offline data file', action='store_true')
    parser.add_argument('-v', '--loglevel', metavar='loglevel', required=False,
                        choices=['WARN', 'INFO', 'DEBUG'], default='WARN',
                        help='Log level for additional output.')
    args = parser.parse_args()
    print "ARGS:%s" % args

    logger.info("ARGS offline[%s] loglevel[%s] freq[%s]" % (args.offline, args.loglevel, args.freq))

    # configure logging
    config_logging(getattr(logging, args.loglevel))
    
    '''Text mine the Washington Post Chapter One Data'''
    # Load the chapter one data
    chap_one_data = load_data('chapterone', args)
    
    # Parse the chapter one data list
    books = parse_data(chap_one_data, args)
    print "Loading %d books." % len(books)
    count = 0
    # Load and parse each chapter one item
    errors=0;
    for k,v in sorted(books.items()):
        if args.loglevel == 'WARN':   # Add a progress indicator
            count+=1
            sys.stdout.write('.')
            sys.stdout.flush()
            if count % 5 == 0: print " %d of %d" % (count, len(books))
        logger.info("--------")           
        item_data = load_data(k, args)
        books = parse_chapter(k, item_data, books, args.offline)
        if k in chaptext: logger.info("Chapter Text [%s] = [%d]" % (k, len(chaptext[k])))
        else: 
            logger.info("Chapter Text [%s] NOT FOUND" % (k))
            errors += 1 
        # Load Review and Parse text into reviewtext dictionary
        review_data = load_data(k, args, books[k]['review'])    
        reviewtext[k] = parse_review(review_data, args)
        logger.info("Review Text  [%s] = [%d]" % (k, len(reviewtext[k])))

    # Debug output
    #output all items in book dictionary
    #for k,v in sorted(books.items()):
    #logger.debug("--> %s\n %s\n" % (k, v))

    # output sample of book items
    count = 0
    for k,v in sorted(books.items()):
        #if (count<54): logger.debug("\nbook['%s']" % (k))           
        logger.debug("\nbook['%s']" % (k))
        item = v
        for a in item:
            #if (count<54): logger.debug("book['%s']['%s']: '%s'" % (k, a, item[a]))       
            logger.debug("book['%s']['%s']: '%s'" % (k, a, item[a]))
            count += 1

    if args.freq:
        # Load Stop Words
        stopWordsList = loadStopWords()            
        # output word frequency in chaptext dictionary
        count = 0
        for key in sorted(chaptext):
            find_frequent_words(books[key]['title'], chaptext[key], stopWordsList)
            find_frequent_words("REVIEW of " + books[key]['title'], reviewtext[key], stopWordsList) 
    
    logger.info("\nSummary:")
    logger.info("    There are %s books in the Washington Post Chapter One website" % (len(books)))  
    logger.info("    Error: Found %d of %d chapters that failed to read in the chapter one text." % (errors, len(books)))



