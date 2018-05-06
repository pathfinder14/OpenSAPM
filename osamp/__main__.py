import input_data
import solver as solver_module
import problem as problem_module

if __name__ == '__main__':
    problem_parametrs = input_data.get_parametrs()
    print(problem_parametrs)
    problem = problem_module.Problem(problem_parametrs)
    print(problem.grid._dt)
    print("AAA Matrix")
    print(problem.model.omega_a_matrix)
    print(problem.model.omega_b_matrix)
    print(problem.model.inverse_omega_a_matrix)
    print(problem.model._lamda_a_matrix)
    solver_module.Solver(problem)