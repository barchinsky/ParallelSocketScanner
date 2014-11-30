import sys, time
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ConfigManager import ConfigManager
import socket
import threading

from Engine import Engine

class ScannerMainWindow(QWidget):
	def __init__(self,parent=None):
		super(ScannerMainWindow,self).__init__(parent)

		self.engine = Engine(self)

		self.setMinimumSize(850,200)

		cfg = ConfigManager()
		self.currentRowIndex = 0

		self.headerCount = 5
		header = QStringList()
		header = ["Client adress","Connection status","Thread number","Requested host","Request status"]

		self.tableView = QTableWidget(10,5)
		closeBtn = QPushButton("Exit")

		for section in xrange(self.headerCount):
			self.tableView.horizontalHeader().resizeSection(section,150)

		self.tableView.setHorizontalHeaderLabels(header)

		layout = QGridLayout()
		layoutH = QHBoxLayout()

		layout.addWidget(self.tableView)
		layout.addWidget(closeBtn,1,2)

		self.setLayout(layout)

		self.connect(closeBtn,SIGNAL("clicked()"),self,SLOT("close()"))

		print "Active threads:",threading.activeCount()

		self.engine_thread = threading.Thread(target=self.engine.run)
		self.engine_thread.daemon = True
		self.engine_thread.start()

	@pyqtSlot()
	def addItem(self,data=["0","0","0","0","0"]):
		print "addItem()"
		for item in xrange(self.headerCount):
			self.tableView.setItem(self.currentRowIndex,item,QTableWidgetItem(data[item]))
		self.currentRowIndex+=1

	@pyqtSlot()
	def close(self):
		sys.exit()


	def stopEngine(self):
		try:
			self.engine_thread.terminate()
		except:
			print "Something goes wrong"

	def getCurrentRowIndex(self):
		return self.currentRowIndex

	def updateItem(self,row,column,data):
		self.tableView.item(row,column).setText(data)

	def updateCurrentRowIndexWhere(self,key,value):
		for index in xrange(self.getCurrentRowIndex()):
			if self.tableView.item(index,0).text() == key:
				self.tableView.item(index,1).setText(value)
