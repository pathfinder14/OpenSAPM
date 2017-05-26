import numpy as np


class ConditionNames:
    def __init__(self):
        pass

    REFLECTION_CONDITION = 'reflection'
    CYCLE_CONDITION = 'cycle'
    ABSORBING_CONDITION = 'absorb'
    APPLIED_FORCE_CONDITION = 'applied_force'


class ProblemTypes:
    def __init__(self):
        pass

    ACOUSTIC = 'acoustic'
    SEISMIC = 'seismic'


class SolverMethods:
    def __init__(self):
        pass

    BIOCOMPACT = 'bicompact'
    LAX_WENDROFF = 'lax_wendroff'
    BEAM_WARMING = 'beam_warming'
    KIR = 'kir'
    TVD = 'tvd'

    cells_for_method = {BIOCOMPACT: (1, 1), LAX_WENDROFF: (3, 3), BEAM_WARMING: (1, 1), KIR: (1, 1), TVD: (1, 1)}

    @classmethod
    def get_cells_amount_left(cls, method_name):
        return cls.cells_for_method[method_name][0]

    @classmethod
    def get_cells_amount_right(cls, method_name):
        return SolverMethods.cells_for_method[method_name][1]


p = 0  # index of pressure in values array
v = 1  # index of velocity (x-component) in values array
u = 2  # index of velocity (y-component) in values array, only for 2d case


def border_condition_1d(grid, type_of_task, border_left, border_right, method_name, force_left=0, force_right=0):
    """
    Applies border conditions to 'grid' array and returns updated version of it.
    Needs to have 'type_of_task' and 'method_name' specified by a string from 'ProblemTypes' class.

    Additional arguments:
        - 'border_left'  - a string from 'ConditionNames' class, specifying type of left border;
        - 'border_right' - a string from 'ConditionNames' class, specifying type of right border;
        - 'force_left' - applied force at the left border;
        - 'force_right' - applied force at the right border
    """
    if type_of_task == ProblemTypes.ACOUSTIC:
        return border_condition_1d_acoustic(grid, type_of_task, border_left, border_right, method_name, force_left, force_right)
    elif type_of_task == ProblemTypes.SEISMIC:
        return border_condition_1d_seismic(grid, border_left, border_right, method_name, force_left, force_right)


def border_condition_2d(grid, type_of_task, border_left, border_right, method_name, force_top):
    """
    Applies border conditions to 'grid' array and returns updated version of it.
    Needs to have 'type_of_task' and 'method_name' specified by a string from 'ProblemTypes' class.

    Additional arguments:
        - 'border_left'  - a string from 'ConditionNames' class, specifying type of left border;
        - 'border_right' - a string from 'ConditionNames' class, specifying type of right border;
        - 'force_top' - applied force at the top. according to the formulation of the problem, force can be applied only at the top
    """
    if type_of_task == ProblemTypes.ACOUSTIC:
        return border_condition_2d_acoustic(grid, border_left, border_right, method_name, force_top)
    elif type_of_task == ProblemTypes.SEISMIC:
        return border_condition_2d_seismic(grid, border_left, border_right, method_name, force_top)


