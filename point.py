class Point(object):
    def __init__(self, num_views, view_dict, y):
        self.num_views = num_views
        self.views = {}
        self.dimensions = {}
        self.means = {}
        self.vars = {}
        self.y = y
        for i in range(num_views):
            self.views[i] = view_dict[i]
            self.dimensions[i] = view_dict[i].shape[0]
            self.means[i] = None
            self.vars[i] = None
