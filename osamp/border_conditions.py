from grid import GridElement1d, Grid1d
from methods import MethodNames


def border_condition_1d(grid, left, right):
    arr = grid.elements
    arrnew = []

    # Check left border.

    if left == MethodNames.REFLECTION_METHOD and len(arr) > 2:
        arrnew.append(GridElement1d(-arr[1].sigma, -1 * arr[1].velocity))
        arrnew.append(GridElement1d(-arr[0].sigma, -1 * arr[0].velocity))

    elif left == MethodNames.CYCLE_METHOD and len(arr) > 2:
        arrnew.append(GridElement1d(arr[len(arr) - 2].sigma, arr[len(arr) - 2].velocity))
        arrnew.append(GridElement1d(arr[len(arr) - 1].sigma, arr[len(arr) - 1].velocity))

    else:
        arrnew.append(GridElement1d(arr[1].sigma, arr[1].velocity))
        arrnew.append(GridElement1d(arr[0].sigma, arr[0].velocity))

    # Add original points.

    arrnew.extend(arr)

    # Check right border.

    if right == MethodNames.REFLECTION_METHOD and len(arr) > 2:
        arrnew.append(GridElement1d(- arr[len(arr) - 1].sigma, -1 * arr[len(arr) - 1].velocity))
        arrnew.append(GridElement1d(- arr[len(arr) - 2].sigma, -1 * arr[len(arr) - 2].velocity))

    elif right == MethodNames.CYCLE_METHOD and len(arr) > 2:
        arrnew.append(GridElement1d(arr[0].sigma, arr[0].velocity))
        arrnew.append(GridElement1d(arr[1].sigma, arr[1].velocity))

    else:
        arrnew.append(GridElement1d(arr[len(arr) - 1].sigma, arr[len(arr) - 1].velocity))
        arrnew.append(GridElement1d(arr[len(arr) - 2].sigma, arr[len(arr) - 2].velocity))

    return Grid1d(arrnew, len(arrnew))
    # And make a new grid from this.
