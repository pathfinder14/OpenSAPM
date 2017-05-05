class GridElement1d:
    def __init__(self, sigma, velocity):
        self.sigma = sigma
        self.velocity = velocity

    def set_value(self, sigma, velocity):
        self.sigma = sigma
        self.velocity = velocity


class Grid1d:
    def __init__(self, dimension):
        self.elements = []  # list of GridElement1d
        self.dimension = dimension

