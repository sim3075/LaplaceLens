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
        result = round(result, 4)

    return render_template('result.html', result=result, graph=graph)