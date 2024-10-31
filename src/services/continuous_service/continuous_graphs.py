import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from scipy.stats import norm, chi2, gamma, t, f, expon




def plot_normal_distribution(mean, stddev, value, direction):
    x = np.linspace(mean - 4 * stddev, mean + 4 * stddev, 1000)
    y = norm.pdf(x, mean, stddev)

    fig, ax = plt.subplots()
    ax.plot(x, y, label='Distribución Normal', color='blue')
    ax.axvline(value, color='red', linestyle='--', label=f'Valor: {value}')

    if direction == 'less_than':
        x_fill = np.linspace(mean - 4 * stddev, value, 1000)
        y_fill = norm.pdf(x_fill, mean, stddev)
        ax.fill_between(x_fill, y_fill, alpha=0.5, color='orange', label='P(X < x)')
    elif direction == 'greater_than':
        x_fill = np.linspace(value, mean + 4 * stddev, 1000)
        y_fill = norm.pdf(x_fill, mean, stddev)
        ax.fill_between(x_fill, y_fill, alpha=0.5, color='orange', label='P(X > x)')

    ax.set_title('Distribución Normal')
    ax.set_xlabel('X')
    ax.set_ylabel('Densidad de Probabilidad')
    ax.legend()
    ax.grid()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf8')

def plot_chi2_distribution(df, value, direction):
    x = np.linspace(0, 30, 1000)  
    y = chi2.pdf(x, df)

    fig, ax = plt.subplots()
    ax.plot(x, y, label='Distribución Chi-Cuadrado', color='blue')
    ax.axvline(value, color='red', linestyle='--', label=f'Valor: {value}')

    if direction == 'less_than':
        x_fill = np.linspace(0, value, 1000)
        y_fill = chi2.pdf(x_fill, df)
        ax.fill_between(x_fill, y_fill, alpha=0.5, color='orange', label='P(X < x)')
    elif direction == 'greater_than':
        x_fill = np.linspace(value, 30, 1000)  
        y_fill = chi2.pdf(x_fill, df)
        ax.fill_between(x_fill, y_fill, alpha=0.5, color='orange', label='P(X > x)')

    ax.set_title('Distribución Chi-Cuadrado')
    ax.set_xlabel('X')
    ax.set_ylabel('Densidad de Probabilidad')
    ax.legend()
    ax.grid()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf8')

def plot_gamma_distribution(alpha, beta, value, direction):
    x = np.linspace(0, 30, 1000)  
    scale = 1 / beta
    y = gamma.pdf(x, alpha, scale=scale)

    fig, ax = plt.subplots()
    ax.plot(x, y, label='Distribución Gamma', color='blue')
    ax.axvline(value, color='red', linestyle='--', label=f'Valor: {value}')

    if direction == 'less_than':
        x_fill = np.linspace(0, value, 1000)
        y_fill = gamma.pdf(x_fill, alpha, scale=scale)
        ax.fill_between(x_fill, y_fill, alpha=0.5, color='orange', label='P(X < x)')
    elif direction == 'greater_than':
        x_fill = np.linspace(value, 30, 1000)
        y_fill = gamma.pdf(x_fill, alpha, scale=scale)
        ax.fill_between(x_fill, y_fill, alpha=0.5, color='orange', label='P(X > x)')

    ax.set_title('Distribución Gamma')
    ax.set_xlabel('X')
    ax.set_ylabel('Densidad de Probabilidad')
    ax.legend()
    ax.grid()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf8')

def plot_t_student_distribution(df, value, direction):
    x = np.linspace(-5, 5, 1000)  
    y = t.pdf(x, df)

    fig, ax = plt.subplots()
    ax.plot(x, y, label='Distribución T-Student', color='blue')
    ax.axvline(value, color='red', linestyle='--', label=f'Valor: {value}')

    if direction == 'less_than':
        x_fill = np.linspace(-5, value, 1000)
        y_fill = t.pdf(x_fill, df)
        ax.fill_between(x_fill, y_fill, alpha=0.5, color='orange', label='P(X < x)')
    elif direction == 'greater_than':
        x_fill = np.linspace(value, 5, 1000)
        y_fill = t.pdf(x_fill, df)
        ax.fill_between(x_fill, y_fill, alpha=0.5, color='orange', label='P(X > x)')

    ax.set_title('Distribución T-Student')
    ax.set_xlabel('X')
    ax.set_ylabel('Densidad de Probabilidad')
    ax.legend()
    ax.grid()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf8')

def plot_f_distribution(dfn, dfd, value, direction):
    x = np.linspace(0, 5, 1000)  
    y = f.pdf(x, dfn, dfd)

    fig, ax = plt.subplots()
    ax.plot(x, y, label='Distribución F', color='blue')
    ax.axvline(value, color='red', linestyle='--', label=f'Valor: {value}')

    if direction == 'less_than':
        x_fill = np.linspace(0, value, 1000)
        y_fill = f.pdf(x_fill, dfn, dfd)
        ax.fill_between(x_fill, y_fill, alpha=0.5, color='orange', label='P(X < x)')
    elif direction == 'greater_than':
        x_fill = np.linspace(value, 5, 1000)
        y_fill = f.pdf(x_fill, dfn, dfd)
        ax.fill_between(x_fill, y_fill, alpha=0.5, color='orange', label='P(X > x)')
    elif direction == 'equal':
        ax.bar(value, f.pdf(value, dfn, dfd), color='orange', alpha=0.7, label=f'P(X = {value})')
    
    ax.set_title('Distribución F')
    ax.set_xlabel('X')
    ax.set_ylabel('Densidad de Probabilidad')
    ax.legend()
    ax.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    
    return base64.b64encode(buf.getvalue()).decode('utf8')

def plot_exponential_distribution(scale, value, direction):
    x = np.linspace(0, 10, 1000) 
    y = expon.pdf(x, scale=scale)

    fig, ax = plt.subplots()
    ax.plot(x, y, label='Distribución Exponencial', color='blue')
    ax.axvline(value, color='red', linestyle='--', label=f'Valor: {value}')

    if direction == 'less_than':
        x_fill = np.linspace(0, value, 1000)
        y_fill = expon.pdf(x_fill, scale=scale)
        ax.fill_between(x_fill, y_fill, alpha=0.5, color='orange', label='P(X < x)')
    elif direction == 'greater_than':
        x_fill = np.linspace(value, 10, 1000)
        y_fill = expon.pdf(x_fill, scale=scale)
        ax.fill_between(x_fill, y_fill, alpha=0.5, color='orange', label='P(X > x)')
    elif direction == 'equal':
        ax.bar(value, expon.pdf(value, scale=scale), color='orange', alpha=0.7, label=f'P(X = {value})')
    
    ax.set_title('Distribución Exponencial')
    ax.set_xlabel('X')
    ax.set_ylabel('Densidad de Probabilidad')
    ax.legend()
    ax.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    
    return base64.b64encode(buf.getvalue()).decode('utf8')
