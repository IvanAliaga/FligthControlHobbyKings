#!/usr/bin/python
'''
Created on 04/06/2014

@author: ivanaliaga
'''

import json
from bottle import static_file, template, response, request, Bottle, abort
from gevent.pywsgi import WSGIServer
from geventwebsocket.server import WebSocketHandler
from geventwebsocket import  WebSocketError
import NavegacionPi
import GpsPoller
import time
import math

app = Bottle()
nav = NavegacionPi.NavegacionPi()
gpsp = GpsPoller.GpsPoller()
gpsp.start()
server = WSGIServer(("192.168.0.4", 8080), app,
                    handler_class=WebSocketHandler)

#Test
@app.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Contro-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Request-Width, X-CSRF-Token'

@app.route('/Control', method='POST')
def control():
    pitch = request.forms.get('Pitch')
    roll  = request.forms.get('Roll')
    yaw   = request.forms.get('Yaw')
    nav.send_data(pitch)
    nav.send_data(roll)
    nav.send_data(yaw)

@app.route('/Aceleracion', method='POST')
def aceleracion():
    throttle = request.forms.get('Throttle')
    nav.send_data(throttle)

@app.route('/Auxiliar', method='POST')
def auxiliar():
    aux = request.forms.get('Aux')
    nav.send_data(aux)

@app.route('/Estado', method='POST')
def estado():
    state = request.forms.get('State')
    nav.send_data(state)
    
@app.route('/destroywebsocket')
def handle_destroywebsocket():
    nav.stop()
    server.stop()

@app.route('/multimedia/<orden>')
def multimedia(orden):
    if orden == 'f':
        return Multimedia.tomarfoto()
    elif orden == 'g':
        return Multimedia.grabarvideo()
    elif orden == 's':
        return Multimedia.streaming()
    else :
        return '<h1><strong>E R R O R, LoL</strong></h1>'

@app.route('/Test')
def test():
    return "<h1>test</h1>"

@app.route('/GPS2')
def gps2():
    return gps()

#@app.route('/GPS')
def gps():
   while 1:
       # In the main thread, every 5 seconds print the current value
       #time.sleep(1)
       lista = [gpsp.get_session().fix.latitude,
                gpsp.get_session().fix.longitude,
                gpsp.get_session().fix.altitude]
		#,
                #gpsp.get_session().fix.eps,
		#gpsp.get_session().fix.epv,
                #gpsp.get_session().fix.epv,
                #gpsp.get_session().fix.ept,
                #gpsp.get_session().fix.speed,
       		#gpsp.get_session().fix.climb,
	 	#gpsp.get_session().fix.track,
		#gpsp.get_session().fix.mode]
       cont = 0  
       for i in range(0, len(lista)):
          if(math.isnan(lista[i])):
	     cont = cont + 1
       if cont == 0:
          return json.dumps(lista)  
          #return { "lat":      lista[0], 
       	  # 	   "lng":      lista[1],
          #     	   "altitude": lista[2]
		   #,
               	   #"eps":      lista[3],
               	   #"epx":      lista[4],
               	   #"epv":      lista[5],
               	   #"ept":      lista[6],
               	   #"speed":    lista[7],
               	   #"climb":    lista[8],
               	   #"track":    lista[9],
               	   #"mode":     lista[10]
          #       }
   return "que hace"

@app.route('/websocket')
def handle_websocket():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')
    while True:
        try:
	    #response.content_type = 'application/json'
            wsock.send(gps())
        except WebSocketError:
            break
    return "web socket gps"

@app.route('/wscontrol')
def control_websocket():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')
    while True:
        try:
	   message = wsock.receive()
	   o = json.loads(message)
	   #print(message)
           nav.send_data(str(o['yaw']))
           nav.send_data(str(o['roll']))
           nav.send_data(str(o['pitch']))
           #print(str(o['yaw']))
           #print(str(o['roll']))
           #print(str(o['pitch']))
	except WebSocketError:
	    break
    return "Web Socket Control"

@app.route('/wsaceleracion')
def aceleracion_websocket():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')
    while True:
        try:
           message = wsock.receive()
           o = json.loads(message)
           #print(message)
           nav.send_data(str(o['throttle']))
        except WebSocketError:
            break
    return "Web Socket Aceleracion"

@app.route('/wsauxiliar')
def auxiliar_websocket():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')
    while True:
        try:
           message = wsock.receive()
           o = json.loads(message)
           #print(message)
           nav.send_data(str(o['aux']))
        except WebSocketError:
            break
    return "Web Socket Auxiliar"
     
@app.route('/wsestado')
def estado_websocket():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')
    while True:
        try:
           message = wsock.receive()
           o = json.loads(message)
           #print(message)
           nav.send_data(str(o['state']))
        except WebSocketError:
            break
    return "Web Socket Auxiliar"

@app.route('/waypoints')
def waypoints():
    return template('UAS/Views/view1.html')

@app.route('/joystick')
def joystick():
    return template('UAS/Views/view2.html')

@app.route('/stream')
def stream():
    return template('UAS/Views/view3.html')

@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='UAS')



server.serve_forever()


