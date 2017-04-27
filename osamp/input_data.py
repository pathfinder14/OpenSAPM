import argparse


def parse_args():
    """The function create parser to arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("path_to_problem",
        help="enter a path to file, that contained a task")
    parser.add_argument("--output", help="output path")
    return parser.parse_args()


def get_dict_from_arguments(arguments):
    """This function returns a dictionary, that contains information about the problem"""
    with open(arguments.path_to_problem) as infile:
        parametrs = {}
        for line in infile:
            tmp = line.split()
            parametrs[tmp[0]] = tmp[1]
    return parametrs


def get_parametrs():
    arguments = parse_args()
    if arguments.path_to_problem is None:
        print("You forgot about path to your problem")
        exit()
    dict_of_parametrs = get_dict_from_arguments(arguments)
    return dict_of_parametrs