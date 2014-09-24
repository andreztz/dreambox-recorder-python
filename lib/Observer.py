#!/usr/bin/env python

import sys
import MySQLdb
import time
import urllib3
from Daemon import Daemon
from Consumer import Consumer

class Observer(Daemon):
	
	db = False
	cursor = False
	logging = False
	outputPath = '/tmp/'
	checkInterval = 5
	recording = False
	consumer = False

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

	#def stopConsumer(self, logging):
	#	logging.debug('stop consumer now')
	#	logging.debug(self.consumer)
	#	if self.consumer != False:
	#		self.consumer.stopRecording()

	# check db and livestream match, if you hit one, start recording till end
	def listen(self):
		self.logging.debug('Listen')
		currentTime = int(time.time())
		# if stream consumer is running, cut it here already...
		if self.recording == True:
			self.logging.debug('Its recording right now')
			self.logging.debug(self.consumer.getProcess())
			
			if currentTime >= self.consumer.getTimeEnd():
				self.logging.debug(self.consumer.getTimeEnd())
				self.logging.debug(currentTime)

				# see here tomorrow
				self.consumer.stopRecording()
				self.recording = False

			return

		self.db = MySQLdb.connect("localhost","root","","dreambox-recorder")
		self.cursor = self.db.cursor()

		timeMin = currentTime - 5
		timeMax = currentTime + 5
		sql = "SELECT * FROM recording WHERE state='waiting' AND (timeStart <= %i AND timeEnd >= %i)" % (timeMin, timeMax)
		try:
			self.cursor.execute(sql)
			results = self.cursor.fetchall()
			for row in results:
				id = row[0]
				token = row[1]
				timeEnd = row[4]
				streamUrl = 'http://10.20.0.99/web/stream.m3u?ref=%s' % (token)
				zapUrl = 'http://10.20.0.99/web/zap?sRef=%s&title=PythonRecording-DontChangeChannelPlease' % (token)
				http = urllib3.PoolManager()
				request = http.request('GET', zapUrl)
				
				outfile = '/home/claudio/aufnahmen/%s.mkv' % (id)
				self.consumer = Consumer(self.logging)
				self.consumer.setStream(streamUrl)
				self.consumer.setOutfile(outfile)
				self.consumer.setTimeEnd(timeEnd)
				status = self.consumer.record()
				status = True
				if status == True:
					self.recording = True
					self.logging.debug('recording now')

				self.logging.debug(status)
		except Exception, e:
			self.logging.debug("<p>Error: %s</p>" % e)

		self.db.close()