import logging

import numpy as np
from sklearn.datasets import load_diabetes
import pandas as pd
import os


class DataLoader:

    def __init__(self, dataset_path):
        self.X, self.y, self.X_test, self.y_test = None, None, None, None
        self.seed = 43
        np.random.seed(self.seed)
        self.dataset_path = dataset_path

    def load_data(self, filename):
        """
        Loads a dataset from the filesystem reading the file with name 'filename'.
        The features are stored in self.X as an np.array
        The target is stored in a self.y as an np.array
        :param filename:
        :return: None
        """
        dataset = pd.read_csv("{}/{}".format(self.dataset_path, filename), sep='\t')
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
        """
        Returns the dataset loaded by self.load_data(filename).
        :return: a tuple self.X (np.array of features) and self.y (np.array of target)
        """
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

    def get_dataset_for_training(self, requeriments):
        """
        Iterates over the files in the datasets directory and verifies wich of those comply with the requested
        requirements for the current model training. The last of the datasets that complies with the requirements
        is then returned by this method.
        :param requeriments: a dictionary with requirements for the dataset to be returned
        :return: the name of the file that complies with the requested requirements.
        """
        files = [fname for fname in os.listdir(self.dataset_path)]
        features = list(map(lambda x: x.lower(), requeriments['features']['list']))
        feat_range = requeriments['features']['range']
        target_range = requeriments['target']['range']
        for file in files:
            try:
                dataset = pd.read_csv("{}/{}".format(self.dataset_path, file), sep="\t")
                columns = dataset.columns.tolist()
                feature_values = dataset[columns[:-1]]
                target_values = dataset[columns[-1]]
                lowercase_cols = list(map(lambda x: x.lower(), columns[:-1]))
                if set(lowercase_cols) != set(features):
                    continue
                if feature_values.max().max() > feat_range[1]:
                    continue
                if feature_values.min().min() < feat_range[0]:
                    continue
                if target_values.max() > target_range[1]:
                    continue
                if target_values.min() < target_range[0]:
                    continue
            except Exception as e:
                print(e)
                continue
            return file
