import re
import csv
import ssl
import json
from time import sleep
from flask import jsonify
from urllib.parse import urlparse, unquote, quote
from urllib.request import urlopen, Request, HTTPError, URLError

# SSL bypass
ssl._create_default_https_context = ssl._create_unverified_context
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

# {csv_file, test_url_index target_url_index}
# csv_file takes the csv file
# test_url_index takes the test urls column number
# target_url_index takes the target urls column number
def parse_urls(csv_file, test_url_index, target_url_index, base_url):
    csv_string = csv_file.stream.read().decode("utf-8").splitlines()
    test_url_index = int(test_url_index)
    target_url_index = int(target_url_index)
    base_url_clean = base_url if not base_url.endswith('/') else base_url[:-1]

    output = []
    csv_reader = csv.reader(csv_string, delimiter=',')

    for row in csv_reader:
        if len(row) >= (test_url_index + 1):
            # prepend breadcrumb with /
            test_prepended = row[test_url_index] if row[test_url_index].startswith('/') else '/' + row[test_url_index]
            target_prepended = row[target_url_index] if row[test_url_index].startswith('/') else '/' + row[target_url_index]
            # set urls
            test_url = row[test_url_index] if row[test_url_index].startswith('http') else '{}{}'.format(base_url_clean, test_prepended)
            target_url = row[target_url_index] if row[target_url_index].startswith('http') else '{}{}'.format(base_url_clean, target_prepended)

            output.append({'testurl':test_url, 'targeturl':target_url})

    return json.dumps(output)

# {test_url target_url}
# test_url takes the test url
# target_url takes the target url
def test_redirect(test_url, target_url):
    output = {}

    if len(urlparse(test_url).scheme) > 0:
        # swap url
        url = test_url
        # Set test url output
        output['url'] = url
        # Set target url output
        output['target'] = target_url

        # send request
        try:
            req = Request(url=url, headers=headers)
            open = urlopen(req)
            status = open.getcode()
            final = open.geturl()

            # Set status output
            output['status'] = status

            # Check if end url matches the target
            if urlparse(final).path in target_url:
                # Set matches output
                output['matches'] = True;
            else:
                # Set matches output
                output['matches'] = False;

        # catch 404s and whatever else
        except HTTPError as e:
            # Set status output
            output['status'] = e.code

        except URLError as e:
            # Set status output
            output['status'] = e.code

    return json.dumps(output)
