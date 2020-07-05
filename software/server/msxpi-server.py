# External module imports
import RPi.GPIO as GPIO
import time
import subprocess
import urllib2
import mmap
import fcntl,os
import sys
from subprocess import Popen,PIPE,STDOUT
from HTMLParser import HTMLParser
import datetime
import time
import glob
import array
import socket
import errno
import select
import base64
from random import randint

version = "0.1"
build   = "20200704.00000"
TRANSBLOCKSIZE = 1024

# Pin Definitons
d0 = 27
d1 = 28
d2 = 3
d3 = 5
d4 = 7
d5 = 29
d6 = 31
d7 = 26

a0 = 24
a1 = 21
a2 = 19
a3 = 23
a4 = 32
a5 = 33
a6 = 8
a7 = 10
a8 = 36
a9 = 11
a10 = 12
a11 = 35
a12 = 38
a13 = 15

cs = 40
wr = 16
io = 18
rdy = 22
res1 = 37
res2 = 13

def init_gpio():
# Pin Setup:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(cs, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(rdy, GPIO.OUT)
    GPIO.setup(wr, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(io, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(res1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(res2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(d0, GPIO.IN)
    GPIO.setup(d1, GPIO.IN)
    GPIO.setup(d2, GPIO.IN)
    GPIO.setup(d3, GPIO.IN)
    GPIO.setup(d4, GPIO.IN)
    GPIO.setup(d5, GPIO.IN)
    GPIO.setup(d6, GPIO.IN)
    GPIO.setup(d7, GPIO.IN)
    GPIO.setup(a0, GPIO.IN)
    GPIO.setup(a1, GPIO.IN)
    GPIO.setup(a2, GPIO.IN)
    GPIO.setup(a3, GPIO.IN)
    GPIO.setup(a4, GPIO.IN)
    GPIO.setup(a5, GPIO.IN)
    GPIO.setup(a6, GPIO.IN)
    GPIO.setup(a7, GPIO.IN)
    GPIO.setup(a8, GPIO.IN)
    GPIO.setup(a9, GPIO.IN)
    GPIO.setup(a10, GPIO.IN)
    GPIO.setup(a11, GPIO.IN)
    GPIO.setup(a12, GPIO.IN)
    GPIO.setup(a13, GPIO.IN)

def spi_transfer(byte_out=0):
    addr = 0
    data = 0
    wr_n = 0
    rd_n = 0
    iorq_n = 0
    mreq_n = 0

    # read A bus
    for bit in [a13,a12,a11,a10,a9,a8,a7,a6,a5,a4,a3,a2,a1,a0]:
        print bit
        addr = addr << 1
        addr = addr | GPIO.input(bit)

    # read D bus
    for bit in [d7,d6,d5,d4,d3,d2,d1,d0]:

        data = data << 1
        data = data | GPIO.input(bit)

    wr_n = GPIO.input(wr)
    rd_n = not wr_n
    mreq_n = GPIO.input(io)
    iorq_n = not mreq_n

    print("Address:",hex(addr))
    print("data:",hex(data))
    print("wr_n:",hex(wr_n))
    print("rd_n:",hex(rd_n))
    print("mreq_n:",hex(mreq_n))
    print("iorq_n:",hex(iorq_n))

    return addr,data,wr_n,rd_n,iorq_n,mreq_n

""" ============================================================================
    msxpi-server.py
    main program starts here
    ============================================================================
"""

def callback_gpio(channel):
    GPIO.output(rdy, GPIO.LOW)
    print("*")
    global interrupt, msx_address,bytein, byteout
    # "r" receive data from MSX
    msx_busddata = spi_transfer()

    print(hex(msx_busddata))

    print("-")
    GPIO.output(rdy, GPIO.HIGH)

init_gpio()
GPIO.add_event_detect(cs, GPIO.RISING, callback=callback_gpio)
GPIO.output(rdy, GPIO.HIGH)
print "GPIO Initialized\n"
print "Starting MSXPi2 Server Version ",version,"Build",build

print "st_recvcmd: waiting command"
try:
    while 1:
        pass

except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
   print("Keyboard interrupt")
   GPIO.cleanup() 

