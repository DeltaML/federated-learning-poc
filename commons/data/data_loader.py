import numpy as np
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

    def get_sub_set(self):
        """
        Returns the dataset loaded by self.load_data(filename).
        :return: a tuple self.X (np.array of features) and self.y (np.array of target)
        """
        return self.X, self.y

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
