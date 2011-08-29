#!c:\Python27\python

import re


# Reference: http://docs.python.org/library/re.html
# \d is a single token matching a digit
# \w match all characters that are considered letters given the current locale settings
# \s matches any whitespace character
# \S matches any non-whitespace character


def Find(pat, text):
  """
  Find the regular expression pattern (pat) in the text string.
  """
  match = re.search(pat, text)
  if match: print "\nPattern[%s] Text[%s] Result[%s]" % (pat, text, match.group())
  else: print '\nnot found'
  
Find('..g', 'called piiig much better:xyzg')
Find(r'\d\s\d\d', 'blah :1 23xyz  ')
Find(r':\w+', 'blah :kitten blah blah  ')
Find(r':\w+', 'blah :kitten123 blah blah  ')
Find(r':\w+', 'blah :kitten123& blah blah  ')

Find(r':\S+', 'blah :kitten123&02934j85gf3f-=0i*&^*& blah blah  ')

Find(r'\w[\w.]*@[\w.]+', 'blah nick.p@gmail.com yatta @ ')


# grouping in parenthesis
pat = r'([\w.]+)@([\w.]+)'
text = 'blah nick.p@gmail.com yatta foo@bar '
for match in re.finditer(r'([\w.]+)@([\w.]+)', text):
  print "\nFINDITER Pattern[%s] Text[%s]\n   Result Group1=[%s]     Group2=[%s]" % (pat, text, match.group(1), match.group(2))
 
