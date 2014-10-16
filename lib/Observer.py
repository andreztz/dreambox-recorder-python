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
		# maybe i can fetch the cursor here, since i now i have to commit after a update, it might work :p
		while True:
			#accept connections from outside
			self.listen()
			time.sleep(self.checkInterval)

	# check db and livestream match, if you hit one, start recording till end
	def listen(self):
		self.logging.debug('Listen')
		currentTime = int(time.time())
		# if stream consumer is running, cut it here already...
		if self.recording == True:
			self.logging.debug('Its recording right now')
			self.logging.debug(self.consumer.getProcess())
			
			if currentTime >= self.consumer.getTimeEnd():
				db = MySQLdb.connect("localhost","root","","dreambox-recorder")
				cursor = db.cursor()
				sql = "UPDATE `recording` set `state`='recorded', file='%s' WHERE id=%s " % (self.consumer.getOutfile(), self.consumer.getId())
				cursor.execute(sql)
				db.commit()
				cursor.close()
				db.close()

				self.consumer.stopRecording()
				self.recording = False

			return

		timeMin = currentTime - 5
		timeMax = currentTime + 5
		
		
		try:
			db = MySQLdb.connect("localhost","root","","dreambox-recorder")
			cursor = db.cursor()
			sql = "SELECT * FROM `recording` WHERE `state`='waiting' AND (timeStart <= %i AND timeEnd >= %i)" % (timeMin, timeMax)
			cursor.execute(sql)
			row = cursor.fetchone()
			self.logging.debug(type(row))
			if isinstance(row, tuple):
				cursor.close()
				db.close()
				id = row[0]
				token = row[1]
				timeEnd = row[4]
				title = row[7]
				channel = row[8]
				streamUrl = 'http://10.20.0.99/web/stream.m3u?ref=%s' % (token)
				zapUrl = 'http://10.20.0.99/web/zap?sRef=%s&title=PythonRecording-DontChangeChannelPlease' % (token)
				http = urllib3.PoolManager()
				request = http.request('GET', zapUrl)
				# TODO: use title, channel and date in outfile for better identification
				outfile = 'file/mpg:/home/claudio/aufnahmen/%s.mpg' % (id)
				self.consumer = Consumer(self.logging)
				self.consumer.setStream(streamUrl)
				self.consumer.setOutfile(outfile)
				self.consumer.setTimeEnd(timeEnd)
				self.consumer.setId(id)
				status = self.consumer.record()

				if status == True:
					db = MySQLdb.connect("localhost","root","","dreambox-recorder")
					cursor = db.cursor()
					sql = "UPDATE `recording` set `state`='recording' WHERE id=%s " % (self.consumer.getId())
					cursor.execute(sql)
					db.commit()
					cursor.close()
					db.close()

					self.recording = True
					self.logging.debug('recording now')

		except Exception, e:
			self.logging.debug("<p>Error: %s</p>" % e)