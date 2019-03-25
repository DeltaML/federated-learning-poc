class ClientInstance():
	def __init__(data, pub_key):
		self.id = data.id
		self.ip = data.ip
		self.port = data.port
		self.pub_key = data.pub_key