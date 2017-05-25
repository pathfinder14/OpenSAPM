import numpy as np
import importlib.util

spec = importlib.util.spec_from_file_location("visual_analyzer", "../utils/environment_properties_analyzers/visual_analyzer.py")
visual_analyzer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(visual_analyzer)

class EnvironmentProperties:

    def __init__(self, density=0, lambda_lame=0, mu_lame=0, x_velocity=0, y_velocity=0,
                 img_creating_parameters=None, analytical_creating_parameters=None):
        if img_creating_parameters is not None:
            self.init_params = dict(img_creating_parameters)
            self.img_creating_parameters = dict(img_creating_parameters)
        if analytical_creating_parameters is not None:
            self.analytical_creating_parameters = analytical_creating_parameters
        self.density = density
        self.lambda_lame = lambda_lame
        self.elasticity_quotient = lambda_lame
        self.mu_lame = mu_lame
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.E = 0
        self.nu_puass = 0
        if x_velocity == 0 and y_velocity == 0 and mu_lame == 0 and lambda_lame != 0:
            self.set_dens_and_lame_for_acoustic(density, lambda_lame)
        if x_velocity == 0 and y_velocity == 0 and mu_lame != 0 and lambda_lame != 0:
            self.set_dens_and_lame_for_seismic(density, lambda_lame, mu_lame)
        if x_velocity != 0 and y_velocity == 0 and mu_lame == 0 and lambda_lame == 0:
            self.set_dens_and_speeds_for_acoustic(density, x_velocity)
        if x_velocity != 0 and y_velocity != 0 and mu_lame == 0 and lambda_lame == 0:
            self.set_dens_and_speeds_for_seismic(density, x_velocity, y_velocity)


    def set_params_for_acoustic_using_v_p(self):
        self.__calculate_params_for_acoustic_task_v_p()

    def set_params_for_acoustic_using_k(self):
        self.__calculate_params_for_acoustic_task_k()


    def set_params_for_seismic_using_lame(self):
        self.__calculate_params_for_seismic_task_vp_vs()

    def set_params_for_seismic_using_speeds(self):
        self.__calculate_params_for_seismic_task_lame()

    def set_dens_and_lame_for_seismic(self, density, elasticity_quotient, mu_lame):
        self.density = density
        self.elasticity_quotient = elasticity_quotient
        self.mu_lame = mu_lame
        self.__calculate_Puass_and_E()
        self.__calculate_speeds()

    def set_dens_and_lame_for_acoustic(self, density, elasticity_quotient):
        self.density = density
        self.elasticity_quotient = elasticity_quotient
        self.x_velocity = (elasticity_quotient/density) ** 0.5

    def set_dens_and_speeds_for_seismic(self, density, x_velocity, y_velocity):
        self.density = density
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.__calculate_Lame_and_Puass_and_E()

    def set_dens_and_speeds_for_acoustic(self, density, x_velocity):
        self.density = density
        self.x_velocity = x_velocity
        self.elasticity_quotient = (x_velocity**2) * density

    def get_get_all_params(self):
        params = {'Density = ': self.density, 'Lambda_Lame = ': self.elasticity_quotient, 'Mu_Lame = ': self.mu_lame,
                  'x_velocity = ': self.x_velocity, 'y_velocity = ': self.y_velocity,
                  'E = ': self.E, 'nu_puass = ': self.nu_puass}
        return params

    def __calculate_params_for_acoustic_task_v_p(self):
        for buf_color in self.init_params.keys():
            init_params = self.init_params.get(buf_color)
            density = init_params[0]
            x_velocity = init_params[1]
            elasticity_quotient = self.__calculate_lambda_lame(density, x_velocity)
            self.img_creating_parameters.update({buf_color: [density, elasticity_quotient, x_velocity]})

    def __calculate_params_for_acoustic_task_k(self):
        for buf_color in self.init_params.keys():
            init_params = self.init_params.get(buf_color)
            density = init_params[0]
            elasticity_quotient = init_params[1]
            x_velocity = self.__calculate_v_p(density, elasticity_quotient)
            self.img_creating_parameters.update({buf_color: [density, elasticity_quotient, x_velocity]})

    def __calculate_lambda_lame(self, density, x_velocity):
        elasticity_quotient = (x_velocity ** 2) * density
        return elasticity_quotient

    def __calculate_v_p(self, density, elasticity_quotient):
        v_p = (elasticity_quotient / density) ** 0.5
        return v_p

    def __calculate_params_for_seismic_task_vp_vs(self):
        for buf_color in self.init_params.keys():
            init_params = self.init_params.get(buf_color)
            density = init_params[0]
            v_p = init_params[1]
            v_s = init_params[2]
            self.set_dens_and_speeds_for_seismic(density, v_p, v_s)
            mu_lame = self.mu_lame
            lambda_lame = self.elasticity_quotient
            self.img_creating_parameters.update({buf_color: [density, lambda_lame, mu_lame, v_p, v_s]})

    def __calculate_params_for_seismic_task_lame(self):
        for buf_color in self.init_params.keys():
            init_params = self.init_params.get(buf_color)
            density = init_params[0]
            lambda_lame = init_params[1]
            mu_lame = init_params[2]
            self.set_dens_and_lame_for_seismic(density, lambda_lame, mu_lame)
            v_p = self.x_velocity
            v_s = self.y_velocity
            self.img_creating_parameters.update({buf_color: [density, lambda_lame, mu_lame, v_p, v_s]})

    def __calculate_Lame_and_Puass_and_E(self):
        self.mu_lame = self.y_velocity ** 2 * self.density
        self.nu_puass = (2 * self.mu_lame - self.x_velocity ** 2 * self.density) / (2 * (self.mu_lame - self.x_velocity ** 2 * self.density))
        self.elasticity_quotient = 2 * self.mu_lame * self.nu_puass / (1 - 2 * self.nu_puass)
        self.E = self.mu_lame * (3 * self.elasticity_quotient + 2 * self.mu_lame) / (self.elasticity_quotient + self.mu_lame)

    def __calculate_speeds(self):
        self.x_velocity = (self.E / self.density) ** 0.5
        self.y_velocity = (self.mu_lame / self.density) ** 0.5

    def __calculate_Puass_and_E(self):
        self.nu_puass = self.elasticity_quotient / (2 * (self.elasticity_quotient + self.mu_lame))
        # self.E = self.mu_lame * (3 * self.elasticity_quotient + 2 * self.mu_lame) / (self.elasticity_quotient + self.mu_lame)
        self.E = self.elasticity_quotient * (1 + self.nu_puass) * (1 - 2*self.nu_puass)/(self.nu_puass)


    def create_environment_for_seismic(self, x=15, y=15):
        """
                One of the main functions in class <Environment_properties> which returns the created environment field
                for seismic task according to the pack of input parameters:
                        (density, x_velocity, v_c) or (density, elasticity_quotient, mu_lame)

                Each element of returned <ndarray> contains list [x_velocity, y_velocity, density, elasticity_quotient, mu_lame]
                        which will be used in further calculations

                :param x:   Width
                :param y:   Height
                :return field:    numpy.ndarray(shape=(x, y))
        """
        square = [self.x_velocity, self.y_velocity, self.density, self.elasticity_quotient, self.mu_lame]
        field = np.ndarray(shape=(x, y), dtype=np.dtype(list))
        field.fill(square)
        return field

    def create_environment_for_acoustic(self, x=15, y=15):
        """
                One of the main function in class <Environment_properties> which returns the created environment field
                for acoustic task according to the pack of input parameters:
                        (density, x_velocity) or (density, k)

                Each element of returned <ndarray> contains list [x_velocity, density, k]
                        which will be used in further calculations

                :param x:   Width
                :param y:   Height
                :return field:    numpy.ndarray(shape=(x, y))
        """
        square = [self.x_velocity, self.density, self.elasticity_quotient]
        field = np.ndarray(shape=(x, y), dtype=np.dtype(list))
        field.fill(square)
        return field

    def create_environment_from_image(self, image_path):
        """
                        One of the main function in class <Environment_properties> which returns the created environment field
                        gathered from the picture with describes the environment
                        with proper parameters for seismic task for each
                        pixel<->(density, elasticity_quotient, mu_lame)
                        or pixel<->(density, x_velocity, v_c) or correspondingly for acoustic task :
                        pixel<->(density, x_velocity) or pixel<->(density, k)

                        Each element of returned <array> contains corresponding list with parameters:
                        [density, elasticity_quotient, mu_lame, x_velocity, y_velocity] for seismic and
                        [density=0, elasticity_quotient=0, x_velocity=0] for acoustic

                        :param image_path: The relative path to the image, which describes the environment
                        :return field:    numpy.ndarray(shape=(height, length)); each element of array contains properties of environment
                """
        picture_parser = visual_analyzer.visual_analyzer(image_path, self.img_creating_parameters)
        field = picture_parser.create_field()
        return field


# # density = 1000
# # x_velocity = 200
# # y_velocity = 400
# # mu_lame = 56
# # elasticity_quotient = 0
# # props = environment_properties(density, elasticity_quotient, mu_lame)
# # field = props.create_environment_for_acoustic()
# # print(field.shape)
#
# image_path = "three_col.jpg"
# params = {(254, 242, 0): [1, 200, 30], (255, 255, 255): [2, 100, 10]}
# properties = EnvironmentProperties(img_creating_parameters=params)
# properties.set_params_for_seismic_using_lame()
# field = properties.create_environment_from_image(image_path)
# print(field[663][1626])
# print(field[600][230])

# buf = tuple(map(tuple, image[0][0]))
# print(buf[0])