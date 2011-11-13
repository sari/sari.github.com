#!c:/Python27/bin

import getopt
import re
import sys
import urllib2
from string import punctuation

books_url = 'http://www.washingtonpost.com/wp-srv/style/books/'
chap1_url = 'http://www.washingtonpost.com/wp-srv/style/longterm/books/chap1/'
review_url = 'http://www.washingtonpost.com/wp-dyn/content/article/'
stopWordsList = [''] # List of words to ignore when calc word frequency.
chaptext = {} # Dictionary of chapter one text.
reviewtext = {} # Dictionary of chapter one's review text.
errors = {} # Count of errors

def usage():
  print "Usage: chap.py [-h --help] [-x --offline] [-d --debug] [-q --frequency]\n"

def parse_options(argv=None):
  """parse command line options"""
  options={}
  # Initialize the options parameter list values
  for key in ['offline', 'debug', 'freq', 'error' , 'exit']: options[key] = None
  
  try:
    opts, args = getopt.getopt(argv, "hxdq", ["help", "offline", "debug", "freq"])
  except getopt.GetoptError, err:
    options['exit']=True
    options['error']=err
    return options

  for o, a in opts:
    if o in ("-h", "--help"):
      options['exit']=True
    elif o in ("-x", "--offline"):
      options['offline'] = True
    elif o in ("-d", "--debug"):
      options['debug'] = True
    elif o in ("-q", "--frequency"):
      options['freq'] = True
    else:
      assert False, "unhandled option"

  return options

def load_data(key, options, review_url=None):
  """load html page data"""
  
  global books_url, chap1_url

  if options['offline']:
    # If review_url is set for offline, append "_review" to the filename
    if review_url is None: item_filename = "../../data/chap_data/%s.htm" % key
    else: item_filename = "../../data/chap_data/%s_review.htm" % key
    text = open(item_filename, 'rU').read()
  else: # Access online data via urls
    try:
      if review_url: page_url = review_url
      else:
        if (key=='chapterone'): base_url=books_url
        else: base_url=chap1_url
        page_url = "%s%s.htm" % (base_url, key)
      # open the page (url or local file)
      req = urllib2.urlopen(page_url)
      # read the page into a string
      text = req.read()
    except Exception, err: # timed out internet connection, get offline file.
      print "No online connection, getting loading offline file."
      text = open(item_filename, 'rU').read()
      
    print "Page Length [%s] = [%d] review[%s]" % (key, len(text), review_url)
  return text

def parse_data(data, options):
  """load chapter book data into book dictionary"""
  global chap1_url, review_url
  books = {}
  if options['debug']: print "Building book dictionary from website"
  
  # Extract chap_url, chap_file, key, title, author and review url from html source
  pattern = r'<b><a href="'
  pattern += '(%s)' % chap1_url # group 1: Chap url prefix
  pattern += '(\w+).htm">' # group 2: key
  pattern += '([^<]+)<[^<]+[^,]*,' # group 3: title
  pattern += '" (non)?fiction ' # group 4: type
  pattern += 'by ([^<]+)<' # group 5: author
  pattern += '[aA <]+' # bad data in crashcourse
  pattern += 'href="(%s)' % review_url # group 6: Review url prefix
  pattern += '([0-9]+/[0-9]+/[0-9]+/)' # group 7: date
  pattern += '(\w+.html)">' # group 8: review
  for match in re.finditer(pattern, data):
    item = {}
    item['chap_url']=chap1_url + match.group(2).strip() + '.htm'
    item['chap_file']=match.group(2).strip() + '.htm'
    item['key']=match.group(2)
    item['title']=match.group(3)
    item['type']= "nonfiction" if match.group(4)=="non" else "fiction"
    item['author']=match.group(5).strip()
    item['review']=review_url + match.group(7).strip() + match.group(8).strip()
    books[match.group(2)]=item

  return books
  
def parse_chapter(key, data, books, options):
    
  """load chapter data into book dictionary"""
  
  global chaptext # dictionary of chapter one text

  # Extract publisher, pages, cost and text from chapter one html source
  pattern = r'plsfield:credit-->'
  pattern += '([^\.]+)\.\s*' # group 1: Publisher
  pattern += '([\d]+)[^$]+' # group 2: pages
  pattern += '\$([^<]+)<' # group 3: cost
  pattern += '.*<h3> Chapter One </h3>(.*) <p> <i>\(Continues\.\.\.\)' #
  
  for match in re.finditer(pattern, data):
    books[key]['publisher']=match.group(1).strip()
    books[key]['pages']=match.group(2).strip()
    books[key]['cost']=match.group(3).strip()
    
    # Get text of chapter one, remove html tags and extra spaces
    chap_one_text = remove_html_tags(match.group(4).strip())
    chap_one_text = remove_extra_spaces(chap_one_text)
    chaptext[key]=chap_one_text

  return books
  
