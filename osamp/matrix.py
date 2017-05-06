import numpy as np


def get_seismic2d_matrix(_lambda, _mu, _rho):
    c_p = np.sqrt((_lambda + 2*_mu)/_rho)
    c_s = np.sqrt(_mu/_rho)
    seismic_matrix = np.diag(np.array([-c_p, c_s, c_p, c_s, 0]))
    return seismic_matrix

##TODO  create class
def get_acoustic2D_matrix():
    c1 = -np.sqrt(_k/_rho)
    c2 = np.sqrt(_k/_rho)
    acoustic_matrix = np.diag(np.array([с1,0,c2]))
    return acoustic_matrix

def get_acoustic2D_eign_matrix(_k, _rho, n):
    """ Retrun matrix of eigenvectors"""
    return np.array([[-np.sqrt(_k*_rho), 0, np.sqrt(_k*_rho)],[n[0], n[1], n[0]], [n[1], n[0], n[1]]])

def get_acoustic1D_matrix(_k, _rho):
    c1 = -np.sqrt(_k/_rho)
    c2 = np.sqrt(_k/_rho)
    acoustic_matrix = np.diag(np.array([с1,c2]))
    return acoustic_matrix

def get_acoustic1D_eign_matrix(_k, _rho, n):
    """ Retrun matrix of eigenvectors"""
    return np.array([[-np.sqrt(_k*_rho), np.sqrt(_k*_rho)],[n, n]])

def get_acoustic1D_inv_eign_matrix(_k, _rho, n):
    return np.array([-1/(2*np.sqrt(_k*_rho)),1/(2*n)], [1/(2*np.sqrt(_k*_rho)),1/(2*n)])
    pass

def get_matrix(dim, type, param):
    if type == 'acoustic':
        if dim == 1:
            return get_acoustic1D_matrix(param[0], param[1], param[2])
        else:
            return get_acoustic2D_matrix()

    if type == 'seismic'
        if dim == 1:
            return
        else:
            return get_seismic2d_matrix()


def get_eign_matrix(dim, type, param):
    if type == 'acoustic':
        if dim == 1:
            return get_acoustic1D_eign_matrix(param[0], param[1], param[2])
        else:
            return get_acoustic2D_eign_matrix()

    if type == 'seismic'
        if dim == 1:
            return
        else:
            return get_seismic2d_matrix()


def get_inv_eign_matrix(dim, type, param):
    if type == 'acoustic':
        if dim == 1:
            return get_acoustic1D_eign_matrix(param[0], param[1], param[2])
        else:
            return get_acoustic2D_eign_matrix()

    if type == 'seismic'
        if dim == 1:
            return
        else:
            return get_seismic2d_matrix()