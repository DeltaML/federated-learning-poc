from data_owner.service.data_owner import DataOwner


class Validator(DataOwner):

    def __init__(self, config, data_loader, encryption_service):
        self.__init__(config, data_loader, encryption_service)


class ValidatorFactory:
    @classmethod
    def create_validator(cls, name, data_loader, encryption_service):
        """
        :param name:
        :param data_loader:
        :param encryption_service:
        :return:
        """
        return Validator(name, data_loader, encryption_service)