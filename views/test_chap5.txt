#!c:/Python27/bin

import unittest
from chap import load_data
from chap import parse_data

class TestChapFuntions(unittest.TestCase):

  def setUp(self):
    # this function runs once before the individual tests are run
    self.expected_length = 47067
    self.expected_book_count = 59
   
  def test_load_data_offline(self):
    offline_data =  load_data(True)
    offline_length = len(offline_data)
    err_msg = "Offline data length [%s] does not equal expected length [%s]" % (offline_length, self.expected_length)
    self.assertEqual(offline_length, self.expected_length, err_msg)

  def test_load_data_online(self):
    online_data =  load_data(False)
    online_length = len(online_data)
    err_msg = "Online data length [%s] does not equal expected length [%s]" % (online_length, self.expected_length)
    self.assertEqual(online_length, self.expected_length, err_msg)

  def test_parse_data(self):

    # Test offline data length
    offline_data =  load_data(True)
    books = parse_data(offline_data)
    book_count = len(books)
    err_msg = "Offline book count [%s] does not equal expected book count [%s]" % (book_count, self.expected_book_count)
    self.assertEqual(book_count, self.expected_book_count, err_msg)

if __name__ == '__main__':
    unittest.main()

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
assertDictContainsSubset(a, b)  all the key/value pairs in a exist in b

Method  Used to compare
assertMultiLineEqual(a, b)  strings 
assertSequenceEqual(a, b)   sequences 
assertListEqual(a, b)   lists 
assertTupleEqual(a, b)  tuples
assertSetEqual(a, b)  sets or frozensets
assertDictEqual(a, b)   dicts 
'''
