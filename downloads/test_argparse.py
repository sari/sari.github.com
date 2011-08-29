#!c:/Python27/bin

import argparse
import sys

def main():
  print "\n"
  parser = argparse.ArgumentParser(epilog="Example: test_argparse.py -n MyName")
  parser.add_argument('-x', '--offline', help='use offline data file (not from internet) ', action='store_true')
  parser.add_argument('-n', '--name', nargs=1, help='Enter your name', required=True)
  parser.add_argument('-a', '--authors', help='List all authors.', action='store_true')
  parser.add_argument('-b', '--books', help='List all books.', action='store_true')
  parser.add_argument('-r', '--review', nargs=1, help='Chapter review for specified book',metavar='book')
  parser.add_argument('-s', '--search', nargs=1, help='Search for specified term in all books.',metavar='search_term')
  args = parser.parse_args()

  print "\n\n\n====================== begin argparse_test output"
  end_msg="====================== end argparse_test\n\n"
  print "\nINFO: Command Line: %s" % (sys.argv)
  for i,arr in enumerate(sys.argv):
    print "INFO: argv[%d] = %s" % (i, arr)

  print "\nINFO: parse_args:"
  print "INFO: argParse args = %s" % (args)
  print "INFO: argParse args.name = %s" % (args.name)
  print "INFO: argParse args.name[0] = %s" % (args.name[0])

  if args.name:
   if args.offline:
    mode = "offline"
   else:
     mode = "online"
   print "\nWelcome %s, you are running this program in %s mode\n" % (args.name[0], mode)

  print end_msg

if __name__ == "__main__":
  main()