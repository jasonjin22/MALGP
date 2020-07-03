# -*- coding: utf-8 -*-
# @Author: orres
# @Email:  jasonjin22@gmail.com
# @Date:   2020-06-24 23:08:04
# @Last Modified by:   orres
# @Last Modified time: 2020-07-04 01:36:35
import random
import numpy as np
import matlab.engine

from point import Point


def update_mean_var(point_list, mean1, mean2, var1, var2):
    if len(point_list) == 1:
        point = point_list[0]
        point.means[1] = mean1
        point.means[2] = mean2
        point.vars[1] = var1
        point.vars[2] = var2
        point.uncertainty = (np.abs(point.means[1]) + np.abs(point.means[2])) / np.sqrt(
            point.vars[1] + point.vars[1] + 1e-2)
    else:
        for i in range(len(point_list)):
            point = point_list[i]
            point.means[1] = mean1[i][0]
            point.means[2] = mean2[i][0]
            point.vars[1] = var1[i][0]
            point.vars[2] = var2[i][0]
            point.uncertainty = (np.abs(point.means[1]) + np.abs(point.means[2])) / np.sqrt(
                point.vars[1] + point.vars[1] + 1e-2)


class State(object):
    def __init__(self, N, num_views, dimensions):
        self.N = N  # number of all training samples
        self.num_views = num_views  # number of views of the samples
        self.dimensions = dimensions  # the dimension of the views
        self.U_t = set()  # unsampled points
        self.S_t = set()  # sampled points
        self.C_t = set()  # the unsampled points but are confident enough
        # hyper parameters
        self.theta1 = None
        self.theta2 = None
        self.sigma2 = None
        self.theta3 = None
        self.theta4 = None
        self.beta2 = None
        self.param = None

    def add_points_into_U_t(self, X1, X2, y):
        for i in range(self.N):
            point = Point(self.num_views, X1[i], X2[i], y[i])
            self.U_t.add(point)

    def sampling_init(self, sample_ratio):
        randomly_sampled_points = random.sample(self.U_t, int(np.floor(sample_ratio * self.N)))
        for point in randomly_sampled_points:
            self.U_t.remove(point)
            point.means[1] = point.y
            point.means[2] = point.y
            point.vars[1] = 0
            point.vars[2] = 0
            self.S_t.add(point)
        print(len(self.U_t))
        print(len(self.S_t))

    def testing(self):
        size_C = len(self.C_t)
        size_S = len(self.S_t)
        size_U = len(self.U_t)
        print("size_C: ", size_C, "size_S: ", size_S, "size_U: ", size_U)
        acc = 0
        for p in self.C_t.union(self.S_t):
            avg = 0.5 * p.means[1] + 0.5 * p.means[2]
            if np.sign(avg) == np.sign(p.y):
                acc += 1
        print(acc / (size_S + size_C))
        print("sample rate: ", size_S / (size_S + size_C))

    def modeling(self):
        a = 0.5
        b = 0.5
        print("Matlab start")
        print("S_t: ", len(self.S_t))
        print("U_t: ", len(self.U_t))

        eng = matlab.engine.start_matlab()
        eng.addpath(r'./gpml-matlab-v3.2-2013-01-15',nargout=0)
        eng.startup(nargout=0)
        X1_s, X2_s, y_s, _ = sampled_set_to_numpy_array(self.S_t)
        X1_u, X2_u, _, unsampled_point_list = sampled_set_to_numpy_array(self.U_t)
        X1_s_mat = matlab.double(X1_s.tolist())
        X2_s_mat = matlab.double(X2_s.tolist())
        y_s_mat = matlab.double(y_s.tolist())
        X1_u_mat = matlab.double(X1_u.tolist())
        X2_u_mat = matlab.double(X2_u.tolist())
        r = eng.modeling(X1_s_mat, X2_s_mat, y_s_mat, a, b, X1_u_mat, X2_u_mat, nargout=5)
        r, mean1, mean2, var1, var2 = r
        self.update_hyper_parameters(r)
        update_mean_var(unsampled_point_list, mean1, mean2, var1, var2)
        confident_points = []
        for p in self.U_t:
            if min(p.vars[1], p.vars[2]) < 0.25:
                confident_points.append(p)
                if np.sign(0.5 * p.means[1] + 0.5 * p.means[2]) != np.sign(p.y):
                    pass
        for p in confident_points:
            self.U_t.remove(p)
            self.C_t.add(p)

    def check_acc(self):
        acc = 0
        for p in self.U_t:
            avg = 0.5 * p.means[1] + 0.5 * p.means[2]
            if np.sign(avg) == np.sign(p.y):
                acc += 1
        print(acc / len(self.U_t))

    def update_hyper_parameters(self, r):
        self.theta1 = r[0][0]
        self.theta2 = r[0][1]
        self.sigma2 = r[0][2]
        self.theta3 = r[0][3]
        self.theta4 = r[0][4]
        self.beta2 = r[0][5]
        self.param = r

    def sampling(self):
        """
        select the point that has the maximum variance and minimum |y| to sample
        call the function add_points()
        :return:
        """
        if len(self.U_t) == 0:
            return
        next_point = None
        max_uncertainty = 0
        for p in self.U_t:
            if p.uncertainty >= max_uncertainty:
                next_point = p
                max_uncertainty = p.uncertainty
        self.U_t.remove(next_point)
        next_point.means[1] = next_point.y
        next_point.means[2] = next_point.y
        next_point.vars[1] = 0
        next_point.vars[2] = 0
        self.S_t.add(next_point)


def sampled_set_to_numpy_array(the_set):
    X1 = None
    X2 = None
    y = None
    point_list = []  # used to record the order of points in the generated array
    for point in the_set:
        point_list.append(point)
        if X1 is None:
            X1 = np.array([point.x1])
            X2 = np.array([point.x2])
        else:
            X1 = np.append(X1, [point.x1], axis=0)
            X2 = np.append(X2, [point.x2], axis=0)
        if y is None:
            y = np.array([point.y])
        else:
            y = np.append(y, point.y)
    return X1, X2, y, point_list
