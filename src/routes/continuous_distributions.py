from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from services.continuous_service.continuous_distributions import (
    calculate_normal, calculate_chi2, calculate_normal, calculate_gamma, calculate_t_student, calculate_f_distribution, calculate_exponential
    )

from services.continuous_service.continuous_graphs import(
    plot_chi2_distribution, plot_exponential_distribution, plot_f_distribution, plot_gamma_distribution,  plot_normal_distribution, plot_t_student_distribution
)
continuous = Blueprint('continuous', __name__, url_prefix='/continuous')

@continuous.route('/normal')
def normal():
    return render_template('normal.html')

@continuous.route('/chi2')
def chi2_distribution():
    return render_template('chi2.html')

@continuous.route('/gamma')
def gamma_distribution():
    return render_template('gamma.html')

@continuous.route('/tstudent')
def t_student():
    return render_template('tstudent.html')

@continuous.route('/f')
def f_distribution_view():
    return render_template('f.html')

@continuous.route('/exponential')
def exponential():
    return render_template('exponential.html')

@continuous.route('/calculate', methods=['POST'])
def calculate():
    distribution = request.form.get('distribution')  
    value = float(request.form.get('value', 0)) 
    graph = None
    result = None
    params = {}  # Diccionario para almacenar la media, varianza y desviación estándar

    if distribution == 'normal':      
        direction = request.form.get('direction', 'less_than')
        mean = float(request.form['mean'])  
        stddev = float(request.form['stddev'])
        result = calculate_normal(value, direction, mean, stddev)
        graph = plot_normal_distribution(mean, stddev, value, direction)
        
        # Parámetros específicos de la distribución normal
        variance = stddev ** 2
        params = {'mean': mean, 'variance': variance, 'stddev': stddev}

    elif distribution == 'chi2':
        direction = request.form.get('direction', 'less_than')
        df = float(request.form['df'])  
        result = calculate_chi2(value, direction, df)  
        graph = plot_chi2_distribution(df, value, direction)
        
        # Parámetros de la distribución chi-cuadrado
        mean = df
        variance = 2 * df
        stddev = (2 * df) ** 0.5
        params = {'mean': mean, 'variance': variance, 'stddev': stddev}

    elif distribution == 'gamma':
        alpha = float(request.form['alpha'])
        beta = float(request.form['beta'])
        direction = request.form.get('direction', 'less_than')
        result = calculate_gamma(value, alpha, beta, direction)
        graph = plot_gamma_distribution(alpha, beta, value, direction)
        
        # Parámetros de la distribución gamma
        mean = alpha * beta
        variance = alpha * (beta ** 2)
        stddev = (variance) ** 0.5
        params = {'mean': mean, 'variance': variance, 'stddev': stddev}

    elif distribution == 't_student':
        df = float(request.form['df'])
        direction = request.form.get('direction', 'less_than')
        result = calculate_t_student(value, df, direction)
        graph = plot_t_student_distribution(df, value, direction)
        
        # Parámetros de la distribución t de Student
        mean = 0 if df > 1 else None  # La media solo existe si df > 1
        variance = df / (df - 2) if df > 2 else None  # La varianza solo existe si df > 2
        stddev = (variance) ** 0.5 if variance is not None else None
        params = {'mean': mean, 'variance': variance, 'stddev': stddev}

    elif distribution == 'f_distribution':
        dfn = float(request.form['dfn'])
        dfd = float(request.form['dfd'])
        direction = request.form.get('direction', 'less_than')
        result = calculate_f_distribution(value, dfn, dfd, direction)
        graph = plot_f_distribution(dfn, dfd, value, direction)
        
        # Parámetros de la distribución F
        mean = dfd / (dfd - 2) if dfd > 2 else None
        variance = (2 * (dfd ** 2) * (dfn + dfd - 2)) / (dfn * (dfd - 2) ** 2 * (dfd - 4)) if dfd > 4 else None
        stddev = (variance) ** 0.5 if variance is not None else None
        params = {'mean': mean, 'variance': variance, 'stddev': stddev}

    elif distribution == 'exponential_distribution':
        scale = float(request.form['scale'])
        direction = request.form.get('direction', 'less_than')
        result = calculate_exponential(value, scale, direction)
        graph = plot_exponential_distribution(scale, value, direction)
        
        # Parámetros de la distribución exponencial
        mean = scale
        variance = scale ** 2
        stddev = scale
        params = {'mean': mean, 'variance': variance, 'stddev': stddev}

    else:
        result = 'Distribución invalida'


    return render_template('result.html', result=result, graph=graph, params=params)
