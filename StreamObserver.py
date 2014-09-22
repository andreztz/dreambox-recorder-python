#!/usr/bin/python
import sys
import logging
import ConfigParser

from lib.Daemon import Daemon
from lib.Observer import Observer
from lib.Consumer import Consumer

# configuration
config = ConfigParser.ConfigParser()
config.read('config.cfg')

# read daemon configuration
PIDFILE = config.get('daemon', 'PIDFILE')
LOGFILE = config.get('daemon', 'LOGFILE')
print PIDFILE
# Configure logging
logging.basicConfig(filename=LOGFILE,level=logging.DEBUG)
logging.captureWarnings(True)

# main loop
if __name__ == "__main__":

	streamObserver = Observer(PIDFILE)
	
	# start|stop|restart|status
	if len(sys.argv) >= 2:
		# start daemon
		if 'start' == sys.argv[1]:
			print "Starting ..."
			try:
				 # set host and port for listener socket
				streamObserver.init(logging)
				streamObserver.setOutputPath(config.get('main', 'OUTPUT_PATH'))
				streamObserver.start()
				
			except:
				pass

		# stop daemon
		elif 'stop' == sys.argv[1]:
			print "Stopping ..."
			streamObserver.stop()

		# restart daemon
		elif 'restart' == sys.argv[1]:
			print "Restaring ..."
			streamObserver.restart()

		# show status
		elif 'status' == sys.argv[1]:
			try:
				pf = file(PIDFILE, 'r')
				pid = int(pf.read().strip())
				pf.close()

			except IOError:
				pid = None

			except SystemExit:
				pid = None

			if pid:
				print '%s is running as pid %s' % (sys.argv[0], pid)

			else:
				print '%s is not running.' % sys.argv[0]

		else:
			print "Unknown command"
			sys.exit(2)

	else:
		print "usage: %s start|stop|restart|status %s" %(sys.argv[0], daemon)
		sys.exit(2)


