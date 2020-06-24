import pyGPs
import random
import numpy as np


class State(object):
    def __init__(self, N, dimensions, conf):
        self.N = N  # number of all training samples
        self.num_views = conf.num_views  # number of views of the samples
        self.dimensions = dimensions  # the dimension of the views
        self.XU_t = []  # x label of unsampled points
        self.XS_t = []  # x label of sampled points
        self.YS_t = []  # y label of sampled points
        self.points = [] # every element is a "point" class in XS_t

    def sampling_init(self,x_train,y_train, conf):
        """
        randomly sample some points from U_t, move them into S_t
        Due to the reason that everytime we run the program, X_train is chosen randomly,so we choose the first
        len(X_train) * conf.sample_init_rate of points into S_t
        @param sample_rate_init: a hyper parameter, number of sampled points = sample_rate_init * self.N
        @return: None
        """
        num_chosen_points = int(len(x_train[0]) * conf.sample_rate_init)
        for j in range(conf.num_views):
            temp = []
            for i in range(num_chosen_points):
                temp.append(x_train[j][i])
            self.XS_t.append(np.array(temp))


        for j in range(conf.num_views):
            temp = []
            for i in range(num_chosen_points,len(x_train[0])):
                temp.append(x_train[j][i])
            self.XU_t.append(np.array(temp))

        for i in range(num_chosen_points):
            self.YS_t.append(y_train[i])

        ys_t = np.array(self.YS_t)

        return [self.XS_t,self.XU_t,ys_t]






    def sampling(self):
        """
        select the point that has the maximum variance and minimum |y| to sample
        call the function add_points()
        :return:
        """
        # length = len(self.XU_t)
        # minimum = float('inf')
        # for i in range(length):
        #     temp =
        #     if temp < minimum:
        #         minimum = temp;
        #         minimum_index = i
        # self.add_point(minimum_index)


        # minimum_index = 0
        #
        #
        #
        #
        # self.XS_t.append(self.XU_t[minimum_index])
        # self.YS_t.append(self.YU_t[minimum_index])
        # self.XU_t.pop(minimum_index)




        pass

    def modeling(self,x_s,x_u,y_s):
        """
        using the parameters in build_model to calculate the mean and varience of every point.
        ALso contruct a class point for every point in the unsample list.
        call the function sample()
        :return:
        """
        pass


