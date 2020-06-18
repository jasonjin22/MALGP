'''
@Author: your name
@Date: 2020-06-16 21:23:05
@LastEditTime: 2020-06-17 01:41:09
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /ALMVL/config.py
'''
from easydict import EasyDict as edict
from pathlib import Path

def get_config():
    conf = edict()
    conf.data_path = "datasets/mvdata/Caltech101-7.mat"
    conf.num_views = 2
    conf.val_set = 0.1
    conf.test_set = 0.1
    conf.train_set = 0.8
    conf.sample_rate_init = 0.2
    

    return conf