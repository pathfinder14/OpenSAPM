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
    WENO = 'weno'
    MCCORMACK = "McCormack"

    cells_for_method = {BIOCOMPACT: (1, 1), LAX_WENDROFF: (3, 3), BEAM_WARMING: (1, 1), KIR: (1, 1), TVD: (1, 1), WENO: (1, 1),MCCORMACK : (2,2) }

    @classmethod
    def get_cells_amount_left(cls, method_name):
        return SolverMethods.cells_for_method[method_name][0]

    @classmethod
    def get_cells_amount_right(cls, method_name):
        return SolverMethods.cells_for_method[method_name][1]


class Directions:
    def __init__(self):
        pass

    X = 'x'
    Y = 'y'


p = 0  # index of pressure in values array
v = 1  # index of velocity (x-component) in values array
u = 2  # index of velocity (y-component) in values array, only for 2d case


def border_condition_1d(grid, type_of_task, border_left, border_right, method_name, time, force_left=0, force_right=0):
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
        return border_condition_1d_acoustic(grid, type_of_task, border_left, border_right, method_name, time, force_left,
                                            force_right)
    elif type_of_task == ProblemTypes.SEISMIC:
        return border_condition_1d_seismic(grid, type_of_task, border_left, border_right, method_name, time, force_left,
                                           force_right)


def border_condition_1d_acoustic(grid, type_of_task, border_left, border_right, method_name, time, force_left=0,
                                 force_right=0):
    cells_left = SolverMethods.get_cells_amount_left(method_name)
    cells_right = SolverMethods.get_cells_amount_right(method_name)
    sizes = [len(grid[0]), len(grid[0][0])]
    grid_new = np.zeros((cells_left, sizes[0], sizes[1]))

    # Check left border.
    if border_left == ConditionNames.REFLECTION_CONDITION:
        for i in range(cells_left - 1, -1, -1):
            grid_new[i][time][p] = grid[cells_left - 1 - i][time][p]
            grid_new[i][time][v] = -grid[cells_left - 1 - i][time][v]

    elif border_left == ConditionNames.CYCLE_CONDITION:
        for i in range(cells_left - 1, -1, -1):
                grid_new[i][time] = grid[len(grid) - cells_left + i][time]
    #
    elif border_left == ConditionNames.ABSORBING_CONDITION:
        for i in range(cells_left - 1, -1, -1):
                grid_new[i][time] = grid[cells_left - 1 - i][time]

    elif border_left == ConditionNames.APPLIED_FORCE_CONDITION:
        for i in range(cells_left - 1, -1, -1):
            grid_new[i][time][v] = grid[cells_left - 1 - i][time][v]
            grid_new[i][time][p] = 2 * force_left - grid[cells_left - 1 - i][time][p]

    ext_grid = np.concatenate((grid_new, grid), axis=0)

    grid_new = np.zeros((cells_right, sizes[0], sizes[1]))

    # Check right border.
    if border_right == ConditionNames.REFLECTION_CONDITION:
        for i in range(cells_right - 1, -1, -1):
                grid_new[i][time][p] = grid[len(grid) - 1 - i][time][p]
                grid_new[i][time][v] = -grid[len(grid) - 1 - i][time][v]

    elif border_right == ConditionNames.CYCLE_CONDITION:
        for i in range(cells_right - 1, -1, -1):
            grid_new[i][time] = grid[i][time]

    elif border_right == ConditionNames.ABSORBING_CONDITION:
        for i in range(cells_right - 1, -1, -1):
            grid_new[i][time] = grid[len(grid) - 1 - i][time]

    elif border_right == ConditionNames.APPLIED_FORCE_CONDITION:
        for i in range(cells_right - 1, -1, -1):
            grid_new[i][time][v] = grid[len(grid) - 1 - i][time][v]
            grid_new[i][time][p] = 2 * force_right - grid[len(grid) - 1 - i][time][p]

    ext_grid = np.concatenate((ext_grid, grid_new), axis=0)
    return ext_grid


def border_condition_1d_seismic(arr, type_of_task, border_left, border_right, method_name, time, force_left, force_right):
    # for 1d seismic and acoustic conditions are the same
    return border_condition_1d_acoustic(arr, type_of_task, border_left, border_right, method_name, time, force_left,
                                        force_right)


