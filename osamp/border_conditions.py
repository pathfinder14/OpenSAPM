class ConditionNames:
    def __init__(self):
        pass

    REFLECTION_CONDITION = 'reflection'
    CYCLE_CONDITION = 'cycle'
    ABSORBING_CONDITION = 'absorb'


class ProblemTypes:
    def __init__(self):
        pass

    ACOUSTIC = 'acoustic'
    SEISMIC = 'seismic'


p = 0 # index of pressure (?) in values array
v = 1 # index of velocity in values array


def border_condition_1d(grid, type_of_task, border_left, border_right):
    """
    Applies border conditions to 'grid' array and returns updated version of it.
    Needs to have 'type_of_task' specified by a string from 'ProblemTypes' class.

    Additional arguments:
        - 'border_left'  - a string from 'ConditionNames' class, specifying type of left border;
        - 'border_right' - a string from 'ConditionNames' class, specifying type of right border;
    """
    if type_of_task == ProblemTypes.ACOUSTIC:
        return border_condition_1d_acoustic(grid, border_left, border_right)
    elif type_of_task == ProblemTypes.SEISMIC:
        return border_condition_1d_seismic(grid, border_left, border_right)


def border_condition_1d_acoustic(grid, border_left, border_right):
    grid_copy = grid[:]

    # Check left border.
    if border_left == ConditionNames.REFLECTION_CONDITION:
        grid_copy[0][p] = -grid[0][p]
        grid_copy[0][v] = -grid[0][v]

        grid_copy[1][p] = -grid[1][p]
        grid_copy[1][v] = -grid[1][v]

    elif border_left == ConditionNames.CYCLE_CONDITION:
        grid_copy[1][p] = grid[len(grid) - 1][p]
        grid_copy[1][v] = grid[len(grid) - 1][v]

        grid_copy[0][p] = grid[len(grid) - 2][p]
        grid_copy[0][v] = grid[len(grid) - 2][v]

    elif border_left == ConditionNames.ABSORBING_CONDITION:
        grid_copy[1][p] = 0
        grid_copy[1][v] = 0

        grid_copy[0][p] = 0
        grid_copy[0][v] = 0

        # else:
        # todo add new methods

    # Check right border.
    if border_right == ConditionNames.REFLECTION_CONDITION:
        grid_copy[len(grid) - 1][p] = -grid[len(grid) - 1][p]
        grid_copy[len(grid) - 1][v] = -grid[len(grid) - 1][v]

        grid_copy[len(grid) - 2][p] = -grid[len(grid) - 2][p]
        grid_copy[len(grid) - 2][v] = -grid[len(grid) - 2][v]

    elif border_right == ConditionNames.CYCLE_CONDITION:
        grid_copy[len(grid) - 1][p] = grid[1][p]
        grid_copy[len(grid) - 1][v] = grid[1][v]

        grid_copy[len(grid) - 2][p] = grid[0][p]
        grid_copy[len(grid) - 2][v] = grid[0][v]

    elif border_right == ConditionNames.ABSORBING_CONDITION:
        grid_copy[len(grid) - 1][p] = 0
        grid_copy[len(grid) - 1][v] = 0

        grid_copy[len(grid) - 2][p] = 0
        grid_copy[len(grid) - 2][v] = 0

        # else:
        # todo add new methods

    return grid_copy


def border_condition_1d_seismic(arr, border_left, border_right):
    # for now seismic and acoustic border conditions do the same thing, but it's not the rule.
    # fixme
    return border_condition_1d_acoustic(arr, border_left, border_right)
