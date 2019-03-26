import requests


class ServerService:

    def __init__(self, config):
        self.server_host = config['SERVER_HOST']

    def register(self, client_data):
        """
        Register client on federated server
        :param client_data:
        :return:
        """
        server_register_url = self.server_host + "/clients/register"
        return requests.post(server_register_url, data=client_data).raise_for_status()
