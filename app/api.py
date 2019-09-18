import flask
from flask import request, render_template
from .redirect_functions import test_redirects

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return render_template("dashboard.html")

@app.route('/api/v1/redirect-test', methods=['POST'])
def api_filter():
    base64_csv = request.files['file']
    test_url_index = request.form['testurl']
    target_url_index = request.form['targeturl']

    return test_redirects(base64_csv, test_url_index, target_url_index)

if __name__ == '__main__':
    app.run()
