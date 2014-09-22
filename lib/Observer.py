#!/usr/bin/env python

import sys
import MySQLdb
import time
import urllib
from Daemon import Daemon

class Observer(Daemon):
	
	db = False
	cursor = False
	logging = False
	outputPath = '/tmp/'
	checkInterval = 5

	def init(self, logging = False):
		self.setLogging(logging)


	def setOutputPath(self, outputPath):
		self.outputPath = outputPath

	# set logging object for debug purpose
	def setLogging(self, logging):
		self.logging = logging

	# main loop
	def run(self):
		while True:
			#accept connections from outside
			self.listen()
			time.sleep(self.checkInterval)

	# check db and livestream match, if you hit one, start recording till end
	def listen(self):
		# if stream consumer is running, cut it here already...

		self.db = MySQLdb.connect("localhost","root","","dreambox-recorder")
		self.cursor = self.db.cursor()
		currentTime = int(time.time())
		timeMin = currentTime - 5
		timeMax = currentTime + 5
		sql = "SELECT * FROM recording WHERE state='waiting' AND (timeStart >= %i OR timeStart <= %i)" % (timeMin, timeMax)
		try:
			self.cursor.execute(sql)
			results = self.cursor.fetchall()
			for row in results:
				id = row[0]
				token = row[1]
				streamUrl = 'http://10.20.0.99/web/stream.m3u?ref=%s' % (token)
				# start recording and update state
				# some tries with ffmpeg
				command = "ffmpeg -i '%s' -c copy -map 0 -f segment -segment_time 600 -segment_format mp4 '/tmp/out.mp4'" % (streamUrl)
				self.logging.debug(command)
		except:
			self.logging.debug("Error: unable to fecth data")

		self.db.close()