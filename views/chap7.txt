#!c:/Python27/bin

import getopt
import re
import sys
import urllib2

books_url = 'http://www.washingtonpost.com/wp-srv/style/books/'
chap1_url = 'http://www.washingtonpost.com/wp-srv/style/longterm/books/chap1/'
review_url = 'http://www.washingtonpost.com/wp-dyn/content/article/' 

def usage():
  print "Usage: chap.py [-h --help] [-x --offline] [-d --debug]\n"

def parse_options(argv=None):
  """parse command line options"""  
  options={}
  for key in ['offline', 'debug', 'error' , 'exit']: options[key] = None
  
  try:
    opts, args = getopt.getopt(argv, "hxd", ["help", "offline", "debug"])
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
    else:
      assert False, "unhandled option"

  return options

def load_data(key, options):
  """load html page data"""
  
  global books_url, chap1_url
  item_filename = "../../data/chap_data/%s.htm" % key  
  if options['offline']:
    text = open(item_filename, 'rU').read()
  else:
    try:
      if (key=='chapterone'): base_url=books_url
      else: base_url=chap1_url
      page_url = "%s%s.htm" % (base_url, key)
      req = urllib2.urlopen(page_url)
      text = req.read()
    except Exception, err:  # timed out internet connection, get offline file.
      print "No online connection, getting loading offline file."
      text = open(item_filename, 'rU').read()
    
  #if options['debug']: print "data length ['%s'] = [%d]\n" % (key, len(text))
  return text 

def parse_data(data, options):
  """load chapter book data into book dictionary"""
  global chap1_url, review_url
  books = {}
  if options['debug']: print "Building book dictionary from website"
  
  # Extract key and title from html source
  pattern = r'<b><a href="'
  pattern += '(%s)' % chap1_url	 	# group 1: Chap url prefix
  pattern += '(\w+).htm">'		# group 2: key
  pattern += '([^<]+)<[^<]+[^,]*,'	# group 3: title
  pattern += '" (non)?fiction '		# group 4: type
  pattern += 'by ([^<]+)<'		# group 5: author
  pattern += '[aA <]+'			# bad data in crashcourse
  pattern += 'href="(%s)' % review_url	# group 6: Review url prefix
  pattern += '([0-9]+/[0-9]+/[0-9]+/)'	# group 7: date
  pattern += '(\w+.html)">'		# group 8: review
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

  # Extract key and title from html source
  pattern = r'plsfield:credit-->'
  pattern += '([^\.]+)\.\s*'	# group 1: Publisher
  pattern += '([\d]+)[^$]+'	# group 2: pages
  pattern += '\$([^<]+)<'	# group 3: cost  
  
  for match in re.finditer(pattern, data):
    books[key]['publisher']=match.group(1).strip()
    books[key]['pages']=match.group(2).strip()
    books[key]['cost']=match.group(3).strip()
    
  return books  
 

def main():
  """Text mine the Washington Post Chapter One Data""" 
  # Parse command line options
  options = parse_options(sys.argv[1:])
  if options['debug']: print "parse_options argv = %s" % sys.argv[1:]  
  if options['exit']:
    if options['error']: print options['error']
    usage()
    sys.exit(2)
    
  # Load the chapter one data
  data = load_data('chapterone', options)
  
  # Parse the chapter one data list
  books = parse_data(data, options)
  
  # Load and parse each chapter one item
  for k,v in sorted(books.items()):   
    item_data = load_data(k, options)   
    books = parse_chapter(k, item_data, books, options)

  # Debug output 
  if options['debug']: 
    """      
    output all items in book dictionary
    for k,v in sorted(books.items()):
      print "--> %s\n    %s\n" % (k, v) 
    """    
    # output sample of book items
    count = 0
    for k,v in sorted(books.items()):
      print ""      
      #if (count<54): print "book['%s']" % (k)
      item = v
      for a in item:
	 if (count<54): print "book['%s']['%s']: '%s'" % (k, a, item[a])
      count += 1 
   
  
  print "\nThere are %s books in the Washington Post Chapter One website\n" % (len(books))

if __name__ == "__main__":
    main()
