import logging
import json
from functools import reduce
from threading import Thread

from commons.decorators.decorators import normalize_optimized_response
from commons.operations_utils.functions import sum_collection
from federated_trainer.models.data_owner_instance import DataOwnerInstance
from federated_trainer.service.data_owner_connector import DataOwnerConnector
from federated_trainer.service.decorators import serialize_encrypted_server_data
from federated_trainer.service.model_buyer_connector import ModelBuyerConnector
from federated_trainer.service.federated_validator import FederatedValidator
from commons.model.model_service import ModelFactory
import numpy as np


class GlobalModel:
    def __init__(self, buyer_id, buyer_host, model_id, public_key, model_type, local_trainers, validators, model):
        self.buyer_id = buyer_id
        self.model_id = model_id
        self.buyer_host = buyer_host
        self.public_key = public_key
        self.model_type = model_type
        self.local_trainers = local_trainers
        self.validators = validators
        self.model = model


class FederatedTrainer:
    def __init__(self, encryption_service, config):
        self.data_owners = {}
        self.encryption_service = encryption_service
        self.config = config
        self.active_encryption = self.config["ACTIVE_ENCRYPTION"]
        self.data_owner_connector = DataOwnerConnector(self.config["DATA_OWNER_PORT"], encryption_service, self.active_encryption)
        self.model_buyer_connector = ModelBuyerConnector(self.config["MODEL_BUYER_PORT"])
        self.global_models = {}

    def register_data_owner(self, data_owner_data):
        """
        Register new data_owner
        :param data_owner_data:
        :return:
        """
        logging.info("Register data owner with {}".format(data_owner_data))
        new_data_owner = DataOwnerInstance(data_owner_data)
        self.data_owners[new_data_owner.id] = new_data_owner
        return {'data_owner_id': len(self.data_owners) - 1}

    def send_requirements_to_data_owner(self, data):
        return self.data_owner_connector.send_requirements_to_data_owners(list(self.data_owners.values()), data)

    def async_server_processing(self, func, *args):
        logging.info("process_in_background...")
        result = func(*args)
        self.model_buyer_connector.send_result(result)

    def process(self, remote_address, data):
        Thread(target=self.async_server_processing, args=self._build_async_processing_data(data, remote_address)).start()

    def _build_async_processing_data(self, data, remote_address):
        data["remote_address"] = remote_address
        return self.federated_learning_wrapper, data

    def _link_data_owners_to_model(self, data):
        """
        Recevies a data structure that contains the requirements over the data needed for training the model.
        Sends these requirements to the data owners. They respond each with a true if they have data that complies with
        the reqs. and false if they don't.
        This method returns a list of the data owners that have the previosly mentioned data.
        :param data:
        :return:
        """
        linked_data_owners = []
        owners_with_data = self.send_requirements_to_data_owner(data)
        for data_owner_link in owners_with_data:
            if (data['model_id'] in data_owner_link) and (data_owner_link[data['model_id']][1]):
                data_owner_key = data_owner_link[data['model_id']][0]
                linked_data_owners.append(self.data_owners[data_owner_key])
        return linked_data_owners

    def split_data_owners(self, linked_data_owners):
        """
        Receives a list of data owners linked to a model_id. Returns two lists.
        The firsts contains the data owners that will participate training the model.
        The second contains the ones that will validate the training.
        :param linked_data_owners:
        :return: Two lists of data owners. The trainers and the validators-
        """
        split_index = int(len(linked_data_owners) * 0.70) + 1
        import random
        copy = linked_data_owners[:]
        random.shuffle(copy)
        return copy[:split_index], copy[split_index:]

    @normalize_optimized_response(active=True)
    def federated_learning(self, data):
        logging.info("Init federated_learning")
        n_iter = self.config["MAX_ITERATIONS"]
        n_iter_partial_res = self.config["ITERS_UNTIL_PARTIAL_RESULT"]
        model_id = data['model_id']
        linked_data_owners = self._link_data_owners_to_model(data)
        local_trainers, validators = self.split_data_owners(linked_data_owners)
        model = ModelFactory.get_model(data["requirements"]["model_type"])()
        model.set_weights(data["model"])
        self.global_models[model_id] = GlobalModel(model_id=model_id,
                                                   buyer_id=data["model_buyer_id"],
                                                   buyer_host=data["remote_address"],
                                                   public_key=data["public_key"],
                                                   model_type=data['requirements']['model_type'],
                                                   local_trainers=local_trainers,
                                                   validators=validators,
                                                   model=model)
        logging.info('Running distributed gradient aggregation for {:d} iterations'.format(n_iter))
        self.encryption_service.set_public_key(data["public_key"])
        validator = FederatedValidator()
        models = []
        averaged_updates = None
        for i in range(1, n_iter+1):
            model = self.training_cicle(self.global_models[model_id], averaged_updates, n_iter_partial_res, i)

        return {'model': model, 'model_id': model_id}

    def training_cicle(self, model_data, averaged_updates, n_iter_partial_res, i):
        gradients, owners = self.get_updates(model_data)
        print("Updates", gradients)
        print("DataOwners", owners)
        #if i > 1:
            #self.update_data_owners_contribution(updates, averaged_updates, owners, validator, X_test, y_test, model_type)
        avg_gradient = self.federated_averaging(gradients, model_data)
        self.send_global_model(avg_gradient, model_data)
        #if (i % n_iter_partial_res) == 0:
            #contribution = validator.get_data_owners_contribution()
            #self.send_partial_result_to_model_buyer(averaged_updates, model_type, X_test, y_test, contribution, model_id)
        #models = self.get_trained_models(model_data)
        model_data.model.gradient_step(avg_gradient, 1.5)
        print("Model {}".format(model_data.model.weights))
        return model_data.model.weights


    def update_data_owners_contribution(self, updates, averaged_updates, owners, validator, X_test, y_test, model_type):
        for i in range(len(updates)):
            validator.update_data_owner_contribution(averaged_updates, updates[i], owners[i], X_test, y_test, model_type)

    def validate_against_model_buyer_test_data(self, updates, model_type, X_test, y_test):
        partial_model = ModelFactory.get_model(model_type)()
        partial_model.set_weights(updates)
        return partial_model.predict(X_test, y_test).mse

    def send_partial_result_to_model_buyer(self, updates, model_type, X_test, y_test, mse_n, model_id):
        mse = self.validate_against_model_buyer_test_data(updates, model_type, X_test, y_test)
        partial_result = {'model': updates.tolist(), 'mse': mse, 'mse_n': mse_n, 'model_id': model_id}
        self.model_buyer_connector.send_partial_result(partial_result)

    @serialize_encrypted_server_data(schema=json.dumps)
    def federated_learning_wrapper(self, data):
        return self.federated_learning(data)

    def send_global_model(self, weights, model_data):
        """Encripta y envia el modelo a ser entrenado"""
        logging.info("Send global models")
        self.data_owner_connector.send_gradient_to_data_owners(model_data.local_trainers, weights)

    def get_updates(self, model_data):
        """
        :param model_type:
        :param public_key:
        :param model_id
        :return:
        """
        model_type = model_data.model_type
        model_id = model_data.model_id
        public_key = model_data.public_key
        local_trainers = model_data.local_trainers
        updates, owners = self.data_owner_connector.get_update_from_data_owners(local_trainers, model_type, public_key, model_id)
        return updates, owners

    def federated_averaging(self, updates, model_data):
        """
        Sum all de partial updates and
        :param model_data:
        :param updates:
        :return:
        """
        logging.info("Federated averaging")
        return reduce(sum_collection, updates) / len(model_data.local_trainers)

    def get_trained_models(self, model_data):
        """obtiene el nombre del modelo a ser entrenado"""
        logging.info("get_trained_models")
        return self.data_owner_connector.get_data_owners_model(model_data.local_trainers)

    def send_prediction_to_buyer(self, data):
        """
        :param data:
        :return:
        """
        self.model_buyer_connector.send_encrypted_prediction(self.global_models[data["model_id"]], data)

    def send_prediction_to_data_owner(self, encrypted_prediction):
        model = self.global_models[encrypted_prediction["model_id"]]
        self.data_owner_connector.send_encrypted_prediction(data_owner=model.data_owner,
                                                            encrypted_prediction=encrypted_prediction)
