import numpy as np
import importlib.util

spec = importlib.util.spec_from_file_location("visual_analyzer", "../utils/environment_properties_analyzers/visual_analyzer.py")
visual_analyzer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(visual_analyzer)

class EnvironmentProperties:
    """
        This is the main class, which models the environment field with input parameters
    """

    # Constructor
    # The environment can be set from picture or analytically
    # The environment can be homogeneous or heterogeneous
    # Parameters can be constants or variable
    def __init__(self, density=0, lambda_lame=0, mu_lame=0, v_p=0, v_s=0,
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
        self.v_p = v_p
        self.v_s = v_s
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


    # Sets all parameters for acoustic, knowing v_p
    def set_params_for_acoustic_using_v_p(self):
        self.__calculate_params_for_acoustic_task_v_p()

    # Sets all parameters for acoustic, knowing v_p
    def set_params_for_acoustic_using_k(self):
        self.__calculate_params_for_acoustic_task_k()

    # Sets all parameters for seismic, knowing lame coefficients
    def set_params_for_seismic_using_lame(self):
        self.__calculate_params_for_seismic_task_vp_vs()

    # Sets all parameters for seismic, knowing v_p and v_s
    def set_params_for_seismic_using_speeds(self):
        self.__calculate_params_for_seismic_task_lame()

    # Calculate and sets density, elasticity_quotient and mu_lame coefficient for seismic task
    def set_dens_and_lame_for_seismic(self, density, elasticity_quotient, mu_lame):
        self.density = density
        self.elasticity_quotient = elasticity_quotient
        self.mu_lame = mu_lame
        self.__calculate_Puass_and_E()
        self.__calculate_speeds()

    # Calculate and sets density and elasticity_quotient for acoustic task
    def set_dens_and_lame_for_acoustic(self, density, elasticity_quotient):
        self.density = density
        self.elasticity_quotient = elasticity_quotient
        self.v_p = (elasticity_quotient/density) ** 0.5

    # Calculate and sets density, x and y velocities for seismic task
    def set_dens_and_speeds_for_seismic(self, density, v_p, v_s):
        self.density = density
        self.v_p = v_p
        self.v_s = v_s
        self.__calculate_Lame_and_Puass_and_E()

    # Calculate and sets density and x velocity for acoustic task
    def set_dens_and_speeds_for_acoustic(self, density, v_p):
        self.density = density
        self.v_p = v_p
        self.elasticity_quotient = (v_p**2) * density

    # Returns all parameters in dictionary
    def get_get_all_params(self):
        params = {'Density = ': self.density, 'Lambda_Lame = ': self.elasticity_quotient, 'Mu_Lame = ': self.mu_lame,
                  'v_p = ': self.v_p, 'v_s = ': self.v_s,
                  'E = ': self.E, 'nu_puass = ': self.nu_puass}
        return params

    # Calculates all parameters for acoustic_task in heterogeneous environment, knowing v_p
    def __calculate_params_for_acoustic_task_v_p(self):
        for buf_color in self.init_params.keys():
            init_params = self.init_params.get(buf_color)
            density = init_params[0]
            v_p = init_params[1]
            elasticity_quotient = self.__calculate_lambda_lame(density, v_p)
            self.img_creating_parameters.update({buf_color: [density, elasticity_quotient, v_p]})

    # Calculates all parameters for acoustic_task in heterogeneous environment, knowing elasticity_quotient
    def __calculate_params_for_acoustic_task_k(self):
        for buf_color in self.init_params.keys():
            init_params = self.init_params.get(buf_color)
            density = init_params[0]
            elasticity_quotient = init_params[1]
            v_p = self.__calculate_v_p(density, elasticity_quotient)
            self.img_creating_parameters.update({buf_color: [density, elasticity_quotient, v_p]})

    # Calculates lambda_lame, knowing density and v_p
    def __calculate_lambda_lame(self, density, v_p):
        elasticity_quotient = (v_p ** 2) * density
        return elasticity_quotient

    # Calculates v_p, knowing density and elasticity_quotient
    def __calculate_v_p(self, density, elasticity_quotient):
        v_p = (elasticity_quotient / density) ** 0.5
        return v_p

    # Calculates all parameters for seismic_task in heterogeneous environment, knowing x and y velocities
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

    # Calculates all parameters for seismic_task in heterogeneous environment, knowing lame parameters
    def __calculate_params_for_seismic_task_lame(self):
        for buf_color in self.init_params.keys():
            init_params = self.init_params.get(buf_color)
            density = init_params[0]
            lambda_lame = init_params[1]
            mu_lame = init_params[2]
            self.set_dens_and_lame_for_seismic(density, lambda_lame, mu_lame)
            v_p = self.v_p
            v_s = self.v_s
            self.img_creating_parameters.update({buf_color: [density, lambda_lame, mu_lame, v_p, v_s]})

    # Calculates Lame parameters, Puasson's parameter and E parameter
    def __calculate_Lame_and_Puass_and_E(self):
        self.mu_lame = self.v_s ** 2 * self.density
        self.nu_puass = (2 * self.mu_lame - self.v_p ** 2 * self.density) / (2 * (self.mu_lame - self.v_p ** 2 * self.density))
        self.elasticity_quotient = 2 * self.mu_lame * self.nu_puass / (1 - 2 * self.nu_puass)
        self.E = self.mu_lame * (3 * self.elasticity_quotient + 2 * self.mu_lame) / (self.elasticity_quotient + self.mu_lame)

    # Calculates x and y velocities
    def __calculate_speeds(self):
        self.v_p = (self.E / self.density) ** 0.5
        self.v_s = (self.mu_lame / self.density) ** 0.5

    # Calculates Puasson's parameter and E parameter
    def __calculate_Puass_and_E(self):
        self.nu_puass = self.elasticity_quotient / (2 * (self.elasticity_quotient + self.mu_lame))
        # self.E = self.mu_lame * (3 * self.elasticity_quotient + 2 * self.mu_lame) / (self.elasticity_quotient + self.mu_lame)
        self.E = self.elasticity_quotient * (1 + self.nu_puass) * (1 - 2*self.nu_puass)/(self.nu_puass)



    def create_environment_for_seismic(self, x=15, y=15):
        """
                One of the main functions in class <Environment_properties> which returns the created environment field
                for seismic task according to the pack of input parameters:
                        (density, v_p, v_c) or (density, elasticity_quotient, mu_lame)

                Each element of returned <ndarray> contains list [v_p, v_s, density, elasticity_quotient, mu_lame]
                        which will be used in further calculations

                :param x:   Width
                :param y:   Height
                :return field:    numpy.ndarray(shape=(x, y))
        """
        square = [self.v_p, self.v_s, self.density, self.elasticity_quotient, self.mu_lame]
        field = np.ndarray(shape=(x, y), dtype=np.dtype(list))
        field.fill(square)
        return field

    def create_environment_for_acoustic(self, x=15, y=15):
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
        square = [self.v_p, self.density, self.elasticity_quotient]
        field = np.ndarray(shape=(x, y), dtype=np.dtype(list))
        field.fill(square)
        return field

    def create_environment_from_image(self, image_path):
        """
                        One of the main function in class <Environment_properties> which returns the created environment field
                        gathered from the picture with describes the environment
                        with proper parameters for seismic task for each
                        pixel<->(density, elasticity_quotient, mu_lame)
                        or pixel<->(density, v_p, v_c) or correspondingly for acoustic task :
                        pixel<->(density, v_p) or pixel<->(density, k)

                        Each element of returned <array> contains corresponding list with parameters:
                        [density, elasticity_quotient, mu_lame, v_p, v_s] for seismic and
                        [density=0, elasticity_quotient=0, v_p=0] for acoustic

                        :param image_path: The relative path to the image, which describes the environment
                        :return field:    numpy.ndarray(shape=(height, length)); each element of array contains properties of environment
                """
        picture_parser = visual_analyzer.visual_analyzer(image_path, self.img_creating_parameters)
        field = picture_parser.create_field()
        return field


# density = 1000
# v_p = 200
# v_s = 400
# mu_lame = 56
# elasticity_quotient = 12
# props = EnvironmentProperties(density, elasticity_quotient, mu_lame)
# field = props.create_environment_for_seismic()
# print(field)
# #
# image_path = "three_col.jpg"
# params = {(254, 242, 0): [1, 200, 30], (255, 255, 255): [2, 100, 10]}
# properties = EnvironmentProperties(img_creating_parameters=params)
# properties.set_params_for_seismic_using_lame()
# field = properties.create_environment_from_image(image_path)
# print(field[663][1626])
# print(field[600][230])

# buf = tuple(map(tuple, image[0][0]))
# print(buf[0])