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
from copy import deepcopy


class GlobalModel:
    def __init__(self, buyer_id, buyer_host, model_id, public_key, model_type, local_trainers, validators, model):
        """

        :param buyer_id: String
        :param buyer_host:
        :param model_id: String
        :param public_key: String
        :param model_type: String
        :param local_trainers: List[]
        :param validators: List[]
        :param model: LinearRegression
        """
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
        """
        :param encryption_service: EncriptionService
        :param config: Dict[String, Any]
        """
        self.data_owners = {}
        self.encryption_service = encryption_service
        self.config = config
        self.active_encryption = self.config["ACTIVE_ENCRYPTION"]
        self.data_owner_connector = DataOwnerConnector(self.config["DATA_OWNER_PORT"], encryption_service, self.active_encryption)
        self.model_buyer_connector = ModelBuyerConnector(self.config["MODEL_BUYER_PORT"])
        self.global_models = {}
        self.n_iter = self.config["MAX_ITERATIONS"]
        self.n_iter_partial_res = self.config["ITERS_UNTIL_PARTIAL_RESULT"]

    def register_data_owner(self, data_owner_data):
        """
        Register new data_owner
        :param data_owner_data: Dict[String, String], Keys: id, host, port
        :return: Dict[String, Int]
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
        split_index = int(len(linked_data_owners) * 0.70)
        import random
        copy = linked_data_owners[:]
        random.shuffle(copy)
        local_trainers, validators = copy[:split_index+1], copy[split_index+1:] or []
        logging.info("LocalTrainers: {}".format(list(map(lambda x: x.id, local_trainers))))
        logging.info("Validators: {}".format(list(map(lambda x: x.id, validators))))
        return local_trainers, validators

    @normalize_optimized_response(active=True)
    def federated_learning(self, data):
        logging.info("Init federated_learning")
        model_id = data['model_id']
        linked_data_owners = self._link_data_owners_to_model(data)
        local_trainers, validators = self.split_data_owners(linked_data_owners)
        model = self.initialize_global_model(data)
        self.global_models[model_id] = GlobalModel(model_id=model_id,
                                                   buyer_id=data["model_buyer_id"],
                                                   buyer_host=data["remote_address"],
                                                   public_key=data["public_key"],
                                                   model_type=data['requirements']['model_type'],
                                                   local_trainers=local_trainers,
                                                   validators=validators,
                                                   model=model)
        logging.info('Running distributed gradient aggregation for {:d} iterations'.format(self.n_iter))
        self.encryption_service.set_public_key(data["public_key"])
        for i in range(1, self.n_iter+1):
            model, global_MSE, partial_MSEs = self.training_cicle(self.global_models[model_id], i)
        return {'model': model.weights, 'model_id': model_id, 'mse': global_MSE, 'partial_MSEs': partial_MSEs}

    def initialize_global_model(self, data):
        model = ModelFactory.get_model(data["requirements"]["model_type"])()
        model.set_weights(np.asarray(data["weights"]))
        return model

    def training_cicle(self, model_data, i):
        gradients, local_trainers = self.get_gradients(model_data)
        logging.info("Updates: {}".format(gradients))
        logging.info("LocalTrainer: {}".format(local_trainers))
        partial_models = [self.partial_update_model(deepcopy(model_data), gradients, local_trainers, i)
                          for i in range(len(local_trainers))]
        logging.info("Something")
        model_data.model.weights, avg_gradient = self.update_model(model_data, gradients)
        logging.info("Done updating model")
        if (i % self.n_iter_partial_res) == 0:
            logging.info("Sending partial results")
            self.send_partial_result_to_model_buyer(model_data, partial_models)
        logging.info("Calculating mses")
        global_MSE = self.get_model_metrics_from_validators(model_data)
        partial_MSEs = self.get_partial_model_metrics_from_validators(partial_models, model_data)
        logging.info("Validators MSEs: {}".format(global_MSE))
        logging.info("Model {}".format(model_data.model))
        self.send_avg_gradient(avg_gradient, model_data)
        return model_data.model, global_MSE, partial_MSEs

    def update_model(self, model_data, gradients):
        """
        Updates the global model by performing a gradient descent step in the direction of the avg. gradient calculated
        from the gradients received from the local trainers.
        :param model_data: a wrapper that contains all the data related to a certain model in training.
        :param gradients: a list of gradients to be averaged.
        :return: the model updated after a step of gradient descent.
        """
        logging.info("Updating global model")
        avg_gradient = self.federated_averaging(gradients, model_data)
        model_data.model.gradient_step(avg_gradient, 1.5)
        return model_data.model.weights, avg_gradient

    def partial_update_model(self, model_data, gradients, trainers, filtered_index):
        """
        Performs the same operation as the update_model method, but leaves out of the update one of the local trainers
        and its corresponding gradient. By doing that we can obtain a model that shows how better would have been to
        leave that local trainer out of the training.
        :param model_data: a wrapper that contains all the data related to a certain model in training.
        :param gradients: a list of gradients to be averaged.
        :param trainers: the list of the local trainers training local models and sending their gradients.
        :param filtered_index: the filtered local trainer and corresponding gradient.
        :return: a dictionary of models trained leaving different local trainers out. The filtered local trainers are
        the keys of the dictionary.
        """
        logging.info("Updating partial model for index {}".format(filtered_index))
        gradients = np.delete(gradients, filtered_index, 0)
        trainer = trainers[filtered_index]
        avg_gradient = self.federated_averaging(gradients, model_data)
        logging.info("Avg gradient {}".format(avg_gradient))
        model_data.model.gradient_step(avg_gradient, 1.5)
        return trainer, model_data.model.weights

    def send_partial_result_to_model_buyer(self, model_data, partial_models):
        partial_result = {'model': model_data.model.weights.tolist(), 'model_id': model_data.model_id}
        self.model_buyer_connector.send_partial_result(partial_result)

    @serialize_encrypted_server_data(schema=json.dumps)
    def federated_learning_wrapper(self, data):
        return self.federated_learning(data)

    def send_avg_gradient(self, gradient, model_data):
        """
        Sends the average gradient back to the data owners for a new gradient step.
        :param gradient: The average of the gradients received by the data owners.
        :param model_data: wrapper with data related to the current model training.
        :return: Nothing
        """
        logging.info("Send global models")
        self.data_owner_connector.send_gradient_to_data_owners(model_data.local_trainers, gradient)

    def get_gradients(self, model_data):
        """
        :param model_data: wrapper with data related to the current model training.
        :return: the gradients calculated after a gradient descent step in the data owners, and the data owners that
        performed such calculation.
        """
        gradients, owners = self.data_owner_connector.get_gradient_from_data_owners(model_data)
        return gradients, owners

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

    def get_model_metrics_from_validators(self, model_data):
        logging.info("Getting global mse")
        return self.data_owner_connector.get_model_metrics_from_validators(model_data.validators, model_data)

    def get_partial_model_metrics_from_validators(self, partial_models, model_data):
        trainers_mses = {}
        logging.info("Getting partials mses")
        for trainer, model_weights in partial_models:
            logging.info("Calculating mse for model without trainer: {}".format(trainer))
            logging.info("Model weigths without the trainer {}".format(model_weights))
            logging.info("Validators {}".format(model_data.validators))
            mses = self.data_owner_connector.get_model_metrics_from_validators(model_data.validators, model_data, model_weights)
            logging.info("MSE for model without trainer: {}".format(mses))
            avg_mse = sum(mses)/len(mses)
            trainers_mses[trainer] = avg_mse
        return trainers_mses

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
