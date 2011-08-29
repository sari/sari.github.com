#!c:/Python27/bin

import getopt
import sys

def usage():
  print "Usage: python getopt_test.py [-h --help] [-x --offline]\n"

def main():

  print "\n\n\n====================== begin getopt_test output"
  end_msg="====================== end getopt_test\n\n"

  print "\nINFO: Command Line: %s" % (sys.argv)
  for i,arr in enumerate(sys.argv):
    print "INFO: argv[%d]=%s" % (i, arr)

  try:
    opts, args = getopt.getopt(sys.argv[1:], "hx", ["help", "offline"])
    print "\nINFO: GetOpt Arguments: "
    print "INFO: opts = %s" % opts
    print "INFO: args = %s\n" % args

  except getopt.GetoptError, err:
    # print help information and exit
    print "\nError: %s" % str(err) # will print something like "option -z not recognized"
    usage()
    print end_msg
    sys.exit(2)
  
  offline=None
  for o, a in opts:
    if o in ("-h", "--help"):  # is variable o in this array
      usage()
      print end_msg
      sys.exit()
    elif o in ("-x", "--offline"):
      offline=True

  if offline:
    print "You are running in offline mode.\n"
  else:
    print "You are running in online mode.\n"

  print end_msg

if __name__ == "__main__":
  main()