"""
A sample Hello World server.
"""
import os
from flask import request, make_response
# import redis
import urllib.request

from flask import Flask, render_template

# pylint: disable=C0103
app = Flask(__name__)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    pageTitle = "Ean's Janky Cloud Run Test App"

    address = "https://us-west2-www-eanh-net.cloudfunctions.net/gcf-connector"
    gcfMessage = urllib.request.urlopen(address).read().decode('utf-8')

    queryStringMessage = request.args.get('x')
    resp = make_response(render_template('index.html',
                                         PageTitle=pageTitle,
                                         QueryStringMessage=queryStringMessage,
                                         GCFMessage=gcfMessage))

    if queryStringMessage:
        resp.set_cookie('testcookie', queryStringMessage)
    return resp


if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')
