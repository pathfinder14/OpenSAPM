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
        return border_condition_1d_acoustic(grid, border_left, border_right, method_name, force_left, force_right)
    elif type_of_task == ProblemTypes.SEISMIC:
        return border_condition_1d_seismic(grid, border_left, border_right, method_name, force_left, force_right)


def border_condition_2d(grid, type_of_task, border_left, border_right, border_top, border_down, method_name, force_top):
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
        return border_condition_2d_acoustic(grid, type_of_task, border_left, border_right, border_top, border_down,
                                            method_name, force_top)
    elif type_of_task == ProblemTypes.SEISMIC:
        return border_condition_2d_seismic(grid, type_of_task, border_left, border_right, border_top, border_down,
                                           method_name, force_top)


def border_condition_1d_acoustic(grid, border_left, border_right, method_name, force_left=0, force_right=0):
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


def border_condition_1d_seismic(arr, border_left, border_right, method_name, force_left, force_right):
    # for 1d seismic and acoustic conditions are the same
    return border_condition_1d_acoustic(arr, border_left, border_right, method_name, force_left, force_right)


def border_condition_2d_acoustic(grid, type_of_task, border_left, border_right, border_top, border_down,
                                 method_name,
                                 force_top):
    cells_left = SolverMethods.get_cells_amount_left(method_name)
    cells_right = SolverMethods.get_cells_amount_right(method_name)

    grid_new = np.zeros((len(grid), cells_left, 3))

    # Check left border.

    if border_left == ConditionNames.REFLECTION_CONDITION:
        for i in range(len(grid)):
            for j in range(cells_left - 1, -1, -1):
                grid_new[i][j][p] = grid[i][cells_left - 1 - j][p]
                grid_new[i][j][v] = -grid[i][cells_left - 1 - j][v]
                grid_new[i][j][u] = -grid[i][cells_left - 1 - j][u]

    elif border_left == ConditionNames.CYCLE_CONDITION:
        for i in range(len(grid)):
            for j in range(cells_left - 1, -1, -1):
                grid_new[i][j] = grid[i][len(grid) - cells_left + j]
    #
    elif border_left == ConditionNames.ABSORBING_CONDITION:
        for i in range(len(grid)):
            for j in range(cells_left - 1, -1, -1):
                grid_new[i][j] = grid[i][cells_left - 1 - j]

    elif border_left == ConditionNames.APPLIED_FORCE_CONDITION:
        raise Exception('Applied force boundary condition is supported only at the top')


    ext_grid = np.concatenate((grid_new, grid), axis=1)

    grid_new = np.zeros((len(grid), cells_right, 3))

    # Check right border.
    if border_right == ConditionNames.REFLECTION_CONDITION:
        for i in range(len(grid)):
            for j in range(cells_right - 1, -1, -1):
                grid_new[i][j][p] = grid[i][len(grid) - 1 - j][p]
                grid_new[i][j][v] = -grid[i][len(grid) - 1 - j][v]
                grid_new[i][j][u] = -grid[i][len(grid) - 1 - j][u]

    elif border_right == ConditionNames.CYCLE_CONDITION:
        for i in range(len(grid)):
            for j in range(cells_right - 1, -1, -1):
                grid_new[i][j] = grid[i][j]

    elif border_right == ConditionNames.ABSORBING_CONDITION:
        for i in range(len(grid)):
            for j in range(cells_right - 1, -1, -1):
                grid_new[i][j] = grid[i][len(grid) - 1 - j]

    elif border_right == ConditionNames.APPLIED_FORCE_CONDITION:
        raise Exception('Applied force boundary condition is supported only at the top')

    ext_grid = np.concatenate((ext_grid, grid_new), axis=1)

    # check top

    grid_new = np.zeros((cells_right, len(grid), 3))

    if border_top == ConditionNames.REFLECTION_CONDITION:
        for i in range(len(grid)):
            for j in range(cells_left - 1, -1, -1):
                grid_new[j][i][p] = grid[cells_left - 1 - j][i][p]
                grid_new[j][i][v] = -grid[cells_left - 1 - j][i][v]
                grid_new[j][i][u] = -grid[cells_left - 1 - j][i][u]

    elif border_top == ConditionNames.CYCLE_CONDITION:
        for i in range(len(grid)):
            for j in range(cells_left - 1, -1, -1):
                grid_new[j][i] = grid[len(grid) - cells_left + j][i]
    #
    elif border_top == ConditionNames.ABSORBING_CONDITION:
        for i in range(len(grid)):
            for j in range(cells_left - 1, -1, -1):
                grid_new[j][i] = grid[cells_left - 1 - j][i]

    elif border_top == ConditionNames.APPLIED_FORCE_CONDITION:
        for i in range(len(grid)):
            for j in range(cells_left - 1, -1, -1):
                grid_new[j][i][v] = grid[cells_left - 1 - j][i][v]
                grid_new[j][i][u] = grid[cells_left - 1 - j][i][u]
                grid_new[j][i][p] = 2 * force_top - grid[cells_left - 1 - j][i][p]


    cells_top = cells_right # fixme
    grid_new = np.concatenate((np.zeros((cells_top, cells_left, 3)), grid_new), axis = 1)
    grid_new = np.concatenate((grid_new, np.zeros((cells_top, cells_right, 3))), axis = 1)

    ext_grid = np.concatenate((grid_new, ext_grid), axis=0)

    # check bottom

    grid_new = np.zeros((cells_right, len(grid), 3))

    if border_down == ConditionNames.REFLECTION_CONDITION:
        for i in range(len(grid)):
            for j in range(cells_left - 1, -1, -1):
                grid_new[j][i][p] = grid[len(grid) - 1 - j][i][p]
                grid_new[j][i][v] = -grid[len(grid) - 1 - j][i][v]
                grid_new[j][i][u] = -grid[len(grid) - 1 - j][i][u]

    elif border_down == ConditionNames.CYCLE_CONDITION:
        for i in range(len(grid)):
            for j in range(cells_left - 1, -1, -1):
                grid_new[j][i] = grid[j][i]
    #
    elif border_down == ConditionNames.ABSORBING_CONDITION:
        for i in range(len(grid)):
            for j in range(cells_left - 1, -1, -1):
                grid_new[j][i] = grid[len(grid) - 1 - j][i]

    elif border_down == ConditionNames.APPLIED_FORCE_CONDITION:
        raise Exception('Applied force boundary condition is supported only at the top')

    cells_down = cells_left  # fixme
    grid_new = np.concatenate((np.zeros((cells_down, cells_left, 3)), grid_new), axis=1)
    grid_new = np.concatenate((grid_new, np.zeros((cells_down, cells_right, 3))), axis=1)

    ext_grid = np.concatenate((ext_grid, grid_new), axis=0)

    return ext_grid


def border_condition_2d_seismic(grid, type_of_task, border_left, border_right, border_top, border_down, method_name,
                                force_top):
    pass

# print border_condition_1d([[0, 1], [1, 2], [2, 3], [4, 5], [5, 6]], ProblemTypes.ACOUSTIC, ConditionNames.APPLIED_FORCE_CONDITION, ConditionNames.APPLIED_FORCE_CONDITION, SolverMethods.BEAM_WARMING)


print border_condition_2d(np.array([[[11,11,11],[12,12,12],[13,13,13]],
[[21,21,21],[22,22,22],[23,23,23]],
[[31,31,31],[32,32,32],[33,33,33]]]), ProblemTypes.ACOUSTIC, ConditionNames.CYCLE_CONDITION, ConditionNames.CYCLE_CONDITION, ConditionNames.APPLIED_FORCE_CONDITION,
                          ConditionNames.CYCLE_CONDITION, SolverMethods.BIOCOMPACT, 15)



