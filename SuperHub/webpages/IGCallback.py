"""
.. module:: IGCallback

IGCallback
*************

:Description: IGCallback

    

:Authors: bejar
    

:Version: 

:Created on: 02/02/2015 8:34 

"""

__author__ = 'bejar'


from flask import Flask, request, render_template
import socket
import time
from instagram.client import InstagramAPI
from httplib import HTTPResponse

hostname = socket.gethostname()
port = 9999

app = Flask(__name__)
city_status = {}

@app.route("/Instagram", methods=['GET', 'POST'])
def callback():
    """
    process the callback from Instagram

    @return:
    """
    #global city_status
    from instagram import client, subscriptions

    if request.method == 'GET':

        if 'hub.challenge' in request.args:
            res = request.args['hub.challenge']
            print request.args
            print request.args['hub.challenge']
            return res
        elif 'code' in request.args:
            return request.args['code']
    else:
        print request.args
        return ''

@app.route('/Status')
def info():
    """
    Status de las ciudades
    """
    global city_status

    return 'Ok'

if __name__ == '__main__':

    # Ponemos en marcha el servidor Flask
    app.run(host='0.0.0.0', port=9999, debug=True)
