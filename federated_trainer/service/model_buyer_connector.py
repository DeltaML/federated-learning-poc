import logging
import requests


class ModelBuyerConnector:

    def __init__(self, model_buyer_port):
        self.model_buyer_port = model_buyer_port
        self. remote_address = None
        self.model_id = None

    def set_remote_buyer_data(self, remote_address, model_id):
        self.remote_address, self.model_id = remote_address, model_id

    def send_result(self, result):
        url = "http://{}:{}/model/{}".format(self.remote_address, self.model_buyer_port, self.model_id)
        logging.info("url {}".format(url))
        requests.put(url, json=result)

    def send_partial_result(self, result):
        url = "http://{}:{}/model/{}".format(self.remote_address, self.model_buyer_port, self.model_id)
        logging.info("url {}".format(url))
        logging.info("PArtials {}".format(result))
        requests.patch(url, json=result.tolist())
