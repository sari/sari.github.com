#!c:/Python27/bin


""" SearchUrl 

Find a search term in a webpage and return context of that search term.

Required Parameters:
topic           A shortcut to define the url for this topic.
term            The search term

Optional Parameters:
# Use view source on the webpage to help determine these values.
left_bound_tag  The left bound tag of the search term.
right_bound_tag The right bound tag of the search term.

Sample Usage:
python ./searchurl.py phobia cats '<br>' '<br>'
python ./searchurl.py babyname Ava '<tr align="right">' '</tr>'


To Do:
 - Add your own website to search a list for a term that returns the term context.
 - Add a message if the term was not found.
 - Add a message if the topic does not exist, and then exit.
 
"""

import re
import sys
import urllib2

args = sys.argv[1:]

if not args:
    print 'usage: topic searchterm [left_bound_tag] [right_bound_tag]'
    sys.exit(1)
topic = args[0]
searchterm = args[1]

# Get the optional parameters
if args[2]:
  left_bound = args[2]
else: left_bound='<br>'
if args[3]:
  right_bound = args[3]
else: right_bound='<br>'

if topic == 'phobia':
  url='http://phobialist.com/';
elif topic == 'babyname':
  url='http://www.socialsecurity.gov/OACT/babynames/';
else:
  url='http://www.emory.edu/';
  
    
print "Topic[%s]: search for term[%s] in url[%s] left_bound[%s] right_bound[%s]\n" % (topic, searchterm, url, left_bound, right_bound)
      
req = urllib2.urlopen(url)
text = req.read()

pattern = r'%s(.*%s.*)%s' % (left_bound, searchterm, right_bound)
regex = re.compile(pattern, re.IGNORECASE)
for match in regex.finditer(text):
    print "%s" % (match.group(1))
  
