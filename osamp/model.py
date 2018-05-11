import environment_properties as env
import matrix

class Model:
    """
    Model is a class, that contains information about formulation the problem
    The main data in model: matrix and property of class
    Model contain matrix of the acoustic/seismic equations
    
    """
    def __init__(self, config):
        self.arg = config
        self._n = [0 for i in range(2)]
        self._type_problem = config['type']
        self._dim = config['dimension']
        self._image_path = config['image_path']
        self._n[0] = config['n_x']
        self._n[1] = config['n_y']
        self._elasticity_quotient = config['elasticity_quotient']
        self.env_prop = env.EnvironmentProperties(
            config['density'], config['elasticity_quotient'], config['mu_lame'],
            config['v_p'], config['v_p'])
        if ((self._type_problem == 'acoustic') & (self._dim == 2)):
            self._omega_a_matrix = matrix.get_omega_a_matrix(self.type_problem, self.env_prop)
            self._omega_b_matrix = matrix.get_omega_b_matrix(self.type_problem, self.env_prop)
            self._lamda_a_matrix = matrix.get_lambda_ab_matrix(self.type_problem, self.env_prop) / self.n[0]
            self._lamda_b_matrix = matrix.get_lambda_ab_matrix(self.type_problem, self.env_prop) / self.n[1]
            self._inverse_omega_a_matrix = matrix.inverse_matrix(self._omega_a_matrix)
            self._inverse_omega_b_matrix = matrix.inverse_matrix(self._omega_b_matrix)
        else:
            self._lamda_matrix = \
            matrix.get_matrix(self._dim, self._type_problem, self.env_prop)
            self._omega_matrix = \
            matrix.get_eign_matrix(self._dim, self._type_problem, self.env_prop, self._n)
            self._inverse_omega_matrix = \
            matrix.get_inv_eign_matrix(self._dim, self._type_problem, self.env_prop, self._n)







    @property
    def lambda_matrix(self):
        return self._lamda_matrix

    @property
    def omega_matrix(self):
        return self._omega_matrix

    @property
    def inverse_omega_matrix(self):
        return self._inverse_omega_matrix

    @property
    def type_problem(self):
        return self._type_problem
    
    @property
    def dim(self):
        return self._dim

    @property
    def n(self):
        return self._n

    @property
    def omega_a_matrix(self):
        return self._omega_a_matrix

    @property
    def omega_b_matrix(self):
        return self._omega_b_matrix

    @property
    def inverse_omega_a_matrix(self):
        return self._inverse_omega_a_matrix

    @property
    def inverse_omega_b_matrix(self):
        return self._inverse_omega_b_matrix

    def __str__(self):
        result_srt = ''
        result_srt += '\nlamda_matrix: ' + str(self._lamda_matrix)
        result_srt += '\nomega_matrix: ' + str(self._omega_matrix)
        result_srt += '\ninverse_omega_matrix: ' + str(self._inverse_omega_matrix)
        return result_srt