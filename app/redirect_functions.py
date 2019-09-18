import csv
import ssl
import json
from time import sleep
from flask import jsonify
from urllib.parse import urlparse, unquote
from urllib.request import urlopen, Request, HTTPError, URLError

# SSL bypass
ssl._create_default_https_context = ssl._create_unverified_context
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

# {csv_file, test_url_index target_url_index}
# csv_file takes the csv file
# test_url_index takes the test urls column number
# target_url_index takes the target urls column number
def parse_urls(csv_file, test_url_index, target_url_index):
    csv_string = csv_file.stream.read().decode("utf-8").splitlines()
    test_url_index = int(test_url_index)
    target_url_index = int(target_url_index)

    output = []
    csv_reader = csv.reader(csv_string, delimiter=',')

    for row in csv_reader:
        if len(row) > 0:
            if len(urlparse(row[test_url_index]).scheme) > 0:
                # swap url
                output.append({'testurl':row[test_url_index], 'targeturl':row[target_url_index]})

    return json.dumps(output)

# {test_url target_url}
# test_url takes the test url
# target_url takes the target url
def test_redirect(test_url, target_url):
    output = {}

    if len(urlparse(test_url).scheme) > 0:
        # swap url
        url = test_url

        # send request
        try:
            req = Request(url=url, headers=headers)
            open = urlopen(req)
            status = open.getcode()
            final = open.geturl()

            # check if end url matches the target
            if final.split('.com')[1] == target_url.split('.com')[1]:
                correct_redirect = True;
            else:
                correct_redirect = False;

        # catch 404s and whatever else
        except HTTPError as e:
            output['url'] = url
            output['status'] = e.code
            output['matches'] = correct_redirect

        except URLError as e:
            output['url'] = url
            output['status'] = e.code
            output['matches'] = correct_redirect

    return jsonify(output)
