import logging

import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.preprocessing import StandardScaler
import pandas as pd


class DataLoader:

    def __init__(self):
        self.X, self.y, self.X_test, self.y_test = None, None, None, None
        self.seed = 43
        np.random.seed(self.seed)

    def load_data(self):
        dataset = pd.read_csv("./dataset/data.csv", sep='\t')
        df_X = dataset[dataset.columns[:-1]]
        # Add constant to emulate intercept
        df_X[len(dataset.columns)] = 1
        df_y = dataset[dataset.columns[-1]]
        self.X = np.asarray(df_X.values.tolist())
        self.y = np.asarray(df_y.values.tolist())

    def load_data_deprecated(self, n_subsets):
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
        X, y = {}, {}
        step = int(X_train.shape[0] / n_subsets)
        for c in range(n_subsets):
            X[c] = X_train[step * c: step * (c + 1), :]
            y[c] = y_train[step * c: step * (c + 1)]
        self.X, self.y, self.X_test, self.y_test = X, y, X_test, y_test

    def get_sub_set(self):
        return self.X, self.y

    @staticmethod
    def load_random_data():
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
        return X_train, y_train, X_test, y_test
