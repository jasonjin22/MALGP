# MALGP

#### claim

- Our code is a combination of Python 3.6 and matlab, the matlab version is 2018b
  - The framework is written in Python and the optimization is done by matlab, with the GPML tool box
  - the gpml-matlab-v3.2-2013-01-15/ directory is from GPML, a matlab tool box for Gaussian process

#### file description

- modeling.m: the matlab script to do optimization and get the updated hyper parameters for GPs
- objFunction.m: the matlab script to do the objective function's evaluation and gradient computation
- test.m: the matlab script to do test on unsampled points
- point.py: the Python codes to define class point
- state.py: the Python codes to define whole framework of the algorithm and model
- run.ipynb: the Jupyter notebook to run experiments

#### data sets

- the dataset can be downloaded from https://github.com/yeqinglee/mvdata
- put the downloaded mvdata/ directory in the datasets/ directory

#### usage

- To run experiments on the datasets use jupyter notebook to open **run.ipynb**

