'''
@Author: your name
@Date: 2020-06-16 21:16:30
@LastEditTime: 2020-06-17 02:44:13
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /ALMVL/read_data.py
'''
import numpy as np
import scipy.io as io


def read_data(data_set, conf):
    """
    read the mat data into the format mentioned in the comments below
    @param data_set: indicate which dataset we are going to read
    @param conf: we could get data path from conf
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

    matr = io.loadmat(conf.data_path)
    X = matr['X'][0]
    Y = matr['Y']
    N = Y.size
    num_views = X.size
    for i in range(num_views):
        X[i].resize(N,(X[i].size//N))
    
    total_data = []
    for i in range(N):
        temp_points = {}
        for j in range(num_views):
            temp_points[j] = X[j][i]
        total_data.append(temp_points)

    train_set_num = int(N*conf.train_set)
    val_set_num = int(N*(conf.train_set+conf.val_set))
    test_set_num = int(N*(conf.train_set+conf.val_set+conf.test_set))
    
    
    X_train = total_data[:train_set_num]
    Y_train = Y[:train_set_num]

    X_val = total_data[train_set_num:val_set_num]
    Y_val = Y[train_set_num:val_set_num]

    X_test = total_data[val_set_num:]
    Y_test = Y[val_set_num:]


    return N, num_views, X_train, Y_train, X_val, Y_val, X_test, Y_test