def parse_review(data, options):
   
  """parse review data for reviewtext dictionary"""

  # Extract text of review, do not include: tags or special chars
  pattern = r'<div id="body_after_content_column">([\W\S]*)<br clear="all">'
  review_text = ''
  for match in re.finditer(pattern, data):
    # Get text of chapter one review text, remove html tags and extra spaces
    review_text = remove_html_tags(match.group(1).strip())
    review_text = remove_html_chars(review_text)
    review_text = remove_extra_spaces(review_text)

  return review_text
 

def main():
  
  global chaptext, reviewtext, errors
  """Text mine the Washington Post Chapter One Data"""
  # Parse command line options
  options = parse_options(sys.argv[1:])
  if options['debug']: print "parse_options argv = %s" % sys.argv[1:]
  if options['exit']:
    if options['error']: print options['error']
    usage()
    sys.exit(2)
        
  print "--------"
  # Load the chapter one data
  data = load_data('chapterone', options)
  
  # Parse the chapter one data list
  books = parse_data(data, options)
    
  # Load and parse each chapter one item
  errors=0;
  for k,v in sorted(books.items()):
    print "--------"
    item_data = load_data(k, options)
    books = parse_chapter(k, item_data, books, options)
    if k in chaptext: print "Chapter Text [%s] = [%d]" % (k, len(chaptext[k]))
    else:
      print "Chapter Text [%s] NOT FOUND" % (k)
      errors += 1
    # Load Review and Parse text into reviewtext dictionary
    review_data = load_data(k, options, books[k]['review'])
    reviewtext[k] = parse_review(review_data, options)
    print "Review Text [%s] = [%d] => parse => [%d]" % (k, len(review_data), len(reviewtext[k]))

  # Debug output
  if options['debug']:

    #output all items in book dictionary
    #for k,v in sorted(books.items()):
    #print "--> %s\n %s\n" % (k, v)

    # output sample of book items
    count = 0
    for k,v in sorted(books.items()):
      #if (count<54): print "\nbook['%s']" % (k)
      print "\nbook['%s']" % (k)
      item = v
      for a in item:
        #if (count<54): print "book['%s']['%s']: '%s'" % (k, a, item[a])
        print "book['%s']['%s']: '%s'" % (k, a, item[a])
        count += 1

  if options['freq']:
    # Load Stop Words
    loadStopWordList(options)
    # output word frequency in chaptext dictionary
    count = 0
    for key in sorted(chaptext):
      find_frequent_words(books[key]['title'], chaptext[key])
      find_frequent_words("REVIEW of " + books[key]['title'], reviewtext[key])
  
  print "\nSummary:"
  print " There are %s books in the Washington Post Chapter One website" % (len(books))
  print " Error: Found %d of %d chapters that failed to read in the chapter one text." % (errors, len(books))
  
def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)
    
def remove_html_chars(data):
    p = re.compile(r'&[^;]+;')
    return p.sub('', data)
  
def remove_extra_spaces(data):
    p = re.compile(r'\s+')
    return p.sub(' ', data)
    
def loadStopWordList(options):
    global stopWordsText
    #opens empty list, reads stopWords.txt
    #adds all words in stopWords.txt to open list
    stopWordsText = open("stopWords.txt", 'r')
     
    for words in stopWordsText:
      words = words.strip('\n')
      stopWordsList.append(words)
      
    if options['debug']: print "\nStop Word List count = [%d]\n" % len(stopWordsList)
      
def find_frequent_words(title, data):
    print "\nTitle: %s\n" % title
    # create a list of words separated at whitespaces
    wordList1 = data.split(None)
     
    # strip any punctuation marks and build modified word list
    # start with an empty list
    wordList2 = []
    for word1 in wordList1:
      word1 = filter(lambda c: c not in "\".?,;", word1)
      # build a wordList of lower case modified words
      wordList2.append(word1.lower())
     
    # create a wordfrequency dictionary
    # start with an empty dictionary
    freqDict = {}
    for word2 in wordList2:
     freqDict[word2] = freqDict.get(word2, 0) + 1

    print "Word list length = [%d] before removal of stop words." % len(freqDict)
    
    # Delete all words frsom stopWordList
    for delword in stopWordsList:
      if delword in freqDict:
del freqDict[delword]

    print "Word list length = [%d] after removal of stop words.\n" % len(freqDict)
    
    print "%-15s %s" % ("Word", "Frequency")
    for w in sorted(freqDict, key=freqDict.get, reverse=True):
        if freqDict[w] > 2: print "%-15s %d" % (w, freqDict[w])

def sort_items(x, y):
  """Sort by value first, and by key (reverted) second."""
  return cmp(x[1], y[1]) or cmp(y[0], x[0])

if __name__ == "__main__":
    main()

