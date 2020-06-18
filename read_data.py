'''
@Author: your name
@Date: 2020-06-16 21:16:30
@LastEditTime: 2020-06-18 10:59:07
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /ALMVL/read_data.py
'''
import numpy as np
import scipy.io as io
import random
from sklearn.decomposition import PCA


def read_data(data_set, conf):
    """
    read the mat data into the format mentioned in the comments below
    @param data_set: indicate which dataset we are going to read
    @param conf: we could get data path from conf
    @return: N, num_views, X_train, Y_train, X_val, Y_val, X_test, Y_test
    """
    N = None  # number of samples in all
    num_views = None

    Y_train = []  # numpy array, consists all the y's
    Y_val = []
    Y_test = []
    # the format of X:
    # a list, like: [{x1}, {x2}, ... ],
    # each element is a dictionary, like: {1: view1(np array), 2: view2(np array), ...}
    X_train = []
    X_val = []
    X_test = []

    matr = io.loadmat(conf.data_path)
    X = matr['X'][0]
    Y = matr['Y']
    N = Y.size
    num_views = conf.new_views
    for i in range(num_views):
        X[i].resize(N,(X[i].size//N))
        if conf.pv:
            assert len(conf.pv) == num_views, "the imput number of components does not match the number of views"
            X[i] = for_PCA(X[i],conf.pv[i])


    total_data = []
    for i in range(Y.size):
        temp_points = {}
        if Y[i][0] == 1:
            x_points = {}
            for j in range(num_views):
                x_points[j] = X[j][i]
            temp_points[1] = x_points
            total_data.append(temp_points)
        elif Y[i][0] == 2:
            x_points = {}
            for j in range(num_views):
                x_points[j] = X[j][i]
            temp_points[-1] = x_points
            total_data.append(temp_points)
        elif Y[i][0] == 3:
            break

    new_N = len(total_data)
    
    random.shuffle(total_data)
    train_set_num = int(new_N*conf.train_set)
    val_set_num = int(new_N*(conf.train_set+conf.val_set))
    test_set_num = int(new_N*(conf.train_set+conf.val_set+conf.test_set))

    temp_train_set = total_data[:train_set_num]
    temp_val_set = total_data[train_set_num:val_set_num]
    temp_test_set = total_data[val_set_num:]

    for i in range(len(temp_train_set)):
        if temp_train_set[i].get(-1):
            # Y_train.append(np.array([-1]))
            Y_train.append([-1])
            X_train.append(temp_train_set[i][-1])
        elif temp_train_set[i].get(1):
            Y_train.append([1])
            X_train.append(temp_train_set[i][1])
    
    for i in range(len(temp_val_set)):
        if temp_val_set[i].get(-1):
            # Y_train.append(np.array([-1]))
            Y_val.append([-1])
            X_val.append(temp_val_set[i][-1])
        elif temp_val_set[i].get(1):
            Y_val.append([1])
            X_val.append(temp_val_set[i][1])
    
    for i in range(len(temp_test_set)):
        if temp_test_set[i].get(-1):
            # Y_train.append(np.array([-1]))
            Y_test.append([-1])
            X_test.append(temp_test_set[i][-1])
        elif temp_test_set[i].get(1):
            Y_test.append([1])
            X_test.append(temp_test_set[i][1])
    
    import pdb;pdb.set_trace()

    return N, num_views, X_train, Y_train, X_val, Y_val, X_test, Y_test

def for_PCA(data, num_components):
    """
    function for PCA
    @param data: apply the dimensionality reduction on data
    @param num_components: number of components to keep
    @return: reduced_data 
    """
    pca = PCA(n_components=num_components)
    reduced_data = pca.fit_transform(data)

    return reduced_data
