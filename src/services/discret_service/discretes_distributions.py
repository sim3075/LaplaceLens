import matplotlib
matplotlib.use('Agg')
from scipy.stats import binom, poisson


def calculate_binomial(n, p, k, direction):
    if direction == 'equal':
        return float(binom.pmf(k, n, p))
    
    elif direction == 'less_than':
        return float(binom.cdf(k - 1, n, p))

    elif direction == 'greater_than':
        return float(1 - binom.cdf(k - 1, n, p))

def calculate_poisson(value, mu, direction):
    if direction == 'equal':
        return poisson.pmf(value, mu)  
    elif direction == 'less_than':
        return poisson.cdf(value, mu)  
    elif direction == 'greater_than':
        return 1 - poisson.cdf(value - 1, mu)   
