class GridElement1d:
    def __init__(self, sigma=0, velocity=0):
        self.sigma = sigma
        self.velocity = velocity

    def set_value(self, sigma, velocity):
        self.sigma = sigma
        self.velocity = velocity


class Grid1d:
    def __init__(self, elements=None, dimension=0):
        if elements is None:
            elements = []
        self.elements = elements  # list of GridElement1d
        self.dimension = dimension


class GridElement2d:
    def __init__(self, sigma=None, velocity=None):  # [sigma_11, sigma_12, sigma_22], sigma_12=sigma_21
        if velocity is None:
            velocity = [0, 0]
        if sigma is None:
            sigma = [0, 0, 0]
        self.sigma = sigma
        self.velocity = velocity

    def set_value(self, sigma, velocity):
        self.sigma = sigma
        self.velocity = velocity


class Grid2d:
    def __init__(self, elements=None, dimension=0):
        if elements is None:
            elements = [[0 for i in range(dimension)] for j in range(dimension)]
        self.elements = elements  # list of GridElement1d
        self.dimension = dimension
