from flask import Flask, render_template
from routes.continuous_distributions import continuous
from routes.discrete_distributions import discrete
from routes.hypothesis_test import hypothesis


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')
    
app.register_blueprint(continuous)
app.register_blueprint(discrete)
app.register_blueprint(hypothesis)
app.add_url_rule('/', endpoint='index')

if __name__ == '__main__':
    app.run(debug=False)