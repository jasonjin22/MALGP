class BaseModel(object):
    def __init__(self, N, X, Y, num_views):
        self.N = N
        self.X = X
        self.Y = Y
        self.num_views = num_views

    def modeling(self):
        pass