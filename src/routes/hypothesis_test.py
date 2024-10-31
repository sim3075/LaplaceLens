from flask import render_template, request, Blueprint
from scipy import stats

hypothesis = Blueprint('hypothesis', __name__, url_prefix='/hypothesis')

# Prueba de Chi-cuadrado
@hypothesis.route('/chi_cuadrado', methods=['GET', 'POST'])
def chi_square_test():
    result = None
    if request.method == 'POST':
        # Obtener los datos observados y esperados
        try:
            observed = list(map(int, request.form['observed'].split(',')))
            expected = list(map(int, request.form['expected'].split(',')))

            # Verificar que ambos arrays tengan la misma longitud
            if len(observed) != len(expected):
                raise ValueError("Los valores observados y esperados deben tener la misma longitud.")

            # Realizar la prueba de Chi-cuadrado
            chi2_stat, p_value = stats.chisquare(observed, expected)

            # Verificar si rechazamos la hipótesis nula
            result = {
                "chi2_stat": chi2_stat,
                "p_value": p_value,
                "reject_null": p_value < 0.05
            }

        except ValueError as ve:
            return render_template('chi_square_test.html', result={"error": str(ve)})
        except Exception as e:
            return render_template('chi_square_test.html', result={"error": "Ocurrió un error al procesar los datos."})

    return render_template('chi_square_test.html', result=result)
