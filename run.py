'''
@Author: your name
@Date: 2020-06-16 21:16:30
@LastEditTime: 2020-06-17 15:19:33
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /ALMVL/run.py
'''
import random
import read_data as rd
import numpy as np
import argparse
from config import get_config
from state import State
from base_model import BaseModel


def add_points_into_states(N, X, Y, num_views, state):
    """
    traverse the read dataset and call state.add_point to add all the points into state.U_t
    determine whether it converge or not
    @param N: number of training samples
    @param X: a list of dictionaries, each dictionary denotes a sample
    @param Y: a numpy array denotes the labels of all the training samples
    @param num_views: number of views
    @param state: the state
    @return: None
    """
    state.model()

    pass


def generate_toy_data(N, num_views):
    d1 = 2
    d2 = 5
    y = np.random.randint(-1, 2, size=[N, 1])
    X = []
    # generate y
    for i in range(len(y)):
        if y[i][0] == 0:
            if random.random() < 0.5:
                y[i][0] = -1
            else:
                y[i][0] = 1
    for i in range(N):
        new_point = {}
        for j in range(num_views):
            new_point[j] = np.random.random((1, d1))
        X.append(new_point)
    return X, y


def run(mode,conf):
    """
    run the multi-view learning algorithm
    @param mode: if mode is 0, run the basic algorithm (with no active learning), if 1, run ALMVL
    @return: None
    """
    # read data
    N, num_views, X_train, Y_train, X_val, Y_val, X_test, Y_test, dimensions = rd.read_data('some parameters',conf)

    if mode == 0:
        # hyper parameters:
        sample_rate_init = 0.1
        # initialize state
        state = State()
        add_points_into_states(N, X_train, Y_train, num_views, state)
        # sample some points at the beginning
        state.sampling_init(sample_rate_init)
    else:
        # X_train, Y_train = generate_toy_data(N, num_views)

        state = State(N,dimensions,conf)
        #put num of conf.sample_init_rate of points into state.s_t.
        state.sampling_init(X_train, Y_train,conf)
        base_model = BaseModel(N, X_train, Y_train, num_views)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='for ALMVL')
    parser.add_argument("-m", "--mode", help="mode for active learning", default=1, type=int)
    parser.add_argument("-pv", "--view", help="PCA parameters for every view and the format is 2,3,4(separated by commas)")
    args = parser.parse_args()

    conf = get_config()
    conf.pv = args.view
    if conf.pv:
        temp = conf.pv.split(',')
        conf.pv = [int(i) for i in temp]
    
    run(args.mode,conf)