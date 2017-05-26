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


def get_seismic2d_inv_eign_matrix(_lambda, _mu, density, n):
    c_s = np.sqrt((_lambda + 2*_mu)/density)
    c_p = np.sqrt(_mu/density)
    row_1 = [n[0]**2/(4*_mu + 2*_lambda + 8*_mu*n[0]**2*n[1]**2), n[1]**2/(4*_mu + 2*_lambda + 8*_mu*n[0]**2*n[1]**2), n[0]*n[1]/(2*_mu + _lambda + 4*_mu*n[0]**2*n[1]**2), n[0]/(2*c_p), n[1]/(2*c_p)]
    row_2 = [n[0]**2/(4*_mu + 2*_lambda + 8*_mu*n[0]**2*n[1]**2), n[1]**2/(4*_mu + 2*_lambda + 8*_mu*n[0]**2*n[1]**2), n[0]*n[1]/(2*_mu + _lambda + 4*_mu*n[0]**2*n[1]**2), -n[0]/(2*c_p), -n[1]/(2*c_p)]
    row_3 = [-n[0]*n[1]/(2*_mu + 4*_mu*n[0]**2*n[1]**2), n[0]*n[1]/(2*_mu + 4*_mu*n[0]**2*n[1]**2), (n[0]**2-n[1]**2)/(2*_mu + 4*_mu*n[0]**2*n[1]**2), -n[1]/(2*c_s), n[0]/(2*c_s)]
    row_4 = [-n[0]*n[1]/(2*_mu + 4*_mu*n[0]**2*n[1]**2), n[0]*n[1]/(2*_mu + 4*_mu*n[0]**2*n[1]**2), (n[0]**2-n[1]**2)/(2*_mu + 4*_mu*n[0]**2*n[1]**2), n[1]/(2*c_s), -n[0]/(2*c_s)]
    row_5 = [(-_lambda*(n[0]**2 - n[1]**2) + 2*_mu*n[1]**2)/(2*_mu + _lambda + 6*_mu*n[0]**2*n[1]**2 + 2*_lambda*n[0]**2*n[1]**2), (-_lambda*(n[0]**2 - n[1]**2) + 2*_mu*n[0]**2)/(2*_mu + _lambda + 6*_mu*n[0]**2*n[1]**2 + 2*_lambda*n[0]**2*n[1]**2), (-4*_mu*n[0]*n[1])/(2*_mu + _lambda + 6*_mu*n[0]**2*n[1]**2 + 2*_lambda*n[0]**2*n[1]**2), 0, 0]
    return np.array([row_1, row_2, row_3, row_4, row_5])

def get_seismic2d_eign_matrix(_lambda, _mu, density, n):
    c_s = np.sqrt((_lambda + 2*_mu)/density)
    c_p = np.sqrt(_mu/density)
    row_1 = [_lambda + 2*_mu*n[0]**2, _lambda + 2*_mu*n[0]**2, -2*n[0]*n[1]*_mu, -2*n[0]*n[1]*_mu, n[1]**2]
    row_2 = [_lambda + 2*_mu*n[1]**2, _lambda + 2*_mu*n[1]**2, 2*n[0]*n[1]*_mu, 2*n[0]*n[1]*_mu, n[0]**2]
    row_3 = [2*n[0]*n[1]*_mu, 2*n[0]*n[1]*_mu, (n[0]**2 - n[1]**2)*_mu, (n[0]**2 - n[1]**2)*_mu, -n[0]*n[1]]
    row_4 = [n[0]*c_p, -n[0]*c_p, -n[1]*c_s, n[1]*c_s, 0]
    row_5 = [n[1]*c_p, -n[1]*c_p, n[0]*c_s, -n[0]*c_s, 0]
    return np.array([row_1, row_2, row_3, row_4, row_5])

def get_acoustic2D_matrix(_k, density):
    c1 = -np.sqrt(_k / density)
    c2 = np.sqrt(_k / density)
    return np.diag(np.array([c1, 0, c2]))

def get_acoustic2D_eign_matrix(_k, density, n):
    """ Return matrix of eigenvectors"""
    return np.array([[-np.sqrt(_k*density), 0, np.sqrt(_k*density)], [n[0], n[1], n[0]], [n[1], n[0], n[1]]])

def get_acoustic2D_inv_eign_matrix(_k, density, n):
    N = n[0]^2 - n[1]^2
    return np.array([[-1/(2*np.sqrt(_k*density)), n[0]/(2*N), -n[1]/(2*N)],[0, -n[1]/(2*N), n[0]/(2*N)], [-1/(2*np.sqrt(_k*density)), n[0]/(2*N), -n[1]/(2*N)]])

def get_acoustic1D_matrix(_k, density):
    c1 = -np.sqrt(_k / density)
    c2 = np.sqrt(_k / density)
    acoustic_matrix = np.diag(np.array([c1,c2]))
    return acoustic_matrix

def get_acoustic1D_eign_matrix(_k, density, n):
    """ Return matrix of eigenvectors"""
    return np.array([[-np.sqrt(_k * density), np.sqrt(_k * density)], [n, n]])

def get_acoustic1D_inv_eign_matrix(_k, density, n):
    return np.array([[-1 / (2 * np.sqrt(_k * density)), 1/(2 * n)], [1 / (2 * np.sqrt(_k * density)), 1/(2 * n)]])

def get_matrix(dim, type, environment_properties, x=15, y=15):
    if type == 'acoustic':
        if dim == 1:
            return get_acoustic1D_matrix(environment_properties.elasticity_quotient, environment_properties.density)
        else:
            return get_acoustic2D_matrix(environment_properties.elasticity_quotient, environment_properties.density)
    if type == 'seismic':
        if dim == 1:
            return get_seismic1d_matrix(environment_properties.mu_lame, environment_properties.density)
        else:
            return get_seismic2d_matrix(environment_properties.lambda_lame, environment_properties.mu_lame, environment_properties.density)

def get_eign_matrix(dim, type, environment_properties, x=15, y=15):
    if type == 'acoustic':
        if dim == 1:
            # TODO: clarify what value should be passed as the third parameter
            return get_acoustic1D_eign_matrix(environment_properties.elasticity_quotient, environment_properties.density,  1)
        else:
            return get_acoustic2D_eign_matrix(environment_properties.elasticity_quotient, environment_properties.density, [1, 1, 1])

    if type == 'seismic':
        if dim == 1:
            return get_seismic1d_eign_matrix(environment_properties.mu_lame, environment_properties.density)
        else:
            # TODO: implement method get_seismic2d_eign_matrix and replace the following with it
            return get_seismic2d_eign_matrix(environment_properties.lambda_lame, environment_properties.mu_lame, environment_properties.density, [1, 1])


def get_inv_eign_matrix(dim, type, environment_properties, x=15, y=15):
    if type == 'acoustic':
        if dim == 1:
            return get_acoustic1D_inv_eign_matrix(environment_properties.elasticity_quotient, environment_properties.density, 1)
        else:
            return get_acoustic2D_inv_eign_matrix(environment_properties.elasticity_quotient, environment_properties.density, [1, 1, 1])

    if type == 'seismic':
        if dim == 1:
            return get_seismic1d_inv_eign_matrix(environment_properties.mu_lame, environment_properties.density)
        else:
            # TODO: implement method get_seismic2d_inv_eign_matrix and replace the following with it
            return get_seismic2d_inv_eign_matrix(environment_properties.lambda_lame, environment_properties.mu_lame, environment_properties.density, [1, 1])


def calculate_params_for_acoustic():
    pass