#!c:/Python27/bin

import getopt
import re
import sys
import urllib2

def load_data(offline, debug=None):

  if offline:
    if debug: print "\nOffline\n"
    text = open("../../data/chap_data/chapterone.htm", 'rU').read()
  else:
    if debug: print "\nOnline\n"
    req = urllib2.urlopen("http://www.washingtonpost.com/wp-srv/style/books/chapterone.htm")
    text = req.read()
    
  if debug: print "data length = [%d]\n" % len(text)
  return text

def parse_data(data, debug=None):
  books = {}
  pattern = r'<b><a href="http://www.washingtonpost.com/wp-srv/style/longterm/books/chap1/(\w+).htm">([^<]+)<'

  if debug: print "\n\nBuilding book dictionary from website"
  for match in re.finditer(pattern, data):
    item = {}
    key = match.group(1)
    title = match.group(2)
    if debug:  print "==> [%s] [%s]" % (key, title)
    item['key'] = key
    item['title'] = title
    books[key] = item

  if debug: print "\n\nSorted Book dictionary"
  for k,v in sorted(books.items()):
    if debug: print "--> %s %s" % (k, v)

  if debug: print "\n%s chapters are available.\n" % (len(books))
  return books

def usage():
  print "Usage: chap.py [-h --help] [-x --offline] [-d --debug]\n"

def parse_options(argv):
  options={}
  options['offline']=None
  options['debug']=None
  try:
    opts, args = getopt.getopt(argv, "hxd", ["help", "offline", "debug"])
  except getopt.GetoptError, err:
    # print help information and exit:
    print str(err) # will print something like "option -a not recognized"
    usage()
    sys.exit(2)
    
  for o, a in opts:
    if o in ("-h", "--help"):
      usage()
      sys.exit()
    elif o in ("-x", "--offline"):
      options['offline'] = True
    elif o in ("-d", "--debug"):
      options['debug'] = True
    else:
      assert False, "unhandled option"
      
  if options['debug']: print "parse_options argv = %s\n" % argv
      
  return options

def main():
  options = parse_options(sys.argv[1:])  
  data = load_data(options['offline'], options['debug'])
  books = parse_data(data, options['debug'])
  print "\nThere are %s books in the Washington Post Chapter One website\n" % (len(books))

if __name__ == "__main__":
    main()
