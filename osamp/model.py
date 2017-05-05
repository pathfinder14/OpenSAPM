class Model(list_of_user_data):
    """
    Model is a class, that contains information about formulation the problem
    The main data in model: matrix and property of class
    Model contain matrix of the acoustic/seismic equations
    
    """
    def __init__(self, arg):
        super(Model, self).__init__()
        self.arg = arg
        