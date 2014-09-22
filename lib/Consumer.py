#!/usr/bin/env python

class Consumer():
	
	logging = False

	def init(self, logging = False):
		self.setLogging(logging)

	# set logging object for debug purpose
	def setLogging(self, logging):
		self.logging = logging
