import environment_properties as env
import matrix

class Model(list_of_user_data):
    """
    Model is a class, that contains information about formulation the problem
    The main data in model: matrix and property of class
    Model contain matrix of the acoustic/seismic equations
    
    """
    def __init__(self, arg):
        self.arg = arg
        self._type_eq = arg['type']
        self._dim = arg['dim']
        self._a_matrix = matrix.get_matrix(self.dim, self.type_eq)
        self._omega_matrix = matrix.get_eign_matrix(self.dim, self.type_eq)
        self._inverse_omega_matrix = matrix.get_inv_eign_matrix(self.dim, self.type_eq)
        self.env_prop = env.EnvironmentProperties(arg['rho'], arg['lambda_lame'], arg['mu_lame'], arg['v_p'], arg['v_s'])
        self.

    @property
    def a_matrix(self):
        return self._a_matrix


    @property
    def type_eq(self):
        return self._type_eq
    
    @property
    def dim(self):
        return self._dim