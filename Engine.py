#!/usr/bin/env python
import socket              
import time
import threading
import re

from ConfigManager import ConfigManager


class Engine():
	def __init__(self,scannerMainWindow):
		cfg = ConfigManager()
		self.mw = scannerMainWindow

		self.threads = []

		self.host = cfg.getServerHost()
		self.port = cfg.getServerPort()

		self.threadCount = 0

		self.ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.ssocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.ssocket.bind((self.host, self.port))       
		self.ssocket.listen(5)

	def start(self):
		adress = []
		while True:
			event = threading.Event()
			print 'Panding'
			conn, addr = self.ssocket.accept()
			self.threadCount += 1
			print 'Accepted'
			if addr not in adress:
				adress.append(addr)
				print addr
			self.server_thread = threading.Thread(target=self.session, args=(conn,addr))
			self.threads.append(self.server_thread)
			self.server_thread.daemon = True
			self.server_thread.start()
			print 'Thread number:%d started.'%(self.threadCount)
		self.ssocket.close()

	def run(self):
		self.start()

	def session(self,conn, addr):
		isActive = True
		self.currentRowNumber = 0
		self.addedRecordsIndexList = []
		threadNumber = self.threadCount
		print 'Session:request goted.'
		while True:
		    print 'Got connection from', addr
		    conn.send("Connected successful.")

		    while True:
		    	msg = conn.recv(1024)
		      	if not msg:
		        	conn.close()
		        	print "No message"
		        	self.threadCount-=1
		        	isActive=False
		        	self.updateDataOnConnectionLost(isActive,addr)
		        	return
		        #break
		      	elif msg == "close":
		        	print ("Connection with %s was closed by the client." % (addr[0]))
		        	conn.close()
			        self.threadCount-=1
			        isActive=False
			        self.updateDataOnConnectionLost(isActive,addr)
		        	return
		      	else:
		        	print "%s: %s" % (addr[0], msg)
		        	#conn.send("Processing request...")
		        	self.processRequest(addr,isActive,msg,threadNumber,conn)
		        	pass


	def processRequest(self,addr,status,msg,threadNum,conn):
		# "Client adress","Connection status","Thread number","Requested host","Request status" // table column order
		adress = addr
		connStatus = status
		requestedHost = msg
		requestStatus = ['Success','Failed (Reason: Bad host)']
		addrStr = str(adress[0])+" "+str(adress[1])

		self.currentRowNumber = self.mw.getCurrentRowIndex()
		print "Row number before insert",self.currentRowNumber

		self.mw.addItem( (addrStr,("Closed","Active")[status],str(threadNum),msg,("Failed (Bad host name)","Success")[self.isValidHost(msg)]) )

		self.addedRecordsIndexList.append(self.currentRowNumber)

		if self.isValidHost(msg):
			openPorts = self.scanHost(msg)
			conn.send("There is %d open ports at %s"%(len(openPorts),msg))
		else:
			conn.send("Bad host name. Try again, please.")



	def updateDataOnConnectionLost(self,status,adress):
		print "updateDataOnConnectionLost"
		print "addedRecordsIndexList",len(self.addedRecordsIndexList)
		self.mw.updateCurrentRowIndexWhere(str(adress[0])+" "+str(adress[1]),"Closed")


	def isValidHost(self,host):
		print "isValidHost",host
		if host == "localhost":
			return True
		else:
			template = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
			return bool(template.match(host))

	def scanHost(self,host):
		openPorts = []
		for port in xrange(65000):
			sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			sock.settimeout(0.1)
			if not sock.connect_ex((host,port)):
				#print("Port %s is closed" % port )
				pass
			else:
				openPorts.append(port)
				#print("Port %s is open" % port)
				sock.close()
		return openPorts

if __name__ == '__main__':
	engine = Engine()
	engine.start()