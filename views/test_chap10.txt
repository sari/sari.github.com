#!c:/Python27   /bin;/usr/bin/python

import argparse
import unittest
import getopt 
from chap27 import load_data
from chap27 import parse_data

class ArgParseMock(object):
  def __init__(self, offline, loglevel, freq):
    self.offline = offline
    self.loglevel = loglevel
    self.freq = freq

class TestChapFuntions(unittest.TestCase):

  def setUp(self):
	
    self.args = ArgParseMock(True, 'WARN', None) # create the mock for the arguments 

    # offline data   
    self.offline_data = load_data('chapterone', self.args)

    # offline book dictionary
    self.books = parse_data(self.offline_data, self.args)
    
    # this function runs once before the individual tests are run
    self.expected_length = 47067
    self.expected_book_count = 59

# load_data tests 
  def test_load_data_offline(self):
    offline_length = len(self.offline_data)
    err_msg = "Offline data length [%s] does not equal expected length [%s]" % (offline_length, self.expected_length)
    self.assertEqual(offline_length, self.expected_length, err_msg)
  def test_load_data_online(self):
    online_data =  load_data('chapterone', self.args)
    online_length = len(online_data)
    err_msg = "Online data length [%s] does not equal expected length [%s]" % (online_length, self.expected_length)
    self.assertEqual(online_length, self.expected_length, err_msg)
  def test_load_data_pattern(self):
    err_msg = "Pattern not contained in offline data."
    pattern = r'Chapter One \(washingtonpost.com\)'
    self.assertRegexpMatches(self.offline_data, pattern, err_msg)    

# parse_data tests 
  def test_parse_data_book_count(self):
    book_count = len(self.books)
    err_msg = "Offline book count [%s] does not equal expected book count [%s]" % (book_count, self.expected_book_count)
    self.assertEqual(book_count, self.expected_book_count, err_msg)
  def test_load_data_key_exists_key(self):
    err_msg = "Key 'star' not found in book dictionary."
    self.assertIn('star', self.books, err_msg)
  def test_load_data_key_exists_title(self):
    err_msg = "Key 'camus' not found in book dictionary."
    self.assertIn('camus', self.books, err_msg) 
  def test_load_data_key_doesnotexist_badkey(self):
    err_msg = "Key 'badkey' found in book dictionary."
    self.assertNotIn('badkey', self.books, err_msg)
  def test_load_data_itemkey_exists_title(self):
    chap = self.books['star']
    err_msg = "Key 'title' not found in item dictionary."
    self.assertIn('title', chap, err_msg)  
  def test_load_data_itemkey_exists_key(self):
    chap = self.books['star']
    err_msg = "Key 'key' not found in item dictionary."
    self.assertIn('key', chap, err_msg)  
  def test_load_data_itemkey_doesnotexist_badkey(self):
    chap = self.books['star']
    err_msg = "Key 'badkey' found in item dictionary."
    self.assertNotIn('badkey', self.books, err_msg) 

#if __name__ == '__main__':
#    unittest.main()

suite = unittest.TestLoader().loadTestsFromTestCase(TestChapFuntions)
unittest.TextTestRunner(verbosity=2).run(suite)

'''
http://docs.python.org/library/unittest.html

Method  Checks that
assertEqual(a, b)   a == b   
assertNotEqual(a, b)  a != b   
assertTrue(x)   bool(x) is True    
assertFalse(x)  bool(x) is False   
assertIs(a, b)  a is b
assertIsNot(a, b)   a is not b
assertIsNone(x)   x is None 
assertIsNotNone(x)  x is not None 
assertIn(a, b)  a in b
assertNotIn(a, b)   a not in b
assertIsInstance(a, b)  isinstance(a, b)
assertNotIsInstance(a, b)   not isinstance(a, b)

Method  Checks that
assertRaises(exc, fun, *args, **kwds)   fun(*args, **kwds) raises exc    
assertRaisesRegexp(exc, re, fun, *args, **kwds)   fun(*args, **kwds) raises exc and the message matches re

Method  Checks that
assertAlmostEqual(a, b)   round(a-b, 7) == 0   
assertNotAlmostEqual(a, b)  round(a-b, 7) != 0   
assertGreater(a, b)   a > b 
assertGreaterEqual(a, b)  a >= b
assertLess(a, b)  a < b 
assertLessEqual(a, b)   a <= b
assertRegexpMatches(s, re)  regex.search(s) 
assertNotRegexpMatches(s, re)   not regex.search(s) 
assertItemsEqual(a, b)  sorted(a) == sorted(b) and works with unhashable objs 

Method  Used to compare
assertMultiLineEqual(a, b)  strings 
assertSequenceEqual(a, b)   sequences 
assertListEqual(a, b)   lists 
assertTupleEqual(a, b)  tuples
assertSetEqual(a, b)  sets or frozensets
assertDictEqual(a, b)   dicts 
'''
