import numpy as np


class LinearRegression:
    """Runs linear regression with local data or by gradient steps,
    where gradient can be passed in.

    Using public key can encrypt locally computed gradients.
    """

    def __init__(self, X, y):
        self.X, self.y = X, y
        self.weights = np.zeros(X.shape[1])

    def set_weights(self, weights):
        self.weights = weights

    def fit(self, n_iter, eta=0.01):
        """Linear regression for n_iter"""
        for _ in range(n_iter):
            gradient = self.compute_gradient()
            self.gradient_step(gradient, eta)

    def gradient_step(self, gradient, eta=0.01):
        """Update the model with the given gradient"""
        print("GRADIENT \n" + str(gradient))
        print("WEIGHTS \n" + str(self.weights))
        self.weights = self.weights - (eta * gradient)

    def compute_gradient(self):
        """Compute the gradient of the current model using the training set
        """
        delta = self.predict(self.X) - self.y
        return delta.dot(self.X) / len(self.X)

    def predict(self, X):
        """Score test data"""
        return X.dot(self.weights)
