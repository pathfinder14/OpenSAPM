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
        self._type_problem = config['type']
        self._dim = config['dimension']
        self._elasticity_quotient = config['elasticity_quotient']
        self.env_prop = env.EnvironmentProperties(
            config['density'], config['elasticity_quotient'], config['mu_lame'],
            config['x_velocity'], config['x_velocity'])
        self._lamda_matrix = \
            matrix.get_matrix(self._dim, self._type_problem, self.env_prop.elasticity_quotient,
                              self.env_prop.density, self.env_prop.mu_lame)
        self._omega_matrix = \
            matrix.get_eign_matrix(self._dim, self._type_problem, self.env_prop.elasticity_quotient,
                                   self.env_prop.density, self.env_prop.mu_lame)
        self._inverse_omega_matrix = \
            matrix.get_inv_eign_matrix(self._dim, self._type_problem, self.env_prop.elasticity_quotient,
                                       self.env_prop.density, self.env_prop.mu_lame)


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

    def __str__(self):
        result_srt = ''
        result_srt += '\nlamda_matrix: ' + str(self._lamda_matrix)
        result_srt += '\nomega_matrix: ' + str(self._omega_matrix)
        result_srt += '\ninverse_omega_matrix: ' + str(self._inverse_omega_matrix)
        return result_srt