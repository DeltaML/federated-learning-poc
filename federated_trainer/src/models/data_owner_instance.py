class DataOwnerInstance(object):
    def __init__(self, data):
        self.id = data["id"]
        self.host = data["host"]
        self.port = data["port"]

    def __str__(self):
        return str({"id": self.id, "host": self.host, "port": self.port})
