import argparse


def parse_arg():
    """The function create parser to arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("path_to_problem",
        help="enter a path to file, that contained a task")
    parser.add_argument("--output", help="output path")
    return parser.parse_args()


def get_dict_from_arguments():
    """This function return a dictionary, that contains information about the problem"""
    pass
    #TODO : open user file and parse user data

def get_parametrs():
    arguments = parse_args()
    if arguments.path_to_problem is None:
        print("You forgot about path to your problem")
        exit()
    dict_of_parametrs = get_dict_from_arguments(arguments)
    return dict_of_parametrs