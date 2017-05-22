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
v = 1  # index of velocity in values array


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
    # for now seismic and acoustic border conditions do the same thing, but it's not the rule.
    # fixme
    return border_condition_1d_acoustic(arr, border_left, border_right, method_name, force_left, force_right)


# print border_condition_1d([[0, 1], [1, 2], [2, 3], [4, 5], [5, 6]], ProblemTypes.ACOUSTIC, ConditionNames.APPLIED_FORCE_CONDITION, ConditionNames.APPLIED_FORCE_CONDITION, SolverMethods.BEAM_WARMING)