def border_condition_1d_acoustic(grid, type_of_task, border_left, border_right, method_name, force_left=0, force_right=0):
    cells_left = SolverMethods.get_cells_amount_left(method_name)
    cells_right = SolverMethods.get_cells_amount_right(method_name)

    grid_new = np.zeros((cells_left, 2))

    # Check left border.

    if border_left == ConditionNames.REFLECTION_CONDITION:
        for i in range(cells_left - 1, -1, -1):
            grid_new[i][p] = grid[cells_left - 1 - i][p]
            grid_new[i][v] = -grid[cells_left - 1 - i][v]

    elif border_left == ConditionNames.CYCLE_CONDITION:
        for i in range(cells_left - 1, -1, -1):
            grid_new[i] = grid[len(grid) - cells_left + i]
    #
    elif border_left == ConditionNames.ABSORBING_CONDITION:
        for i in range(cells_left - 1, -1, -1):
            grid_new[i] = grid[cells_left - 1 - i]

    elif border_left == ConditionNames.APPLIED_FORCE_CONDITION:
        for i in range(cells_left - 1, -1, -1):
            grid_new[i][v] = grid[cells_left - 1 - i][v]
            grid_new[i][p] = 2 * force_left - grid[cells_left - 1 - i][p]

    ext_grid = np.concatenate((grid_new, grid), axis=0)

    grid_new = np.zeros((cells_right, 2))

    # Check right border.
    if border_right == ConditionNames.REFLECTION_CONDITION:
        for i in range(cells_right - 1, -1, -1):
            grid_new[i][p] = grid[len(grid) - 1 - i][p]
            grid_new[i][v] = -grid[len(grid) - 1 - i][v]

    elif border_right == ConditionNames.CYCLE_CONDITION:
        for i in range(cells_right - 1, -1, -1):
            grid_new[i] = grid[i]

    elif border_right == ConditionNames.ABSORBING_CONDITION:
        for i in range(cells_right - 1, -1, -1):
            grid_new[i] = grid[len(grid) - 1 - i]

    elif border_right == ConditionNames.APPLIED_FORCE_CONDITION:
        for i in range(cells_right - 1, -1, -1):
            grid_new[i][v] = grid[len(grid) - 1 - i][v]
            grid_new[i][p] = 2 * force_right - grid[len(grid) - 1 - i][p]

    ext_grid = np.concatenate((ext_grid, grid_new), axis=0)
    return ext_grid


def border_condition(grid, type_of_task, border_left, border_right, method_name, tension, force_left=0, force_right=0):
    cells_left = SolverMethods.get_cells_amount_left(method_name)
    cells_right = SolverMethods.get_cells_amount_right(method_name)

    grid_new = np.zeros((cells_left, len(tension)))
    # Check left border.

    if border_left == ConditionNames.REFLECTION_CONDITION:
        for i in range(cells_left - 1, -1, -1):
            grid_new[i] = grid[cells_left - 1 - i]
            #grid_new[i][v] = -grid[cells_left - 1 - i][v]

    elif border_left == ConditionNames.CYCLE_CONDITION:
        for i in range(cells_left - 1, -1, -1):
            grid_new[i] = grid[len(grid) - cells_left + i]
    #
    elif border_left == ConditionNames.ABSORBING_CONDITION:
        for i in range(cells_left - 1, -1, -1):
            grid_new[i] = grid[cells_left - 1 - i]

    elif border_left == ConditionNames.APPLIED_FORCE_CONDITION:
        if type_of_task == 'acoustic':
            for i in range(cells_left - 1, -1, -1):
                grid_new[i][v] = grid[cells_left - 1 - i][v]
                grid_new[i][p] = 2 * force_left - grid[cells_left - 1 - i][p]
                grid_new[i][2] = grid[cells_left - 1 - i][2]
        else:#TODO you should create real applied force for seismic tension [sigma11, sigma22, sigma12, u, v]
            for i in range(cells_left - 1, -1, -1):
                grid_new[i][0] = 2 * force_left - grid[cells_left - 1 - i][0]
                grid_new[i][1] = 2 * force_left - grid[cells_left - 1 - i][1]
                grid_new[i][2] = grid[cells_left - 1 - i][2]
                grid_new[i][3] = grid[cells_left - 1 - i][3]
                grid_new[i][4] = grid[cells_left - 1 - i][4]



    ext_grid = np.concatenate((grid_new, grid), axis=0)

    grid_new = np.zeros((cells_right, len(tension)))

    # Check right border.
    if border_right == ConditionNames.REFLECTION_CONDITION:
        for i in range(cells_right - 1, -1, -1):
           grid_new[i] = grid[len(grid) - 1 - i]
    elif border_right == ConditionNames.CYCLE_CONDITION:
        for i in range(cells_right - 1, -1, -1):
            grid_new[i] = grid[i]

    elif border_right == ConditionNames.ABSORBING_CONDITION:
        for i in range(cells_right - 1, -1, -1):
            grid_new[i] = grid[len(grid) - 1 - i]

    elif border_right == ConditionNames.APPLIED_FORCE_CONDITION:
        if type_of_task == 'acoustic':
            for i in range(cells_left - 1, -1, -1):
                grid_new[i][v] = grid[cells_left - 1 - i][v]
                grid_new[i][p] = 2 * force_left - grid[cells_left - 1 - i][p]
                grid_new[i][2] = grid[cells_left - 1 - i][2]
        else:#TODO you should create real applied force for seismic tension [sigma11, sigma22, sigma12, u, v]
            for i in range(cells_left - 1, -1, -1):
                grid_new[i][0] = 2 * force_left - grid[cells_left - 1 - i][0]
                grid_new[i][1] = 2 * force_left - grid[cells_left - 1 - i][1]
                grid_new[i][2] = grid[cells_left - 1 - i][2]
                grid_new[i][3] = grid[cells_left - 1 - i][3]
                grid_new[i][4] = grid[cells_left - 1 - i][4]


    ext_grid = np.concatenate((ext_grid, grid_new), axis=0)
    return ext_grid

