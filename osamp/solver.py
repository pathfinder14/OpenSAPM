from problem import Problem

class Solver(Problem):
    """
    Solver class for simulations. 
    Time axis is labed as t, spaces ax, ay
    
    """
    def __init__(self, Problem):
        super(Solver, self).__init__()
        self.problem = Problem
        self.cfl = 0.1 #TODO change this parametrs to user's propertyies
        self.dimension = problem.dimension
        problem = self.problem
        matrix_of_eigns = problem.model.lambda_matrix
        omega_matrix = problem.model.omega_matrix
        inv_matrix = problem.model.inverse_omega_matrix
        grid = problem.grid
        #solve dv/dt=a dv/dx
        #TODO: find information v = omega*u
        num_of_equation = len(matrix_of_eigns)
        v = np.zeros(num_of_equation)
        u = np.zeros(num_of_equation)
        grid[0]
        for i in xrange(num_of_equation):
            #v = np.dot(omega_matrix, u)
            v[i] = kir(problem.grid.shape[0], problem.grid.shape[1], problem.grid, lambda_matrix[i], cfl, 1)
            u[i] = np.dot(inv_matrix, v[i])



def _generate_border_conditions(self):
    if self._dimension == 1:
        return border_conditions.border_condition_1d(self._grid, TODO, TODO)
        # TODO: no idea what to pass as parameters cause method signature is not easily understandable
    elif self._dimension == 2:
        return border_conditions.border_condition_2d()