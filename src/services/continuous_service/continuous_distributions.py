import matplotlib
matplotlib.use('Agg')
from scipy.stats import norm, chi2, gamma,t, f, expon


def calculate_normal(value, direction, mean, stddev):
    z = (value - mean) / stddev  

    if direction == 'less_than':
        return norm.cdf(z)  
    elif direction == 'greater_than':
        return 1 - norm.cdf(z) 
    
def calculate_chi2(value, direction, df):
    if direction == 'less_than':
        return chi2.cdf(value, df)  
    elif direction == 'greater_than':
        return 1 - chi2.cdf(value, df) 
    
def calculate_gamma(value, alpha, beta, direction):
    scale = 1 / beta
    gamma_dist = gamma(alpha, scale=scale)
    if direction == 'less_than':
        return gamma_dist.cdf(value)
    elif direction == 'greater_than':
        return 1 - gamma_dist.cdf(value)
    
def calculate_t_student(value, df, direction):
    if direction == 'equal':
        return t.pdf(value, df)  
    elif direction == 'less_than':
        return t.cdf(value, df)  
    elif direction == 'greater_than':
        return 1 - t.cdf(value, df)  

def calculate_f_distribution(value, dfn, dfd, direction):
    if direction == 'less_than':
        return f.cdf(value, dfn, dfd)   
    elif direction == 'greater_than':
        return 1 - f.cdf(value, dfn, dfd) 

def calculate_exponential(value, scale, direction):
    if direction == 'less_than':
        return expon.cdf(value, scale=1/scale) 
    elif direction == 'greater_than':
        return 1 - expon.cdf(value, scale=1/scale)  

