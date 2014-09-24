# Livestream Consumer in python for the raspberry-pi

This is the livestream consumer which is able to save the streams locally.
Its taking care of your choice you did in the web-ui: https://github.com/claudio-walser/dreambox-recorder


## Dependencies
 - python >= 2.5.x
 - python-urllib3
 - python-mysqldb
 - cvlc

## Installation
...

## Usage
    python /Path/To/Your/CodeBase/StreamObserver.py (start|stop|restart|status)

## Issues
It DOES NOT work on the raspberry with cvlc, because of lack of hardware acceleration in order to use the gpu for rendering...
Seems omxplayer is able to use the gpu on a raspberry, have to dig into that...
