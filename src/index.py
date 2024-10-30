import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from scipy.stats import norm, chi2, gamma, binom, poisson, t, f, expon
from flask import Flask, render_template, request

app = Flask(__name__)

#funciones

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


#graficas

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




@app.route('/')
def index():
    return render_template('index.html')

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
    return render_template('tstudent.html')

@app.route('/f')
def f_distribution_view():
    return render_template('f.html')

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
    result = None
    
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
        graph = plot_gamma_distribution(alpha, beta, value, direction)

    elif distribution == 'binomial':
        n = int(request.form['n'])
        p = float(request.form['p'])
        k = int(request.form['k'])
        direction = request.form.get('direction', 'less_than')  
        result =calculate_binomial(n, p, k, direction)
        graph = plot_binomial_distribution(n, p, k, direction) 

    elif distribution == 'poisson':
        mu = float(request.form['mu'])
        k = int(request.form['k'])
        direction = request.form.get('direction')  
        result = calculate_poisson(mu, k, direction)
        graph = plot_poisson_distribution(mu, k, direction)

    elif distribution == 't_student':
        df = float(request.form['df'])
        direction = request.form.get('direction', 'less_than')
        result = calculate_t_student(value, df, direction)
        graph =plot_t_student_distribution(df, value, direction)


    elif distribution == 'f_distribution':
        dfn = float(request.form['dfn'])
        dfd = float(request.form['dfd'])
        direction = request.form.get('direction', 'less_than')
        result = calculate_f_distribution(value, dfn, dfd, direction)
        graph = plot_f_distribution(dfn, dfd, value, direction)

    elif distribution == 'exponential_distribution':
        scale = float(request.form['scale'])
        direction = request.form.get('direction', 'less_than')
        result = calculate_exponential(value, scale, direction)
        graph = plot_exponential_distribution(scale, value, direction)
    else:
        result = 'Distribución invalida'
    
    return render_template('result.html', result=result, graph=graph)

if __name__ == '__main__':
    app.run(debug=True)