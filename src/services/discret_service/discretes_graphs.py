import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from scipy.stats import binom, poisson


def plot_binomial_distribution(n, p, k, direction):
    x = np.arange(0, n + 1)
    y = binom.pmf(x, n, p)
    
    fig, ax = plt.subplots()
    ax.bar(x, y, label='Distribución Binomial', color='blue', alpha=0.7)
    
    ax.axvline(k, color='red', linestyle='--', label=f'Valor: {k}')
    
    if direction == 'equal':
        ax.bar(k, binom.pmf(k, n, p), color='orange', alpha=0.7, label=f'P(X = {k})')
    elif direction == 'less_than':
        ax.bar(x[x < k], y[x < k], color='orange', alpha=0.7, label=f'P(X < {k})')
    elif direction == 'greater_than':
        ax.bar(x[x > k], y[x > k], color='orange', alpha=0.7, label=f'P(X > {k})')
    
    ax.set_title('Distribución Binomial')
    ax.set_xlabel('Número de éxitos (X)')
    ax.set_ylabel('Probabilidad')
    ax.legend()
    ax.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    
    return base64.b64encode(buf.getvalue()).decode('utf8')

def plot_poisson_distribution(mu, k, direction):
    x = np.arange(0, np.ceil(mu) * 3)  
    y = poisson.pmf(x, mu)
    
    fig, ax = plt.subplots()
    ax.bar(x, y, label='Distribución Poisson', color='blue', alpha=0.7)
    
    ax.axvline(k, color='red', linestyle='--', label=f'Valor: {k}')
    
    if direction == 'equal':
        ax.bar(k, poisson.pmf(k, mu), color='orange', alpha=0.7, label=f'P(X = {k})')
    elif direction == 'less_than':
        ax.bar(x[x < k], y[x < k], color='orange', alpha=0.7, label=f'P(X < {k})')
    elif direction == 'greater_than':
        ax.bar(x[x > k], y[x > k], color='orange', alpha=0.7, label=f'P(X > {k})')
    
    ax.set_title('Distribución Poisson')
    ax.set_xlabel('Número de eventos (X)')
    ax.set_ylabel('Probabilidad')
    ax.legend()
    ax.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)

    return base64.b64encode(buf.getvalue()).decode('utf8')



