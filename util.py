import numpy as np

def estimate_coef(x, y):
    n = np.size(x)
    if n == 0 or n == 1:
        return None
    m_x = np.mean(x)
    m_y = np.mean(y)
    cov = np.dot(x, y) - n * m_x * m_y
    var = np.var(x)
    if var == 0:
        return None
    else:
        return cov / var

