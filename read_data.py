import numpy as np


def read_data(data_set):
    """
    read the mat data into the format mentioned in the comments below
    @param data_set: indicate which dataset we are going to read
    @return: N, num_views, X_train, Y_train, X_val, Y_val, X_test, Y_test
    """
    N = None  # number of samples in all
    Y_train = None  # numpy array, consists all the y's
    Y_val = None
    Y_test = None
    # the format of X:
    # a list, like: [{x1}, {x2}, ... ],
    # each element is a dictionary, like: {1: view1(np array), 2: view2(np array), ...}
    X_train = None
    X_val = None
    X_test = None
    num_views = None

    return N, num_views, X_train, Y_train, X_val, Y_val, X_test, Y_test
