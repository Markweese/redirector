import flask
from flask import request, render_template
from .redirect_functions import test_redirect, parse_urls

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return render_template("form.html")

@app.route('/api/v1/redirect-test', methods=['POST'])
def api_filter():
    csv_file = request.files['file']
    test_url_index = request.form['testurl']
    target_url_index = request.form['targeturl']
    parsed_urls = parse_urls(csv_file, test_url_index, target_url_index)

    return render_template("dashboard.html", urls=parsed_urls)

if __name__ == '__main__':
    app.run()
