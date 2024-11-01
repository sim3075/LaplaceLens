import matplotlib
matplotlib.use('Agg')
from scipy.stats import binom, poisson

def calculate_binomial(n, p, k, direction):
    if direction == 'equal':
        result= float(binom.pmf(k, n, p))
    
    elif direction == 'less_than':
        result= float(binom.cdf(k - 1, n, p))

    elif direction == 'greater_than':
        result= float(1 - binom.cdf(k - 1, n, p))

    if abs(result) < 1e-6:
        result = 0
    else:
        result = round(result, 6)
    return result

def calculate_poisson(value, mu, direction):
    if direction == 'equal':
        result= poisson.pmf(value, mu)  
    elif direction == 'less_than':
        result= poisson.cdf(value, mu)  
    elif direction == 'greater_than':
        result= 1 - poisson.cdf(value - 1, mu)   
    
    if abs(result) < 1e-6:
        result = 0
    else:
        result = round(result, 6)
    return result
