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

hostname = socket.gethostname()
port = 9999

app = Flask(__name__)
city_status = {}

@app.route("/Instagram")
def callback():
    """
    process the callback from Instagram

    @return:
    """
    global city_status

    city = request.args['content']
    res = city.json()

    return res

@app.route('/Status')
def info():
    """
    Status de las ciudades
    """
    global city_status

    return 'Ok'

if __name__ == '__main__':

    # Ponemos en marcha el servidor Flask
    app.run(host='0.0.0.0', port=9999, debug=False)
