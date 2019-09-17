import flask
from flask import request
# from .redirect_functions import test_redirects

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/api/v1/redirect-test', methods=['GET'])
def api_filter():
    params = request.args

    base64_csv = params['csv']
    test_url_index = params['testurl']
    target_url_index = params['targeturl']

    return "test_redirects(base64_csv, test_url_index, target_url_index)"

if __name__ == '__main__':
    app.run()
