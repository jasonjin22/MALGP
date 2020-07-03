class Point(object):
    def __init__(self, num_views, x1, x2, y):
        self.num_views = num_views
        self.views = {}
        self.dimensions = {}
        self.means = {}
        self.vars = {}
        self.x1 = x1
        self.x2 = x2
        self.y = y
        self.uncertainty = None
