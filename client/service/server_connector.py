import requests
import logging


class ServerConnector:

    def __init__(self, config):
        self.server_host = config['SERVER_HOST']

    def register(self, client_data):
        """
        Register client on federated server
        :param client_data:
        :return:
        """
        server_register_url = self.server_host + "/clients/register"
        logging.info("Register client {} to server {}".format(client_data, server_register_url))
        response = requests.post(server_register_url, json=client_data)
        response.raise_for_status()
        return response.json()
