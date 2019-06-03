import requests
import logging


class FederatedTrainerConnector:
    def __init__(self, config):
        self.config = config
        self.federated_trainer_host = config['FEDERATED_TRAINER_HOST']

    def send_model_order(self, data):
        server_register_url = self.federated_trainer_host + "/model"
        response = requests.post(server_register_url, json=data)
        response.raise_for_status()

    def send_transformed_prediction(self, prediction):
        server_register_url = self.federated_trainer_host + "/prediction"
        logging.info("Send prediction")
        response = requests.post(server_register_url, json=prediction.get_data()).raise_for_status()
        return response.json()
