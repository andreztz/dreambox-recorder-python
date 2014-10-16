#!/usr/bin/python

import time
import os
import sys
import subprocess
import urllib3

# move on, nothing to see here yet
print 'Test that streaming shit'

token = '1:0:1:13F:39:1:FFFF01D2:0:0:0:'

arrayAll = [
	"cvlc",
	"http://10.20.0.99/web/stream.m3u?ref=%s" % (token),
	"--sout",
	"file/mpg:/tmp/test.mpg"
]


zapUrl = 'http://10.20.0.99/web/zap?sRef=%s&title=PythonRecording-DontChangeChannelPlease' % (token)
http = urllib3.PoolManager()
request = http.request('GET', zapUrl)
#process = os.execvp("cvlc", arrayArgs)
#process = os.popen(cmd)
process = subprocess.Popen(arrayAll)

print "Start debugging"
time.sleep(25)
print "End Debugging"

for prop in dir(process):
	print prop

print type(process)
#print 
process.kill()