def border_condition_2d_acoustic(grid, border_left, border_right, method_name, time, direction=Directions.X,
                                 force_left=0, force_right=0):
    cells_left = SolverMethods.get_cells_amount_left(method_name)
    cells_right = SolverMethods.get_cells_amount_right(method_name)

    grid_new = np.zeros((cells_left, 3))

    # Check left border.

    if border_left == ConditionNames.REFLECTION_CONDITION:
        for i in range(cells_left - 1, -1, -1):
            if direction == Directions.X:
                grid_new[i][v] = -grid[cells_left - 1 - i][v]
                grid_new[i][u] = grid[cells_left - 1 - i][u]
            else:
                grid_new[i][v] = grid[cells_left - 1 - i][v]
                grid_new[i][u] = -grid[cells_left - 1 - i][u]
            grid_new[i][p] = grid[cells_left - 1 - i][p]


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
            grid_new[i][p] = 2 * force_left - grid[cells_left - 1 - i][p]

    ext_grid = np.concatenate((grid_new, grid), axis=0)

    grid_new = np.zeros((cells_right, 3))

    # Check right border.
    if border_right == ConditionNames.REFLECTION_CONDITION:
        for i in range(cells_right - 1, -1, -1):
            if direction == Directions.X:
                grid_new[i][v] = -grid[len(grid) - 1 - i][v]
                grid_new[i][u] = grid[len(grid) - 1 - i][u]
            else:
                grid_new[i][v] = grid[len(grid) - 1 - i][v]
                grid_new[i][u] = -grid[len(grid) - 1 - i][u]
            grid_new[i][p] = grid[len(grid) - 1 - i][p]

    elif border_right == ConditionNames.CYCLE_CONDITION:
        for i in range(cells_right - 1, -1, -1):
            grid_new[i] = grid[i]

    elif border_right == ConditionNames.ABSORBING_CONDITION:
        for i in range(cells_right - 1, -1, -1):
            grid_new[i] = grid[len(grid) - 1 - i]

    elif border_right == ConditionNames.APPLIED_FORCE_CONDITION:
        for i in range(cells_left - 1, -1, -1):
            grid_new[i][v] = grid[len(grid) - 1 - i][v]
            grid_new[i][u] = grid[len(grid) - 1 - i][u]
            grid_new[i][p] = 2 * force_right - grid[len(grid) - 1 - i][p]

    ext_grid = np.concatenate((ext_grid, grid_new), axis=0)
    return ext_grid


s11 = 0
s22 = 1
s12 = 2
vx = 3
vy = 4  # v is already existing


