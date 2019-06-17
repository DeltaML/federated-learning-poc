import numpy as np

from commons.decorators.decorators import optimized_collection_parameter
from commons.model.model_service import ModelFactory
from data_owner.service.data_owner import DataOwner


class LocalTrainer(DataOwner):

    def __init__(self, config, data_loader, encryption_service):
        self.__init__(config, data_loader, encryption_service)

    @optimized_collection_parameter(optimization=np.asarray, active=True)
    def step(self, step_data):
        """
        TODO: POdría evaluarse la posibilidad de que el federated local_trainer indique cuando evaluar una prediccion local
        :param encrypted_model:
        :return:
        """
        self.model.gradient_step(step_data, float(self.config['ETA']))

    def process(self, model_type, public_key):
        """
        Process to run model
        :param model_type:
        :param public_key:
        :return:
        """
        self.encryption_service.set_public_key(public_key)
        X, y = self.data_loader.get_sub_set()
        self.model = self.model if self.model else ModelFactory.get_model(model_type)(X, y)
        return self.client_id, self.model.compute_gradient().tolist()


class ValidatorFactory:
    @classmethod
    def create_local_trainer(cls, name, data_loader, encryption_service):
        """
        :param name:
        :param data_loader:
        :param encryption_service:
        :return:
        """
        return LocalTrainer(name, data_loader, encryption_service)