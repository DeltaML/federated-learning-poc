from commons.data.data_loader import DataLoader

TEST1 = {
    "features": {
        "list": {
            "correct": ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7'],
            "extraAmount": ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 's6'],
            "lessAmount": ['f1', 'f2', 'f3', 'f4', 'f5'],
            "wrongNames": ['s6', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7']
        },
        "range": {
            "correct": [-2, 3],
            "wrong1": [0, 3],
            "wrong2": [-2, 1],
            "wrong3": [4, 6]
        },
    },
    "target": {
        "range": {
            "correct": [10, 20],
            "wrong1": [10, 15],
            "wrong2": [15, 20],
            "wrong3": [0, 6]
        },
    }
}

########################################################################################################################
#  TESTING GET_DATASET_FOR_TRAINING METHOD  ############################################################################
########################################################################################################################


def populate_requeriments_dict(feature_list_test, feature_range_test, target_range_test):
    features = {
        "list": TEST1["features"]["list"][feature_list_test],
        "range": TEST1["features"]["range"][feature_range_test]
    }
    target = {"range": TEST1["target"]["range"][target_range_test]}
    return {"features": features, "target": target}


def run_requeriment_test_with_parameters(feature_list_test, feature_range_test, target_range_test):
    reqs = populate_requeriments_dict(feature_list_test, feature_range_test, target_range_test)
    data_loader = DataLoader("./test_data/")
    result = data_loader.get_dataset_for_training(reqs)
    return result


def test_simple_dataset_not_comply_with_amount_of_features():
    result = run_requeriment_test_with_parameters("extraAmount", "correct", "correct")
    assert(result != "test1.csv")


def test_simple_dataset_not_comply_with_feature_names():
    result = run_requeriment_test_with_parameters("wrongNames", "correct", "correct")
    assert(result != "test1.csv")


def test_simple_dataset_not_comply_with_feature_ranges():
    result = run_requeriment_test_with_parameters("correct", "wrong1", "correct")
    assert(result != "test1.csv")
    result = run_requeriment_test_with_parameters("correct", "wrong2", "correct")
    assert(result != "test1.csv")
    result = run_requeriment_test_with_parameters("correct", "wrong3", "correct")
    assert(result != "test1.csv")


def test_simple_dataset_not_comply_with_target_range():
    result = run_requeriment_test_with_parameters("correct", "correct", "wrong1")
    assert(result != "test1.csv")
    result = run_requeriment_test_with_parameters("correct", "correct", "wrong2")
    assert(result != "test1.csv")
    result = run_requeriment_test_with_parameters("correct", "correct", "wrong3")
    assert(result != "test1.csv")

#  def test_simple_dataset_not_comply_with_field_separators():


def test_simple_dataset_comply_with_reqs():
    result = run_requeriment_test_with_parameters("correct", "correct", "correct")
    assert(result == "test1.csv")


test_simple_dataset_not_comply_with_amount_of_features()
test_simple_dataset_not_comply_with_target_range()
test_simple_dataset_not_comply_with_feature_ranges()
test_simple_dataset_not_comply_with_feature_names()
test_simple_dataset_not_comply_with_amount_of_features()
test_simple_dataset_comply_with_reqs()

########################################################################################################################
#  TESTING LOAD_DATA METHOD  ###########################################################################################
########################################################################################################################


def test_load_data():
    loader = DataLoader("./test_data")
    loader.load_data("test1.csv")
    X, y = loader.get_sub_set()
    assert(X is not None)
    assert(len(X) == 3)
    assert (len(X[0]) == 8)
    assert (y is not None)
    assert (len(y) == 3)
    assert (y[0] == 20)


test_load_data()