def border_condition_1d_seismic(arr, border_left, border_right, method_name, force_left, force_right):
    # for 1d seismic and acoustic conditions are the same
    return border_condition_1d_acoustic(arr, border_left, border_right, method_name, force_left, force_right)


def border_condition_2d_acoustic(grid, border_left, border_right, method_name, force_top):
    cells_left = SolverMethods.get_cells_amount_left(method_name)
    cells_right = SolverMethods.get_cells_amount_right(method_name)

    grid_new = np.zeros((cells_left, 3))

    # Check left border.

    if border_left == ConditionNames.REFLECTION_CONDITION:
        for i in range(cells_left - 1, -1, -1):
            grid_new[i][p] = grid[cells_left - 1 - i][p]
            grid_new[i][v] = -grid[cells_left - 1 - i][v]
            grid_new[i][u] = -grid[cells_left - 1 - i][u]

    elif border_left == ConditionNames.CYCLE_CONDITION:
        for i in range(cells_left - 1, -1, -1):
            grid_new[i] = grid[len(grid) - cells_left + i]
    #
    elif border_left == ConditionNames.ABSORBING_CONDITION:
        for i in range(cells_left - 1, -1, -1):
            grid_new[i] = grid[cells_left - 1 - i]

    elif border_left == ConditionNames.APPLIED_FORCE_CONDITION:
        for i in range(cells_left - 1, -1, -1):
            grid_new[i][v] = grid[cells_left - 1 - i][v]
            grid_new[i][u] = grid[cells_left - 1 - i][u]
            grid_new[i][p] = 2 * force_top - grid[cells_left - 1 - i][p]

    ext_grid = np.concatenate((grid_new, grid), axis=0)

    grid_new = np.zeros((cells_right, 3))

    # Check right border.
    if border_right == ConditionNames.REFLECTION_CONDITION:
        for i in range(cells_right - 1, -1, -1):
            grid_new[i][p] = grid[len(grid) - 1 - i][p]
            grid_new[i][v] = -grid[len(grid) - 1 - i][v]
            grid_new[i][u] = -grid[len(grid) - 1 - i][u]

    elif border_right == ConditionNames.CYCLE_CONDITION:
        for i in range(cells_right - 1, -1, -1):
            grid_new[i] = grid[i]

    elif border_right == ConditionNames.ABSORBING_CONDITION:
        for i in range(cells_right - 1, -1, -1):
            grid_new[i] = grid[len(grid) - 1 - i]

    elif border_right == ConditionNames.APPLIED_FORCE_CONDITION:
        raise Exception('Applied force condition can be used only at the top.')

    ext_grid = np.concatenate((ext_grid, grid_new), axis=0)
    return ext_grid


def border_condition_2d_seismic(grid, border_left, border_right, method_name, force_top):
    pass

# print border_condition_2d([[0, 1, 2], [1, 2, 3], [2, 3, 4], [4, 5, 5], [5, 6, 6]], ProblemTypes.ACOUSTIC, ConditionNames.APPLIED_FORCE_CONDITION, ConditionNames.CYCLE_CONDITION, SolverMethods.BEAM_WARMING, 5)

#
# print border_condition_2d(np.array([[[11,11,11],[12,12,12],[13,13,13]],
# [[21,21,21],[22,22,22],[23,23,23]],
# [[31,31,31],[32,32,32],[33,33,33]]]), ProblemTypes.ACOUSTIC, ConditionNames.CYCLE_CONDITION, ConditionNames.CYCLE_CONDITION, ConditionNames.APPLIED_FORCE_CONDITION,
#                           ConditionNames.CYCLE_CONDITION, SolverMethods.BIOCOMPACT, 15)
