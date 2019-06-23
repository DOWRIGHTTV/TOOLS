#!/usr/bin/python3

from contextlib import closing
from socket import socket, AF_INET, SOCK_DGRAM
import sys
import struct
import time


def getNTPTime(host = "192.168.2.74"):
		port = 123
		buf = 1024
		address = (host,port)
		msgstr = '\x1b' + 47 * '\0'
		msg = msgstr.encode()

		# reference time (in seconds since 1900-01-01 00:00:00)
		TIME1970 = 2208988800 # 1970-01-01 00:00:00

		# connect to server
		client = socket( AF_INET, SOCK_DGRAM)
		client.sendto(msg, address)
		msg, address = client.recvfrom( buf )

		t = struct.unpack( "!12I", msg )[10]
		t -= TIME1970

		return time.ctime(t).replace("  "," ")

if __name__ == "__main__":
		print(getNTPTime())
