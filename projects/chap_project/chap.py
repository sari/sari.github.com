#!c:/Python27/bin

import getopt
import re
import sys
import urllib2



def load_data(offline):

  if offline:
    print "\nOffline\n"
    text = open("../../data/chap_data/chapterone.htm", 'rU').read()
  else:
    print "\nOnline\n"
    req = urllib2.urlopen("http://www.washingtonpost.com/wp-srv/style/books/chapterone.htm")
    text = req.read()
    
  print "data length = [%d]\n" % len(text)
    

def usage():
  print "Usage: chap.py [-h --help] [-x --offline]\n"

def main():
  try:
    opts, args = getopt.getopt(sys.argv[1:], "hx", ["help", "offline"])
  except getopt.GetoptError, err:
    # print help information and exit:
    print str(err) # will print something like "option -a not recognized"
    usage()
    sys.exit(2)
    
  offline = None
  for o, a in opts:
    if o in ("-h", "--help"):
      usage()
      sys.exit()
    elif o in ("-x", "--offline"):
      offline=True
    else:
      assert False, "unhandled option"
    
  load_data(offline)

if __name__ == "__main__":
    main()
