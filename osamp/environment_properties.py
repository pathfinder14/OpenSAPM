import matplotlib as mplot
import numpy as np
from utils.environment_properties_analyzers import visual_analyzer as va

class environment_properties(object):

    def __init__(self, params, density=0, lambda_lame=0, mu_lame=0, v_p=0, v_s=0):
        self.params = params
        self.density = density
        self.lambda_lame = 0
        self.mu_lame = 0
        self.v_p = 0
        self.v_s = 0
        self.E = 0
        self.nu_puass = 0
        if v_p == 0 and v_s == 0 and mu_lame == 0 and lambda_lame != 0:
            self.set_dens_and_lame_for_acoustic(density, lambda_lame)
        if v_p == 0 and v_s == 0 and mu_lame != 0 and lambda_lame != 0:
            self.set_dens_and_lame_for_seismic(density, lambda_lame, mu_lame)
        if v_p != 0 and v_s == 0 and mu_lame == 0 and lambda_lame == 0:
            self.set_dens_and_speeds_for_acoustic(density, v_p)
        if v_p != 0 and v_s != 0 and mu_lame == 0 and lambda_lame == 0:
            self.set_dens_and_speeds_for_seismic(density, v_p, v_s)



    def set_dens_and_lame_for_seismic(self, density, lambda_lame, mu_lame):
        self.density = density
        self.lambda_lame = lambda_lame
        self.mu_lame = mu_lame
        self.__calculate_Puass_and_E()
        self.__calculate_speeds()

    def set_dens_and_lame_for_acoustic(self, density, lambda_lame):
        self.density = density
        self.lambda_lame = lambda_lame
        self.v_p = (lambda_lame/density) ** 0.5

    def set_dens_and_speeds_for_seismic(self, density, v_p, v_s):
        self.density = density
        self.v_p = v_p
        self.v_s = v_s
        self.__calculate_Lame_and_Puass_and_E()

    def set_dens_and_speeds_for_acoustic(self, density, v_p):
        self.density = density
        self.v_p = v_p
        self.lambda_lame = (v_p**2) * density

    def get_get_all_params(self):
        params = {'Density = ': self.density, 'Lambda_Lame = ': self.lambda_lame, 'Mu_Lame = ': self.mu_lame,
                  'v_p = ': self.v_p, 'v_s = ': self.v_s,
                  'E = ': self.E, 'nu_puass = ': self.nu_puass}
        return params

    def __calculate_Lame_and_Puass_and_E(self):
        self.mu_lame = self.v_s ** 2 * self.density
        self.nu_puass = (2 * self.mu_lame - self.v_p ** 2 * self.density) / (2 * (self.mu_lame - self.v_p ** 2 * self.density))
        self.lambda_lame = 2 * self.mu_lame * self.nu_puass / (1 - 2 * self.nu_puass)
        self.E = self.mu_lame * (3 * self.lambda_lame + 2 * self.mu_lame) / (self.lambda_lame + self.mu_lame)

    def __calculate_speeds(self):
        self.v_p = (self.E / self.density) ** 0.5
        self.v_s = (self.mu_lame / self.density) ** 0.5

    def __calculate_Puass_and_E(self):
        self.nu_puass = self.lambda_lame / (2 * (self.lambda_lame + self.mu_lame))
        # self.E = self.mu_lame * (3 * self.lambda_lame + 2 * self.mu_lame) / (self.lambda_lame + self.mu_lame)
        self.E = self.lambda_lame * (1 + self.nu_puass) * (1 - 2*self.nu_puass)/(self.nu_puass)


    def create_environment_for_seismic(self, x=1000, y=1000):
        """
                One of the main functions in class <Environment_properties> which returns the created environment field
                for seismic task according to the pack of input parameters:
                        (density, v_p, v_c) or (density, lambda_lame, mu_lame)

                Each element of returned <ndarray> contains list [v_p, v_s, density, lambda_lame, mu_lame]
                        which will be used in further calculations

                :param x:   Width
                :param y:   Height
                :return field:    numpy.ndarray(shape=(x, y))
        """
        square = [self.v_p, self.v_s, self.density, self.lambda_lame, self.mu_lame]
        field = np.ndarray(shape=(x, y), dtype=np.dtype(list))
        field.fill(square)
        return field

    def create_environment_for_acoustic(self, x=100, y=100):
        """
                One of the main function in class <Environment_properties> which returns the created environment field
                for acoustic task according to the pack of input parameters:
                        (density, v_p) or (density, k)

                Each element of returned <ndarray> contains list [v_p, density, k]
                        which will be used in further calculations

                :param x:   Width
                :param y:   Height
                :return field:    numpy.ndarray(shape=(x, y))
        """
        square = [self.v_p, self.density, self.lambda_lame]
        field = np.ndarray(shape=(x, y), dtype=np.dtype(list))
        field.fill(square)
        return field

    def create_environment_from_image(self, image_path):
        """
                        One of the main function in class <Environment_properties> which returns the created environment field
                        gathered from the picture with describes the environment
                        with proper parameters for seismic task for each
                        pixel<->(density, lambda_lame, mu_lame)
                        or pixel<->(density, v_p, v_c) or correspondingly for acoustic task :
                        pixel<->(density, v_p) or pixel<->(density, k)

                        Each element of returned <array> contains corresponding list with parameters:
                        [density, lambda_lame, mu_lame, v_p, v_s] for seismic and
                        [density=0, lambda_lame=0, v_p=0] for acoustic

                        :param image_path: The relative path to the image, which describes the environment
                        :return field:    numpy.ndarray(shape=(height, length)); each element of array contains properties of environment
                """
        picture_parser = va.visual_analyzer(image_path, self.params)
        field = picture_parser.create_field()
        return field


# # density = 1000
# # v_p = 200
# # v_s = 400
# # mu_lame = 56
# # lambda_lame = 0
# # props = environment_properties(density, lambda_lame, mu_lame)
# # field = props.create_environment_for_acoustic()
# # print(field.shape)
#
# image_path = "three_col.jpg"
# params = {(254, 242, 0) : [1, 2, 3]}
# properties = environment_properties(params=params)
# field = properties.create_environment_from_image(image_path)
# print(type(field))
# print(field[663][1626])
#
# # buf = tuple(map(tuple, image[0][0]))
# # print(buf[0])