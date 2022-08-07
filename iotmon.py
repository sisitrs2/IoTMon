import eventlet
eventlet.monkey_patch()
from flask import Flask, request, render_template, session, request, redirect, abort, make_response, url_for, send_from_directory
from flask_jsglue import JSGlue
import jwt
import json
import sys
from os import  path, listdir, makedirs
import os
import csv
from datetime import datetime, timedelta
from uuid import uuid4
import urllib.parse
from flask_socketio import SocketIO, emit
import socketio as client_socket


app = Flask(__name__, template_folder="templates")
jsglue = JSGlue(app)
socketio = SocketIO(app, cors_allowed_origins="http://localhost")

# Connect to socket
sio = client_socket.Client()


app.config['SESSION_COOKIE_NAME'] = "iotmon"
app.secret_key = str(uuid4())  # Nice

clients = {} #key: username; value: list of sockets
#/SocketIO
connected_hosts = {} # key: host_id. value: last time asked for actions.


#### Pages ####

@app.route('/')
def index(logged=False):
    if not is_logged(logged):
        return render_template('login.html')
    
    data = get_scan_json()
    return render_template('index.html', data=data, username=session["username"])


@app.route('/login', methods=['GET', 'POST'])
def login(logged=False):

    if request.method == 'GET':
        resp = make_response(render_template("login.html"))
        resp.set_cookie('iotmon', "")
        return resp
       
    elif request.method == 'POST':
        creds = request.form.to_dict()
        if creds:
            uid = validate_user_login(creds)

            if uid:
                print(creds)
                session["username"] = creds["username"]
                session["uid"] = uid
                clients[session["uid"]] = socketio
                token = jwt.encode({'user': "{}-{}".format(creds['username'], uid), 'exp': datetime.utcnow(
                ) + timedelta(hours=9)}, app.secret_key)
                resp = make_response(index(token.decode('UTF-8')))
                resp.set_cookie('iotmon', token.decode('UTF-8'))
                return resp
        
        # If the user is not authenticated
        resp = make_response(render_template("login.html"))
        resp.set_cookie('iotmon', "")
        return resp

######################
#                    #
#    DB Functions    #
#                    #
######################


def validate_user_login(creds):
    print(creds)
    return "1"


######################
#                    #
#  System Functions  #
#                    #
######################

def get_scan_json():
    json_file = open('map.json', 'r')
    json_text = json_file.read()
    try:
        data = json.loads(json_text)
    except:
        print("Error parsing json file.")
        return ""
    return data
    

def is_logged(logged=False):
    try:
        token = request.cookies['iotmin']
        data = jwt.decode(token, app.secret_key)
        return True
    except Exception:
        try:
            data = jwt.decode(logged, app.secret_key)
            return True
        except:
            return False

def init(app):
    pass

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5454)
