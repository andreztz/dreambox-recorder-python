#!/usr/bin/env python
import subprocess

class Consumer():
	
	logging = False
	stream = ''
	outfile = '/tmp/tmp.mkv'
	process = False
	timeEnd = 0

	def __init__(self, logging):
		self.logging = logging

	# set logging object for debug purpose
	def record(self):
		#self.logging.debug(self.stream)
		#command = "cvlc %s --sout file/mkv:%s" % (self.stream, self.outfile)
		
		command = [
			"cvlc",
			self.stream,
			"--sout",
			self.outfile
		]

		#process = os.execvp("cvlc", arrayArgs)
		#process = os.popen(cmd)
		self.process = subprocess.Popen(command)


		#self.process = os.popen(command)
		#self.process = 'Got me'
		self.logging.debug(self.process)
		#self.logging.debug(self.process)
		#self.logging.debug('not sure, do i wait for this process?')
		##status = subprocess.call(command, shell=True)
		
		return True

	def setStream(self, stream):
		self.stream = stream

	def setOutfile(self, outfile):
		self.outfile = outfile

	def stopRecording(self):
		self.logging.debug('stop recording process')
		try:
			self.process.terminate()
		except:
			self.logging.debug("Exception: %s" % (rc))
		
		return True

	def setTimeEnd(self, time):
		self.timeEnd = time

	def getTimeEnd(self):
		return self.timeEnd

	def getProcess(self):
		return self.process