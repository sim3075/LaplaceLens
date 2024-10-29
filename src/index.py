from flask import Flask, render_template, request
from scipy.stats import norm, chi2, gamma, binom, poisson, t, f, expon
import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

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

def calculate_binomial(n, p, k):
    return binom.cdf(k, n, p)

def calculate_poisson(value, mu):
    return poisson.cdf(value, mu)

def calculate_t_student(value, df):
    return t.cdf(value, df)

def calculate_f_distribution(value, dfn, dfd):
    return f.cdf(value, dfn, dfd)

def calculate_exponential(value, scale):
    return expon.cdf(value, scale=scale)

#FUNCIONES PARQA GRAFICAS DE LAS FINCIONES 

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
    x = np.linspace(0, 30, 1000)  # Rango de x para la distribución
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




@app.route('/')
def index():
    continuous = ['Normal', 'Chi-cuadrado', 'Gamma', 'T-Student', 'F', 'Exponencial']
    discrete = ['Binomial', 'Poisson']
    return render_template('index.html', continuous=continuous, discrete=discrete)

@app.route('/normal')
def normal():
    return render_template('normal.html')

@app.route('/chi2')
def chi2_distribution():
    return render_template('chi2.html')

@app.route('/gamma')
def gamma_distribution():
    return render_template('gamma.html')

@app.route('/tstudent')
def t_student():
    return render_template('t_student.html')

@app.route('/f')
def f_distribution_view():
    return render_template('f_distribution.html')

@app.route('/exponential')
def exponential():
    return render_template('exponential.html')

@app.route('/binomial')
def binomial():
    return render_template('binomial.html')

@app.route('/poisson')
def poisson_distribution():
    return render_template('poisson.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    distribution = request.form.get('distribution')  
    value = float(request.form.get('value', 0)) 
    graph = None
    
    if distribution == 'normal':      
        direction = request.form.get('direction', 'less_than')
        mean = float(request.form['mean'])  
        stddev = float(request.form['stddev'])
        result = calculate_normal(value, direction, mean, stddev)
        graph = plot_normal_distribution(mean, stddev, value, direction)  

    elif distribution == 'chi2':
        direction = request.form.get('direction', 'less_than')
        df = float(request.form['df'])  
        direction = request.form.get('direction', 'less_than')
        result = calculate_chi2(value, direction, df)  
        graph = plot_chi2_distribution(df, value, direction)

    elif distribution == 'gamma':
        alpha = float(request.form['alpha'])
        beta = float(request.form['beta'])
        direction = request.form.get('direction', 'less_than')
        result = calculate_gamma(value, alpha, beta, direction)

    elif distribution == 'binomial':
        n = int(request.form['n'])
        p = float(request.form['p'])
        k = int(request.form['k'])
        result = calculate_binomial(n, p, k)
    elif distribution == 'poisson':
        mu = float(request.form['mu'])
        result = calculate_poisson(value, mu)
    elif distribution == 't_student':
        df = float(request.form['df'])
        result = calculate_t_student(value, df)
    elif distribution == 'f_distribution':
        dfn = float(request.form['dfn'])
        dfd = float(request.form['dfd'])
        result = calculate_f_distribution(value, dfn, dfd)
    elif distribution == 'exponential':
        scale = float(request.form['scale'])
        result = calculate_exponential(value, scale)
    else:
        result = 'Distribución invalida'
    
    return render_template('result.html', result=result, graph=graph)

if __name__ == '__main__':
    app.run(debug=True)
