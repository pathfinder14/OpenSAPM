import numpy as np

class EnvironmentProperties(object):
    def __init__(self, density, elasticity_quotient = 0, mu_lame = 0, x_velocity = 0, y_velocity = 0):
        self.density = density
        self.elasticity_quotient = elasticity_quotient
        self.mu_lame = mu_lame
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.E = 0
        self.nu_puass = 0
        if x_velocity == 0 and y_velocity == 0:
            self.__calculate_Puass_and_E()
            self.__calculate_speeds()
        else:
            self.__calculate_Lame_and_Puass_and_E()

    def set_dens_and_lame(self, density, elasticity_quotient, mu_lame):
        self.density = density
        self.elasticity_quotient = elasticity_quotient
        self.mu_lame = mu_lame
        self.__calculate_Puass_and_E()
        self.__calculate_speeds()

    def set_dens_and_speeds(self, density, x_velocity, y_velocity):
        self.density = density
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.__calculate_Lame_and_Puass_and_E()

    def get_get_all_params(self):
        params = {'Density = ': self.density, 'Lambda_Lame = ': self.elasticity_quotient, 'Mu_Lame = ': self.mu_lame,
                  'x_velocity = ': self.x_velocity, 'y_velocity = ': self.y_velocity,
                  'E = ': self.E, 'nu_puass = ': self.nu_puass}
        return params

    def __calculate_Lame_and_Puass_and_E(self):
        self.mu_lame = self.y_velocity ** 2 * self.density
        self.nu_puass = (2 * self.mu_lame - self.x_velocity ** 2 * self.density) / (2 * (self.mu_lame - self.x_velocity ** 2 * self.density))
        self.elasticity_quotient = 2 * self.mu_lame * self.nu_puass / (1 - 2 * self.nu_puass)
        self.E = self.mu_lame * (3 * self.elasticity_quotient + 2 * self.mu_lame) / (self.elasticity_quotient + self.mu_lame)

    def __calculate_speeds(self):
        self.x_velocity = (self.elasticity_quotient / self.density) ** 0.5
        self.y_velocity = (self.mu_lame / self.density) ** 0.5

    def __calculate_Puass_and_E(self):
        self.nu_puass = self.elasticity_quotient / (2 * (self.elasticity_quotient + self.mu_lame))
        self.E = self.mu_lame * (3 * self.elasticity_quotient + 2 * self.mu_lame) / (self.elasticity_quotient + self.mu_lame)


    def create_environment_for_seismic(self, x=1000, y=1000):
        """
                One of the main functions in class <Environment_properties> which returns the created environment field
                for seismic task according to the pack of input parameters:
                        (density, x_velocity, v_c) or (density, elasticity_quotient, mu_lame)

                Each element of returned <ndarray> contains list [x_velocity, y_velocity, density, elasticity_quotient, mu_lame]
                        which will be used in further calculations

                :param x:   Width
                :param y:   Height
                :return:    numpy.ndarray(shape=(x, y))
        """
        square = [self.x_velocity, self.y_velocity, self.density, self.elasticity_quotient, self.mu_lame]
        field = np.ndarray(shape=(x, y), dtype=np.dtype(list))
        field.fill(square)
        return field

    def create_environment_for_acoustic(self, x=1000, y=1000):
        """
                One of the main function in class <Environment_properties> which returns the created environment field
                for acoustic task according to the pack of input parameters:
                        (density, x_velocity) or (density, k)

                Each element of returned <ndarray> contains list [x_velocity, density, k]
                        which will be used in further calculations

                :param x:   Width
                :param y:   Height
                :return:    numpy.ndarray(shape=(x, y))
        """
        square = [self.x_velocity, self.density, self.elasticity_quotient]
        field = np.ndarray(shape=(x, y), dtype=np.dtype(list))
        field.fill(square)
        return field