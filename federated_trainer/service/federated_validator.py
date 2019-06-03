from functools import reduce
from commons.model.model_service import ModelFactory

class FederatedValidator(object):

    def __init__(self):
        # This dict has the accumulated difference between the subsequent mse between the y_pred for each data_owner
        # contribution to the global model and the y_test
        self.acc_diff_error_by_owner = {}

    def update_data_owner_contribution(self, averaged_updates, data_owner_updates, data_owner, X_test, y_test, model_type):
        """
        This method stores the accumulated difference between the mse calculated for the model trained by each
        data owner, and the mse calculated for the averaged (global) model. This difference will, later, be used to
        calculate the contribution of each data owner to the training of the model.
        :param global_model:
        :param data_owner_model:
        :param data_owner:
        :param X_test:
        :param y_test:
        :return:
        """
        if data_owner not in self.acc_diff_error_by_owner:
            self.acc_diff_error_by_owner[data_owner] = 0
        data_owner_model = ModelFactory.get_model(model_type)()
        data_owner_model.set_weights(data_owner_updates)
        global_model = ModelFactory.get_model(model_type)()
        global_model.set_weights(averaged_updates)
        data_owner_mse = data_owner_model.predict(X_test, y_test).mse
        global_mse = global_model.predict(X_test, y_test).mse
        print("DataOwner {} mse: {}".format(data_owner, data_owner_mse))
        print("GlobalModel mse: {}".format(global_mse))
        self.acc_diff_error_by_owner[data_owner] += data_owner_mse - global_mse
        print("Diff DataOwner {}: {}".format(data_owner, self.acc_diff_error_by_owner[data_owner]))

    def get_data_owners_contribution(self):
        """
        Calculates the total contribution that each data owner made in the training of the model.
        First makes all the diffs positive by adding them the minimum diff if there is at least one negative.
        Then calculates the proportion that each diff represent regarding the sum of all diffs.
        That proportion will be the contribution, and its range is [0, 1]
        :return:
        """
        diffs = self.acc_diff_error_by_owner.values()
        min_diff = min(diffs)
        if min_diff < 0:
            for data_owner in self.acc_diff_error_by_owner:
                self.acc_diff_error_by_owner[data_owner] += abs(min_diff)
        sum_diff = sum(diffs)
        contribution = {}
        for data_owner in self.acc_diff_error_by_owner:
            contribution[data_owner] = self.acc_diff_error_by_owner[data_owner] / float(sum_diff)
        print("Contributions", contribution)
        return contribution
