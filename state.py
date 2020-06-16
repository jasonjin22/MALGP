import GPy
import random
import numpy as np


class State(object):
    def __init__(self, N):
        self.N = N  # number of all training samples
        self.num_views = None  # number of views of the samples
        self.dimensions = {}  # the dimension of the views
        self.U_t = set()  # unsampled points
        self.S_t = set()  # sampled points

    def sampling_init(self, sample_rate_init):
        """
        randomly sample some points from U_t, move them into S_t
        @param sample_rate_init: a hyper parameter, number of sampled points = sample_rate_init * self.N
        @return: None
        """

        pass

    def sampling(self):
        pass

    def modeling(self):
        pass

    def add_point(self, point):
        """
        add point into U_t, fill in num_views, dimensions
        @param point: the point should be moved into U_t
        @return: None
        """
        pass
