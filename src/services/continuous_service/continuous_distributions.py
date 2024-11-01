import matplotlib
matplotlib.use('Agg')
from scipy.stats import norm, chi2, gamma,t, f, expon


from scipy.stats import norm

def calculate_normal(value, direction, mean, stddev):
    z = (value - mean) / stddev  

    if direction == 'less_than':
        result = norm.cdf(z)
    elif direction == 'greater_than':
        result = 1 - norm.cdf(z)
    
    if abs(result) < 1e-6:
        result = 0.0
    else:
        result = round(result, 6)
    
    return result
    
def calculate_chi2(value, direction, df):
    if direction == 'less_than':
        result = chi2.cdf(value, df)  
    elif direction == 'greater_than':
        result = 1 - chi2.cdf(value, df) 

    if abs(result) < 1e-6:
        result = 0
    else:
        result = round(result, 6)
    return result
    
def calculate_gamma(value, alpha, beta, direction):
    scale = 1 / beta
    gamma_dist = gamma(alpha, scale=scale)
    if direction == 'less_than':
        result = gamma_dist.cdf(value)
    elif direction == 'greater_than':
        result = 1 - gamma_dist.cdf(value)
    
    if abs(result) < 1e-6:
        result = 0
    else:
        result = round(result, 6)
    return result
    
def calculate_t_student(value, df, direction):
    if direction == 'equal':
        result= t.pdf(value, df)  
    elif direction == 'less_than':
        result= t.cdf(value, df)  
    elif direction == 'greater_than':
        result= 1 - t.cdf(value, df) 

    if abs(result) < 1e-6:
        result = 0
    else:
        result = round(result, 6)
    return result 

def calculate_f_distribution(value, dfn, dfd, direction):
    if direction == 'less_than':
        result= f.cdf(value, dfn, dfd)   
    elif direction == 'greater_than':
        result= 1 - f.cdf(value, dfn, dfd) 
    
    if abs(result) < 1e-6:
        result = 0
    else:
        result = round(result, 6)
    return result

def calculate_exponential(value, scale, direction):
    if direction == 'less_than':
        result= expon.cdf(value, scale=1/scale) 
    elif direction == 'greater_than':
        result= 1 - expon.cdf(value, scale=1/scale)
    result = round(result, 5)
    
    if abs(result) < 1e-6:
        result = 0
    else:
        result = round(result, 6)
    return result 

