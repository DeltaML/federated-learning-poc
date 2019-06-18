import logging
import requests


class ModelBuyerConnector:

    def __init__(self, model_buyer_port):
        self.model_buyer_port = model_buyer_port
        self.remote_address = "cte_model_buyer"  # TODO: SACAR ESTA NEGREADA

    def send_result(self, result):
        url = "http://{}:{}/model/{}".format(self.remote_address, self.model_buyer_port, result['model_id'])
        logging.info("url {}".format(url))
        requests.put(url, json=result)

    def send_partial_result(self, result):
        url = "http://{}:{}/model/{}".format(self.remote_address, self.model_buyer_port, result['model_id'])
        logging.info("url {}".format(url))
        logging.info("Partials {}".format(result))
        requests.patch(url, json=result)

    def send_encrypted_prediction(self, model, encrypted_prediction):
        """
        {'model_id': self.model_id,
         'prediction_id': self.id,
         'encrypted_prediction': Data Owner encrypted prediction,
         'public_key': Data Owner PK}
        :param model:
        :param encrypted_prediction:
        :return:
        """
        url = "http://{}:{}/transform".format(model.remote_address, self.model_buyer_port, model.model_id)
        logging.info("Url {}".format(url))
        requests.post(url, json=encrypted_prediction)
