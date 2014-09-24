#!/usr/bin/python

import time
import os
import sys
import subprocess

# move on, nothing to see here yet
print 'Test that streaming shit'

cmd = "cvlc http://10.20.0.99/web/stream.m3u?ref=1:0:19:235C:5B:1:FFFF0182:0:0:0: --sout file/mkv:/tmp/61091.mkv"
arrayAll = [
	"cvlc",
	"http://10.20.0.99/web/stream.m3u?ref=1:0:19:235C:5B:1:FFFF0182:0:0:0:",
	"--sout",
	"file/mkv:/tmp/61091.mkv"
]
arrayArgs = [
	"http://10.20.0.99/web/stream.m3u?ref=1:0:19:235C:5B:1:FFFF0182:0:0:0:",
	"--sout",
	"file/mkv:/tmp/61091.mkv"
]

#process = os.execvp("cvlc", arrayArgs)
#process = os.popen(cmd)
process = subprocess.Popen(arrayAll)

print "Start debugging"
time.sleep(5)
print "End Debugging"

for prop in dir(process):
	print prop

print type(process)
#print 
process.kill()