import logging

import numpy as np
from sklearn.datasets import load_diabetes


class DataLoader:

    def __init__(self):
        self.X, self.y, self.X_test, self.y_test = None, None, None, None
        self.seed = 43
        np.random.seed(self.seed)

    def load_data(self, n_subsets):
        """
        Import the dataset via sklearn, shuffle and split train/test.
        Return training, target lists for `n_clients` and a holdout test set
        """
        logging.info("Loading data")
        diabetes = load_diabetes()
        y = diabetes.target
        X = diabetes.data
        # Add constant to emulate intercept
        X = np.c_[X, np.ones(X.shape[0])]

        # The features are already preprocessed
        # Shuffle
        perm = np.random.permutation(X.shape[0])
        X, y = X[perm, :], y[perm]

        # Select test at random
        test_size = 50
        test_idx = np.random.choice(X.shape[0], size=test_size, replace=False)
        train_idx = np.ones(X.shape[0], dtype=bool)
        train_idx[test_idx] = False
        X_test, y_test = X[test_idx, :], y[test_idx]
        X_train, y_train = X[train_idx, :], y[train_idx]

        # Split train among multiple clients.
        # The selection is not at random. We simulate the fact that each client
        # sees a potentially very different sample of patients.
        X, y = [], []
        step = int(X_train.shape[0] / n_subsets)
        for c in range(n_subsets):
            X.append(X_train[step * c: step * (c + 1), :])
            y.append(y_train[step * c: step * (c + 1)])
        self.X, self.y, self.X_test, self.y_test = X, y, X_test, y_test

    def get_sub_set(self, sub_set_id):
        return self.X[sub_set_id], self.y[sub_set_id]
