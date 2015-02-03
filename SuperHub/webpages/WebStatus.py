__author__ = 'bejar'


from flask import Flask, request, render_template
import socket
import time

# Configuration stuff
hostname = socket.gethostname()
port = 9000


app = Flask(__name__)
city_status = {}


@app.route("/Update")
def update():
    """
    Updates the status of the process collecting tweets from a city
    @return:
    """

    global city_status

    city = request.args['content']
    citycount = request.args['count']
    strtime = time.ctime(int(time.time()))
    city_status[city]['time'] = strtime
    city_status[city]['count'] = citycount
    return 'Ok'


@app.route('/Status')
def info():
    """
    Status de las ciudades
    """
    global city_status

    return render_template('Status.html', cities=city_status)

if __name__ == '__main__':

    # Ponemos en marcha el servidor Flask
    app.run(host='0.0.0.0', port=8890, debug=False)
