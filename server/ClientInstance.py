class ClientInstance(object):
	def __init__(self, data, pub_key):
		self.id = data["id"]
		self.ip = data["ip"]
		self.port = data["port"]
		self.pub_key = pub_key

	def __str__(self):
		client = {}
		client["id"] = self.id
		client["ip"] = self.ip
		client["port"] = self.port
		client["pub_key"] = self.pub_key
		return str(client)