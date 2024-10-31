from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
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