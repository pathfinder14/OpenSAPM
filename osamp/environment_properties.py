import numpy as np

class EnvironmentProperties(object):

    def __init__(self, density, lambda_lame=0, mu_lame=0, v_p=0, v_s=0):
        self.density = density
        self.lambda_lame = lambda_lame
        self.mu_lame = mu_lame
        self.v_p = v_p
        self.v_s = v_s
        self.E = 0
        self.nu_puass = 0
        if v_p == 0 and v_s == 0:
            self.__calculate_Puass_and_E()
            self.__calculate_speeds()
        else:
            self.__calculate_Lame_and_Puass_and_E()

    def set_dens_and_lame(self, density, lambda_lame, mu_lame):
        self.density = density
        self.lambda_lame = lambda_lame
        self.mu_lame = mu_lame
        self.__calculate_Puass_and_E()
        self.__calculate_speeds()

    def set_dens_and_speeds(self, density, v_p, v_s):
        self.density = density
        self.v_p = v_p
        self.v_s = v_s
        self.__calculate_Lame_and_Puass_and_E()

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
        self.E = self.mu_lame * (3 * self.lambda_lame + 2 * self.mu_lame) / (self.lambda_lame + self.mu_lame)


    def create_environment_for_seismic(self, x=1000, y=1000):
        """
                One of the main functions in class <Environment_properties> which returns the created environment field
                for seismic task according to the pack of input parameters:
                        (density, v_p, v_c) or (density, lambda_lame, mu_lame)

                Each element of returned <ndarray> contains list [v_p, v_s, density, lambda_lame, mu_lame]
                        which will be used in further calculations

                :param x:   Width
                :param y:   Height
                :return:    numpy.ndarray(shape=(x, y))
        """
        square = [self.v_p, self.v_s, self.density, self.lambda_lame, self.mu_lame]
        field = np.ndarray(shape=(x, y), dtype=np.dtype(list))
        field.fill(square)
        return field

    def create_environment_for_acoustic(self, x=1000, y=1000):
        """
                One of the main function in class <Environment_properties> which returns the created environment field
                for acoustic task according to the pack of input parameters:
                        (density, v_p) or (density, k)

                Each element of returned <ndarray> contains list [v_p, density, k]
                        which will be used in further calculations

                :param x:   Width
                :param y:   Height
                :return:    numpy.ndarray(shape=(x, y))
        """
        square = [self.v_p, self.density, self.lambda_lame]
        field = np.ndarray(shape=(x, y), dtype=np.dtype(list))
        field.fill(square)
        return field