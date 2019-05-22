import uuid


class Prediction:
    def __init__(self, values, mse=None, model=None):
        self.id = str(uuid.uuid1())
        self.model = model
        self.values = values
        self.mse = mse

    def get_values(self):
        """
        TODO: Refactor this!
        :return:
        """
        return self.values.tolist()
