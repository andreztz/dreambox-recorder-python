#!/usr/bin/env python

import sys
import MySQLdb
import time
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
		self.db = MySQLdb.connect("localhost","root","","dreambox-recorder")
		self.cursor = self.db.cursor()
		# you seriously have to optimize this
		sql = "SELECT * FROM recording WHERE state='waiting'"
		try:
			self.cursor.execute(sql)
			results = self.cursor.fetchall()
			for row in results:
				id = row[0]
				token = row[1]
				# check if startTime is around current time (closer than (self.checkInterval) seconds) - could be done already in the query
				## only if statement from top was true
				# check if livestream state is already recording - its not due to the query
				# start recording and update state - Within consumer class
				# save stream using https://pypi.python.org/pypi/hlsclient and ffmpeg
				self.logging.debug("start livestream consumer for given token: %s" % (token))
		except:
			self.logging.debug("Error: unable to fecth data")

		self.db.close()