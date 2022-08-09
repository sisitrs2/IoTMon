import eventlet
eventlet.monkey_patch()
from flask import Flask, request, render_template, session, request, redirect, abort, make_response, url_for, send_from_directory
import jwt
import json
import sys
import sqlite3
from os import  path, listdir, makedirs
import os
import csv
from datetime import datetime, timedelta
from uuid import uuid4
import urllib.parse
from flask_socketio import SocketIO, emit
import socketio as client_socket

DB_TABLES = './DB/tables.sql'
DB_INIT = './DB/init.sql'
DB = './DB/iotmon.db'

app = Flask(__name__, template_folder="templates")
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
    
    #data = get_scan_json()
    devices = get_devices()
    device_users = get_device_users()
    device_types = get_device_types()

    return render_template('index.html', devices=devices, device_users=device_users, device_types=device_types, username=session["username"])


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


@app.route('/add_device', methods=['POST'])
def add_device():
    #print("--------")
    #if not is_logged():
    #    return render_template('login.html')
    
    data = request.form.to_dict()
    if not data:
        print("ERROR: no data given to add_device.")
        resp = make_response(index())
        return resp

    if not data["name"] or not \
        data["address"] or not \
        data["device_user_id"]:
        print("REDIRECT: Incomplete data for device_add.")
        resp = make_response(index())
        return resp

    username = session['username']
    area_id = db_get(f"SELECT area_id FROM users WHERE username='{ username }';")
    area_id = area_id[0][0]
    db_edit(f"INSERT INTO devices(name, address, device_user_id, type, version, link, area_id) VALUES('{ data['name'] }', '{ data['address'] }', { data['device_user_id'] }, '{ data['type'] }', '{ data['version'] }', '{ data['link'] }', { area_id })")    

    resp = make_response(index())
    return resp
    

@app.route('/add_device_user', methods=['POST'])
def add_device_user():
    #if not is_logged():
    #    return render_template('login.html')
    
    data = request.form.to_dict()
    if not data:
        return redirect(request.referrer)

    if not data["name"] or not \
        data["address"] or not \
        data["device_user"]:
        print("REDIRECT: Incomplete data for device_add.")
        return redirect(request.referrer)

    username = session["username"]
    area_id = db_get(f"SELECT area_id FROM users WHERE username='{username}';")[0][0]
    db_edit(f"INSERT INTO devices(name, address, device_user_id, type, version, link, area_id) VALUES('{ data['name'] }', '{ data['address'] }', { data['device_user_id'] }, '{ data['type'] }', '{ data['version'] }', '{ data['link'] }', { area_id })")    

    return redirect(request.referrer)
   

######################
#                    #
#    DB Functions    #
#                    #
######################


def validate_user_login(creds):
    username = creds["username"]
    password = creds["password"]
    user = db_get(f"SELECT id FROM users WHERE username='{ username }' AND password='{ password }';")
    if user:
        return True
    else:
        return False


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
    print(" >>>>> In is_logged <<<<<<")
    try:
        token = request.cookies['iotmin']
        if not token:
            print("ERROR: No token.")
        data = jwt.decode(token, app.secret_key)
        print("Success token decoded.")
        return True
    except Exception:
        try:
            data = jwt.decode(logged, app.secret_key)
            print("Success token decoded.")
            return True
        except:
            print("Failed token decode.")
            return False


########################
#                      #
#  Database Functions  #
#                      #
########################

def db_edit(query):
    """
    Like db_get() but with commit to change the db and returns the id of the row
    That the Action took place
    """
    #if serialize_input(query):
    #    return
    conn = create_connection()
    cur = conn.cursor()
    print("DB EXECUTE: " + query)
    cur.execute(query)
    conn.commit()
    result = cur.lastrowid
    conn.close()
    return result

def db_get(query):
    conn = create_connection()
    cur = conn.cursor()
    print("DB EXECUTE: " + query)
    cur.execute(query)
    result = cur.fetchall()
    conn.close()
    return result

def get_device_users():
    users = db_get(f"SELECT id, username, type_id FROM device_users;")
    return users

def get_device_types():
    types = db_get(f"SELECT id, name FROM types;")
    obj_types = {}
    for typ in types:
        obj_types[typ[0]] = typ[1]
    return obj_types

def get_devices():
    username = session["username"]
    area_id = db_get(f"SELECT area_id FROM users WHERE username='{username}';")
    if not area_id:
        print("WARNING: db_get_devices - empty area_id")
    
    area_id = area_id[0][0]
    devices = db_get(f"SELECT * FROM devices WHERE area_id='{area_id}';")
    obj_devices = []

    for device in devices:
        obj_device = {
            "Id": device[0],
            "Name": device[1],
            "Address": device[2],
            "TypeID": device[3],
            "Version": device[4],
            "Temperature": device[5],
            "Voltage": device[6],
            "Current": device[7],
            "Status": device[8],
            "Data": device[9],
            "LastScan": device[10],
            "Link": device[11],
            "Device_user_id": device[12]
        }
        obj_devices.append(obj_device)

    return obj_devices


def create_connection():
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(DB)
    except Exception as e:
        print(e)
        conn.close()
    return conn


def init():
    """ Create and initialize DB. """
    with open(DB_TABLES, "r") as table:
        tables = table.read()
    with open(DB_INIT, "r") as initialize:
        init = initialize.read()

    if not os.path.isfile(DB):
        conn = create_connection()
        c = conn.cursor()
        try:
            c.executescript(tables)
            print("DB => Tables Created.")
            c.executescript(init)
            print("DB => DB Initialized.")
        except Exception as e:
            print(e)
        conn.close()
    else:
        print("DB Found.")
    


if __name__ == '__main__':
    init()
    socketio.run(app, debug=True, host='0.0.0.0', port=5454)
