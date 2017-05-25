import numpy as np

def get_seismic1d_matrix(mu, density):
    c_p = np.sqrt(mu / density)
    return np.diag(np.array([c_p, -c_p]))

def get_seismic1d_eign_matrix(mu, density):#TODO!!
    """ Retrun matrix of eigenvectors"""
    c_p = np.sqrt(mu/density)
    return np.array([[1/c_p, 1/c_p], [1, 1]])

def get_seismic1d_inv_eign_matrix(_mu, density):
    c_p = np.sqrt(_mu/density)

    return np.array([[-0.5*c_p, 0.5], [-0.5*c_p, 0.5]])

def get_seismic2d_matrix(_lambda, _mu, density):
    c_p = np.sqrt((_lambda + 2*_mu)/density)
    c_s = np.sqrt(_mu/density)
    return np.diag(np.array([-c_p, c_s, c_p, c_s, 0]))

def get_seismic2d_inv_eign_matrix(_lambda, mu_lame, density):
    c_p = np.sqrt((_lambda + 2*mu_lame)/density)
    c_s = np.sqrt(mu_lame/density)
    return np.diag(np.array([-c_p, c_s, c_p, c_s, 0]))

def get_seismic2d_eign_matrix(_lambda, mu_lame, density):
    c_p = np.sqrt((_lambda + 2*mu_lame)/density)
    c_s = np.sqrt(mu_lame/density)
    return np.diag(np.array([-c_p, c_s, c_p, c_s, 0]))

def get_acoustic2D_matrix(_k, density):
    c1 = -np.sqrt(_k / density)
    c2 = np.sqrt(_k / density)
    return np.diag(np.array([c1, 0, c2]))

def get_acoustic2D_eign_matrix(_k, density, n):
    """ Retrun matrix of eigenvectors"""
    return np.array([[-np.sqrt(_k*density), 0, np.sqrt(_k*density)],[n[0], n[1], n[0]], [n[1], n[0], n[1]]])

def get_acoustic2D_inv_eign_matrix(_k, density, n):
    N = n[0]^2 - n[1]^2
    return np.array([[-1/(2*np.sqrt(_k*density)), n[0]/(2*N), -n[1]/(2*N)],[0, -n[1]/(2*N), n[0]/(2*N)], [-1/(2*np.sqrt(_k*density)), n[0]/(2*N), -n[1]/(2*N)]])

def get_acoustic1D_matrix(_k, density):
    c1 = -np.sqrt(_k / density)
    c2 = np.sqrt(_k / density)
    acoustic_matrix = np.diag(np.array([c1,c2]))
    return acoustic_matrix

def get_acoustic1D_eign_matrix(_k, density, n):
    """ Retrun matrix of eigenvectors"""
    return np.array([[-np.sqrt(_k * density), np.sqrt(_k * density)], [n, n]])

def get_acoustic1D_inv_eign_matrix(_k, density, n):
    return np.array([[-1 / (2 * np.sqrt(_k * density)), 1/(2 * n)], [1 / (2 * np.sqrt(_k * density)), 1/(2 * n)]])

def get_matrix(dim, type, elasticity_quotient, density, mu_lame):
    if type == 'acoustic':
        if dim == 1:
            return get_acoustic1D_matrix(elasticity_quotient, density)
        else:
            return get_acoustic2D_matrix(elasticity_quotient, density)
    if type == 'seismic':
        if dim == 1:
            return get_seismic1d_matrix(mu_lame, density)
        else:
            return get_seismic2d_matrix(elasticity_quotient, mu_lame, density)

def get_eign_matrix(dim, type, elasticity_quotient, density, mu_lame):
    if type == 'acoustic':
        if dim == 1:
            # TODO: clarify what value should be passed as the third parameter
            return get_acoustic1D_eign_matrix(elasticity_quotient, density, 1)
        else:
            return get_acoustic2D_eign_matrix(elasticity_quotient, density, [1, 1, 1])

    if type == 'seismic':
        if dim == 1:
            return get_seismic1d_eign_matrix(mu_lame, density)
        else:
            # TODO: implement method get_seismic2d_eign_matrix and replace the following with it
            return get_seismic2d_eign_matrix(elasticity_quotient, mu_lame, density)


def get_inv_eign_matrix(dim, type, elasticity_quotient, density, mu_lame):
    if type == 'acoustic':
        if dim == 1:
            return get_acoustic1D_inv_eign_matrix(elasticity_quotient, density, 1)
        else:
            return get_acoustic2D_inv_eign_matrix(elasticity_quotient, density, [1, 1, 1])

    if type == 'seismic':
        if dim == 1:
            return get_seismic1d_inv_eign_matrix(mu_lame, density)
        else:
            # TODO: implement method get_seismic2d_inv_eign_matrix and replace the following with it
            return get_seismic2d_inv_eign_matrix(elasticity_quotient, mu_lame, density)