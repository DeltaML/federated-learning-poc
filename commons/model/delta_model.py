import numpy as np


class DeltaModel(object):
    def __init__(self, X=None, y=None):
        self.X, self.y = X, y
        self.weights = np.zeros(X.shape[1]) if X is not None else None

    def set_data(self, X, y):
        self.X, self.y = X, y
        self.weights = np.zeros(X.shape[1])

    def set_weights(self, weights):
        self.weights = weights

    def fit(self, n_iter, eta=0.01):
        pass

    def predict(self, X):
        pass
