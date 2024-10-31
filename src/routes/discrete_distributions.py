from flask import (
    Blueprint, redirect, render_template, request, url_for
)

from services.discret_service.discretes_distributions import (
    calculate_binomial, calculate_poisson
    )

from services.discret_service.discretes_graphs import(
    plot_binomial_distribution, plot_poisson_distribution
)
discrete = Blueprint('discrete', __name__, url_prefix='/discrete')



@discrete.route('/binomial')
def binomial():
    return render_template('binomial.html')

@discrete.route('/poisson')
def poisson_distribution():
    return render_template('poisson.html')

@discrete.route('/calculate', methods=['POST'])
def calculate():
    distribution = request.form.get('distribution')  
    value = float(request.form.get('value', 0)) 
    graph = None
    result = None
    
    if distribution == 'binomial':
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
    else:
        result = 'Distribución invalida'
    
    return render_template('result.html', result=result, graph=graph)
