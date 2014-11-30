import sys, time
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from ScannerServer import ScannerMainWindow

if __name__ == '__main__':
	app = QApplication(sys.argv)
	mw = ScannerMainWindow()
	mw.show()
	sys.exit(app.exec_())