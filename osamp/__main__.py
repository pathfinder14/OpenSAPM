import input_data
import solver as solver_module
import problem as problem_module

if __name__ == '__main__':
    problem_parametrs = input_data.get_parametrs()
    problem = problem_module.Problem(problem_parametrs)
    solver.solve(problem)