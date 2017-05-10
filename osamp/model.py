import environment_properties as env
import matrix

class Model:
    """
    Model is a class, that contains information about formulation the problem
    The main data in model: matrix and property of class
    Model contain matrix of the acoustic/seismic equations
    
    """
    def __init__(self, arg):
        self.arg = arg
        self._type_problem = arg['type']
        self._dim = arg['dimension']
        self.lame = arg['lambda_lame']
        self._lamda_matrix = \
            matrix.get_matrix(self._dim, self._type_problem, [arg['lambda_lame'], arg['rho']])
        self._omega_matrix = \
            matrix.get_eign_matrix(self._dim, self._type_problem, [arg['lambda_lame'], arg['rho']])
        self._inverse_omega_matrix = \
            matrix.get_inv_eign_matrix(self._dim, self._type_problem, [arg['lambda_lame'], arg['rho']])
        self.env_prop = env.EnvironmentProperties(arg['rho'], arg['lambda_lame']) # arg['mu_lame'], arg['v_p'], arg['v_s']

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
        result_srt += ' lamda_matrix: ' + str(self._lamda_matrix)
        result_srt += ' omega_matrix: ' + str(self._omega_matrix)
        result_srt += ' inverse_omega_matrix: ' + str(self._inverse_omega_matrix)
        return result_srt