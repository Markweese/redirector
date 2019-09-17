import csv
import base64
from time import sleep
from flask import jsonify
from urllib.parse import urlparse, unquote
from urllib.request import urlopen, Request, HTTPError, URLError

# {base64_csv, test_url_index target_url_index}
# base64_csv takes the url encoded base64 csv string
# test_url_index takes the test urls column number
# target_url_index takes the target urls column number
def test_redirects(base64_csv, test_url_index, target_url_index):
    csv_string = unquote(base64_csv)
    test_url_index = int(test_url_index)
    target_url_index = int(target_url_index)

    output = []
    base64_parsed = base64.b64decode(csv_string).decode('unicode_escape').splitlines()
    csv_reader = csv.reader(base64_parsed, delimiter=',')

    for row in csv_reader:
        if len(row) > 0:
            if len(urlparse(row[test_url_index]).scheme) > 0:
                # swap url
                url = row[test_url_index]

                # send request
                try:
                    req = Request(url=url, headers=headers)
                    open = urlopen(req)
                    status = open.getcode()
                    final = open.geturl()

                    # check if end url matches the target
                    if final.split('.com')[1] == row[target_url_index].split('.com')[1]:
                        correct_redirect = True;
                    else:
                        correct_redirect = False;

                # catch 404s and whatever else
                except HTTPError as e:
                    output.append({'url': url, 'status': e.code, 'matches': correct_redirect})
                    continue
                except URLError as e:
                    output.append({'url': url, 'status': e.code, 'matches': correct_redirect})
                    continue

                # output
                output.append({'url': url, 'status': status, 'matches': correct_redirect})

    return jsonify(output)
