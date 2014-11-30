#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

sock = socket.socket()
sock.connect(('localhost', 50999))

while True:
	exit=False
	data = sock.recv(1024)
	print data

	if data:
		text = raw_input("Enter text:")
		if text == "close":
			sock.send(text)
			sock.close()
			exit=True
		elif text=='show':
			continue
		else:
			sock.send(text)
			print 'Waiting for response...'
			continue
	if exit:
		break


sock.close()
