import ConfigParser
import os

class ConfigManager():
	def __init__(self):
		self.config = ConfigParser.RawConfigParser()
		self.config.read('conf/configs.cfg')

		if not os.path.isfile('conf/configs.cfg'):
			self.createConfFile()

	def getConfFilePath(self):
		dirname = os.path.dirname(__file__)
		if dirname == "src":
			return '../conf/configs.cfg'
		else:
			return '/home/max/TF/NetworkManagmentTool/conf/configs.cfg'

	def createConfFile(self):
		#create config file
		self.config.add_section('logging')
		self.config.add_section('server')
		self.config.set('server', 'host', 'localhost')
		self.config.set('server', 'port', '50999')
		self.config.set('server','storage','data/OpenPorts')
		self.config.add_section('client')
		self.config.set('client','ip','localhost')
		
		with open('conf/configs.cfg', 'wb') as configfile:
			self.config.write(configfile)

	def getClientIp(self):
		return self.config.get('client','ip')

	def getSaveFile(self):
		return self.config.get('server','storage')

	def getServerHost(self):
		return self.config.get('server','host')

	def getServerPort(self):
		return int(self.config.get('server','port'))
