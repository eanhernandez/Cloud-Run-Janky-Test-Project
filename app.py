"""
A sample Hello World server.
"""
import os
import sys
# import redis
import urllib.request


from flask import Flask, render_template
from flask import request, make_response

#from google.cloud import storage

# pylint: disable=C0103
app = Flask(__name__)


@app.route('/')
def hello():

    timeout=5

    pageTitle = "Ean's Janky Cloud Run Test App"

    gcfaddress = "https://us-west2-saturday-307518.cloudfunctions.net/WhatIsYourFavoriteBand-1"
    gcfMessage = urllib.request.urlopen(gcfaddress,timeout=timeout).read().decode('utf-8')
    gceaddress = "http://10.154.0.2:8080/faveband.html"
    try:
        VpcMessage = urllib.request.urlopen(gceaddress,timeout=timeout).read().decode('utf-8')
    except:
        e = sys.exc_info()[0]
        VpcMessage = str(e)


    queryStringMessage = request.args.get('x')
    resp = make_response(render_template('index.html',
                                         PageTitle=pageTitle,
                                         QueryStringMessage=queryStringMessage,
                                         GCFMessage=gcfMessage,
                                         GCFaddress=gcfaddress,
                                         VPCMessage=VpcMessage,
                                         GCEaddress=gceaddress))

    if queryStringMessage:
        resp.set_cookie('testcookie', queryStringMessage)
    return resp


if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')
