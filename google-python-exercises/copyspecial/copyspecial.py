#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import commands

"""Copy Special exercise
"""

def get_special_paths(dirs):
  specialFiles = []
  bnames = []
  while dirs:
    allFiles = os.listdir(dirs[0])
    for filename in allFiles:
      match = re.search(r'[\w-]+__[\w-]+__[\w.]+', filename)
      if match:
          specialFiles.append(os.path.join(dirs[0],match.group()))
          bnames.append(match.group())

    dirs.pop(0) # Go to the next directory
    if len(set(bnames)) < len(bnames):
      print "error: duplicate file name"
      sys.exit(1)

  return specialFiles

def copy_to(files, todir):
  todirpath = os.path.abspath(todir)
  if not os.path.exists(todirpath):
    os.mkdir(todirpath)

  for fname in files:
    basename = os.path.basename(fname)
    shutil.copy(fname, os.path.join(todirpath, basename))

def zip_to(paths, tozip):
  print "Command to be executed : zip -j %s.zip %s" % (tozip, ' '.join(paths))
  cmd = 'zip -j %s %s' % (tozip, ' '.join(paths))
  (status, output) = commands.getstatusoutput(cmd)
  if status != 0:
    print output

def main():
  # This basic command line argument parsing code is provided.
  # Add code to call your functions below.

  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]
  if not args:
    print "usage: [--todir dir][--tozip zipfile] dir [dir ...]"
    sys.exit(1)

  # todir and tozip are either set from command line
  # or left as the empty string.
  # The args array is left just containing the dirs.
  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  tozip = ''
  if args[0] == '--tozip':
    tozip = args[1]
    del args[0:2]

  if len(args) == 0:
    print "error: must specify one or more dirs"
    sys.exit(1)

  if args[0] == 'dir':
    del args[0]
  else:
    print "usage: [--todir dir][--tozip zipfile] dir [dir ...]"
    sys.exit(1)

  dirs = []
  while args:
    dirs.append(os.path.abspath(args[0]))
    del args[0]

  specialFiles = get_special_paths(dirs)
  if todir != '':
    copy_to(specialFiles, todir)

  if tozip != '':
    zip_to(specialFiles, tozip)
  
if __name__ == "__main__":
  main()
