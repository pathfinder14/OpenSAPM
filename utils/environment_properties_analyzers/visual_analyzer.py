import numpy as np
import matplotlib.pyplot as plt

class visual_analyzer(object):
    """
    This class is in charge of parsing given picture model of environment
    and providing class <environment_properties> with needed input data

    TODO
    """

    def __init__(self, image_path, params):
        self.image = self._parse_picture(image_path)
        self.params = params

    def _parse_picture(self, image_path):
        image_file = open(image_path, 'rb')
        image = plt.imread(image_file)
        return image

    def show_picture(self):
        plt.imshow(self.image)
        plt.axis('off')
        plt.show()

    def create_field(self):
        x = self.image.shape[0]
        y = self.image.shape[1]
        field = np.zeros((x, y), dtype=list)
        for i in range(x):
            line = tuple(map(tuple, self.image[i]))
            for j in range(y):
                square = line[j]
                field[i][j] = self.params.get(square)

        return field




# image_path = "three_col.jpg"
# params = {(254, 242, 0) : [1, 2, 3],  (255, 255, 255): [2, 100, 10]}
# anal = visual_analyzer(image_path, params)
# anal.show_picture()
# field = anal.create_field()
# print(field[663][1626])
# print(field[600][230])
# image = anal.image
# # buf = tuple(map(tuple, image[0][0]))
# # print(buf[0])