def border_condition_2d_seismic(grid, border_left, border_right, method_name, time, direction=Directions.X, force_left=0,
                                force_right=0):
    """Border condition for 2d seismic equation"""

    cells_left = SolverMethods.get_cells_amount_left(method_name)
    cells_right = SolverMethods.get_cells_amount_right(method_name)

    grid_new = np.zeros((cells_left, 5))

    if direction == Directions.X:
        s_main = s11
        s_extra = s22

        v_main = vx
        v_extra = vy

    else:
        s_main = s22
        s_extra = s11

        v_main = vy
        v_extra = vx

    # Check left border.
    if border_left == ConditionNames.REFLECTION_CONDITION:
        for i in range(cells_left - 1, -1, -1):
            grid_new[i][s11] = grid[cells_left - 1 - i][s11]
            grid_new[i][s22] = grid[cells_left - 1 - i][s22]
            grid_new[i][s12] = grid[cells_left - 1 - i][s12]
            grid_new[i][v_main] = -grid[cells_left - 1 - i][v_main]
            grid_new[i][v_extra] = grid[cells_left - 1 - i][v_extra]

    elif border_left == ConditionNames.CYCLE_CONDITION:
        for i in range(cells_left - 1, -1, -1):
            grid_new[i] = grid[len(grid) - cells_left + i]
    #
    elif border_left == ConditionNames.ABSORBING_CONDITION:
        for i in range(cells_left - 1, -1, -1):
            grid_new[i] = grid[cells_left - 1 - i]

    elif border_left == ConditionNames.APPLIED_FORCE_CONDITION:
        for i in range(cells_left - 1, -1, -1):
            grid_new[i][s_main] = 2 * force_left - grid[cells_left - 1 - i][s_main]
            grid_new[i][s12] = 2 * force_left - grid[cells_left - 1 - i][s12]
            grid_new[i][s_extra] = grid[cells_left - 1 - i][s_extra]
            grid_new[i][vx] = grid[cells_left - 1 - i][vx]
            grid_new[i][vy] = grid[cells_left - 1 - i][vy]

    ext_grid = np.concatenate((grid_new, grid), axis=0)

    grid_new = np.zeros((cells_right, 5))

    # Check right border.
    if border_right == ConditionNames.REFLECTION_CONDITION:
        for i in range(cells_right - 1, -1, -1):
            grid_new[i][s11] = grid[len(grid) - 1 - i][s11]
            grid_new[i][s22] = grid[len(grid) - 1 - i][s22]
            grid_new[i][s12] = grid[len(grid) - 1 - i][s12]
            grid_new[i][v_main] = -grid[len(grid) - 1 - i][v_main]
            grid_new[i][v_extra] = grid[len(grid) - 1 - i][v_extra]

    elif border_right == ConditionNames.CYCLE_CONDITION:
        for i in range(cells_right - 1, -1, -1):
            grid_new[i] = grid[i]

    elif border_right == ConditionNames.ABSORBING_CONDITION:
        for i in range(cells_right - 1, -1, -1):
            grid_new[i] = grid[len(grid) - 1 - i]

    elif border_right == ConditionNames.APPLIED_FORCE_CONDITION:
        for i in range(cells_left - 1, -1, -1):
            grid_new[i][s_main] = 2 * force_right - grid[len(grid) - 1 - i][s_main]
            grid_new[i][s12] = 2 * force_right - grid[len(grid) - 1 - i][s12]
            grid_new[i][s_extra] = grid[len(grid) - 1 - i][s_extra]
            grid_new[i][vx] = grid[len(grid) - 1 - i][vx]
            grid_new[i][vy] = grid[len(grid) - 1 - i][vy]

    ext_grid = np.concatenate((ext_grid, grid_new), axis=0)
    return ext_grid


def border_condition_2d(grid, type_of_task, border_left, border_right, method_name, time, direction=Directions.X,
                        force_left=0, force_right=0):
    """
    Applies border conditions to 'grid' array and returns updated version of it.
    Needs to have 'type_of_task' and 'method_name' specified by a string from 'ProblemTypes' class.
    Additional arguments:
        - 'border_left'  - a string from 'ConditionNames' class, specifying type of left border;
        - 'border_right' - a string from 'ConditionNames' class, specifying type of right border;
        - 'force_top' - applied force at the top. according to the formulation of the problem, force can be applied only at the top
    """
    if type_of_task == ProblemTypes.ACOUSTIC:
        return border_condition_2d_acoustic(grid, border_left, border_right, method_name, time, direction, force_left,
                                            force_right)
    elif type_of_task == ProblemTypes.SEISMIC:
        return border_condition_2d_seismic(grid, border_left, border_right, method_name, time, direction, force_left,
                                           force_right)

# print border_condition_2d([[0, 1, 2, 3, 4], [1, 2, 3, 4, 5], [2, 3, 4, 4, 5], [4, 5, 5, 5, 5], [5, 6, 6, 7, 7
#                                                                                                 ]],
#                           ProblemTypes.SEISMIC,
#                           ConditionNames.REFLECTION_CONDITION, ConditionNames.REFLECTION_CONDITION,
#                           SolverMethods.BEAM_WARMING,
#                           Directions.X)

#
# print border_condition_2d(np.array([[[11,11,11],[12,12,12],[13,13,13]],
# [[21,21,21],[22,22,22],[23,23,23]],
# [[31,31,31],[32,32,32],[33,33,33]]]), ProblemTypes.ACOUSTIC, ConditionNames.CYCLE_CONDITION, ConditionNames.CYCLE_CONDITION, ConditionNames.APPLIED_FORCE_CONDITION,
#                           ConditionNames.CYCLE_CONDITION, SolverMethods.BIOCOMPACT, 15)
