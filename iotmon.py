from flask import Flask, request, render_template, session, request, redirect, abort, make_response, url_for, send_from_directory
from flask_jsglue import JSGlue
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
COOKIE = 'iotmon'

app = Flask(__name__, template_folder="templates")
jsglue = JSGlue(app)
socketio = SocketIO(app, cors_allowed_origins="http://localhost")

# Connect to socket
sio = client_socket.Client()


#app.config['SESSION_COOKIE_NAME'] = COOKIE
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
    
    # Remove once is_logged is fixed.

    if not "username" in session.keys():
        return render_template('login.html')
    elif session["admin"] == True:
        return make_response(admin())
    
    devices = get_devices()
    device_users = get_device_users()
    device_types = get_device_types()
    alarms = get_alarms()

    # Show only relevant alerts.
    for device in devices:
        if device["Id"] in alarms.keys():
            status = "OK"
            for alarm in alarms[device["Id"]]:
                if alarm["Relevant"] == 1:
                    status = device["Status"]
                    break
            device["Status"] = status

    return render_template('index.html', devices=devices, device_users=device_users, device_types=device_types, username=session["username"], alarms=alarms)


@app.route('/login', methods=['GET', 'POST'])
def login(logged=False):
    if request.method == 'GET':
        resp = make_response(render_template("login.html"))
        resp.set_cookie(COOKIE, "")
        return resp
       
    elif request.method == 'POST':
        creds = request.form.to_dict()
        if creds:
            uid = validate_user_login(creds)
            print(uid)
            if uid:
                session["username"] = creds["username"]
                session["uid"] = uid
                session["admin"] = is_admin(uid)
                clients[session["uid"]] = socketio
                token = jwt.encode({'user': "{}-{}".format(creds['username'], uid), 'exp': datetime.utcnow(
                ) + timedelta(hours=9)}, app.secret_key)
                print(token)
                resp = make_response(index(token))
                resp.set_cookie(COOKIE, token.decode('UTF-8'))
                return resp
        
        # If the user is not authenticated
        resp = make_response(render_template("login.html"))
        resp.set_cookie(COOKIE, "")
        return resp



@app.route('/admin')
def admin():
    #if not is_logged():
    #    return render_template('login.html')

    devices = get_devices()
    device_users = get_device_users()
    device_types = get_device_types()
    areas = get_areas()

    return render_template('devices.html', devices=devices, device_users=device_users, device_types=device_types, username=session["username"], areas=areas)


@app.route('/admin/alarms')
def alarms():
    devices = get_devices()
    device_users = get_device_users()
    device_types = get_device_types()
    alarms = get_alarms()
    areas = get_areas()

    return render_template('alarms.html', devices=devices, device_users=device_users, device_types=device_types, username=session["username"], areas=areas, alarms=alarms)


@app.route('/admin/devices')
def devices():
    return make_response(admin())


@app.route('/admin/system')
def system():
    areas = get_areas()
    users = get_users()

    return render_template('system.html', areas=areas, users=users, username=session["username"])



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
        print("REDIRECT: Incomplete data for add_device.")
        resp = make_response(index())
        return resp

    username = session['username']
    if "area_id" in data:
        area_id = data["area_id"]
    else:
        area_id = db_get(f"SELECT area_id FROM users WHERE username='{ username }';")
        area_id = area_id[0][0]
    
    device_type_id = db_get(f"SELECT type_id FROM device_users WHERE id='{ data['device_user_id'] }';")
    device_type_id = device_type_id[0][0]
    db_set(f"INSERT INTO devices(name, address, device_user_id, type_id, version, link, area_id) VALUES('{ data['name'] }', '{ data['address'] }', { data['device_user_id'] }, '{ device_type_id }', '{ data['version'] }', '{ data['link'] }', { area_id });")    

    resp = make_response(index())
    return resp
    

@app.route('/remove_device', methods=['POST'])
def remove_device():
    #print("--------")
    #if not is_logged():
    #    return render_template('login.html')

    if request.method == 'POST':
        id = request.values.get('id')
    else:
        resp = make_response(index())
        return resp

    if not id:
        print("ERROR: no id given to remove_device.")
        resp = make_response(index())
        return resp

    db_set(f"DELETE FROM devices WHERE id={ id };")    

    resp = make_response(index())
    return resp


@app.route('/remove_user', methods=['POST'])
def remove_user():
    #print("--------")
    #if not is_logged():
    #    return render_template('login.html')

    if request.method == 'POST':
        id = request.values.get('id')
    else:
        resp = make_response(system())
        return resp

    if not id:
        print("ERROR: no id given to remove_user.")
        resp = make_response(system())
        return resp

    db_set(f"DELETE FROM users WHERE id={ id };")    

    resp = make_response(system())
    return resp


@app.route('/remove_area', methods=['POST'])
def remove_area():
    #print("--------")
    #if not is_logged():
    #    return render_template('login.html')

    if request.method == 'POST':
        id = request.values.get('id')
    else:
        resp = make_response(system())
        return resp

    if not id:
        print("ERROR: no id given to remove_area.")
        resp = make_response(system())
        return resp

    db_set(f"DELETE FROM areas WHERE id={ id };")    

    resp = make_response(system())
    return resp

@app.route('/add_area', methods=['POST'])
def add_area():
    #if not is_logged():
    #    return render_template('login.html')
    
    data = request.form.to_dict()
    if not data:
        return redirect(request.referrer)

    if not data["name"]:
        print("REDIRECT: Incomplete data for add_area.")
        return redirect(request.referrer)

    db_set(f"INSERT INTO areas(name) VALUES('{ data['name'] }');")    

    resp = make_response(system())
    return resp
   

@app.route('/add_user', methods=['POST'])
def add_user():
    #if not is_logged():
    #    return render_template('login.html')
    
    data = request.form.to_dict()
    if not data:
        return redirect(request.referrer)

    if not data["username"] or not \
        data["password"] or not \
        data["admin"]:
        print("REDIRECT: Incomplete data for add_user.")
        return redirect(request.referrer)

    username = session["username"]
    area_id = db_get(f"SELECT area_id FROM users WHERE username='{username}';")[0][0]
    db_set(f"INSERT INTO users(username, password, area_id, admin) VALUES('{ data['username'] }', '{ data['password'] }', '{ data['area_id'] }', { data['admin'] });")    

    resp = make_response(system())
    return resp
   

@app.route('/add_device_user', methods=['POST'])
def add_device_user():
    #if not is_logged():
    #    return render_template('login.html')
    
    data = request.form.to_dict()
    if not data:
        return redirect(request.referrer)

    if not data["username"] or not \
        data["password"] or not \
        data["device_type_id"]:
        print("REDIRECT: Incomplete data for add_device_user.")
        return redirect(request.referrer)

    username = session["username"]
    area_id = db_get(f"SELECT area_id FROM users WHERE username='{username}';")[0][0]
    db_set(f"INSERT INTO device_users(username, password, type_id, permissions) VALUES('{ data['username'] }', '{ data['password'] }', '{ data['device_type_id'] }', '{ data['permissions'] }');")    

    resp = make_response(index())
    return resp
   

@app.route('/add_device_type', methods=['POST'])
def add_device_type():
    #if not is_logged():
    #    return render_template('login.html')
    
    data = request.form.to_dict()
    if not data:
        return redirect(request.referrer)

    if not data["name"]:
        print("REDIRECT: Incomplete data for add_device_type.")
        return redirect(request.referrer)
    

    device_types = get_device_types()
    for name in device_types.values():
        if name == data["name"]:
            print("REDIRECT: Name is already taken.")
            return redirect(request.referrer)

    db_set(f"INSERT INTO types(name) VALUES('{ data['name'] }');")    

    resp = make_response(index(True))
    return resp


@app.route('/toggle_relevant', methods=['POST'])
def toggle_relevant():

    if request.method == 'POST':
        id = request.values.get('id')
    else:
        resp = make_response(alarms())
        return resp

    if not id:
        print("REDIRECT: Incomplete data for toggle_alarm.")
        return redirect(request.referrer)
    
    relevant = db_get(f"SELECT relevant FROM alarms WHERE id={ id };")
    if not relevant:
        return redirect(request.referrer)
    
    relevant = relevant[0][0]
    if relevant:
        relevant = 0
    else:
        relevant = 1
    
    db_set(f"UPDATE alarms SET relevant={ relevant } WHERE id={ id };")
    return redirect(request.referrer)



def validate_user_login(creds):
    username = creds["username"]
    password = creds["password"]
    user = db_get(f"SELECT id FROM users WHERE username='{ username }' AND password='{ password }';")
    if user:
        return user[0][0]
    else:
        return False


def is_admin(uid=False):
    if not uid:
        uid = session["uid"]
    
    admin = db_get(f"SELECT admin FROM users WHERE id='{ uid }';")
    return admin[0][0]


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
        print(request.cookies)
        token = request.cookies[COOKIE]
        print(token)

        if not token:
            print("ERROR: No token.")
        data = jwt.decode(token, app.secret_key)
        print("Success token decoded.")
        return True
    except Exception:
        try:
            data = jwt.decode(logged, app.secret_key)
            print(data)
            print("Success token decoded.")
            return True
        except:
            print("Failed token decode.")
            print(logged)
            return False


########################
#                      #
#  Database Functions  #
#                      #
########################

def db_set(query):
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

def get_users():
    users = db_get(f"SELECT * FROM users;")
    obj_users = []
    for user in users:
        obj_user = {
            "Id": user[0],
            "Username": user[1],
            "Password": user[2],
            "Area_id": user[3],
            "Admin": user[4]
        }
        obj_users.append(obj_user)
    return obj_users

def get_areas():
    areas = db_get(f"SELECT id, name FROM areas;")
    obj_areas = {}
    for area in areas:
        obj_areas[area[0]] = area[1]
    return obj_areas

def get_device_types():
    types = db_get(f"SELECT id, name FROM types;")
    obj_types = {}
    for typ in types:
        obj_types[typ[0]] = typ[1]
    return obj_types

def get_devices():
    username = session["username"]
    if not session["admin"]:
        area_id = db_get(f"SELECT area_id FROM users WHERE username='{username}';")
        if not area_id:
            print("WARNING: db_get_devices - empty area_id")
    
        area_id = area_id[0][0]
        devices = db_get(f"SELECT * FROM devices WHERE area_id='{area_id}';")
    else:
        devices = db_get(f"SELECT * FROM devices;")

    obj_devices = []
    for device in devices:
        obj_device = {
            "Id": device[0],
            "Name": device[1],
            "Address": device[2],
            "Type_id": device[3],
            "Version": device[4],
            "Batteries": device[5],
            "Temperature": device[6],
            "Voltage": device[7],
            "Current": device[8],
            "Status": device[9],
            "Data": device[10],
            "LastScan": device[11],
            "Link": device[12],
            "Area_id": device[13],
            "Device_user_id": device[14]
        }
        obj_devices.append(obj_device)

    return obj_devices


def get_alarms():
    username = session["username"]
    if not session["admin"]:
        area_id = db_get(f"SELECT area_id FROM users WHERE username='{username}';")
        if not area_id:
            print("WARNING: db_get_alarms - empty area_id")
    
        area_id = area_id[0][0]
        alarms = db_get(f"SELECT * FROM alarms WHERE area_id='{area_id}';")
    else:
        alarms  = db_get(f"SELECT * FROM alarms;")

    obj_alarms = {}
    for alarm in alarms:
        obj_alarm = {
            "Id": alarm[0],
            "Data": alarm[1],
            "LastScan": alarm[2],
            "Device_id": alarm[3],
            "Area_id": alarm[4],
            "Relevant": alarm[5]
        }
        if obj_alarm["Device_id"] not in obj_alarms:
            obj_alarms[obj_alarm["Device_id"]] = []
        obj_alarms[obj_alarm["Device_id"]].append(obj_alarm)

    return obj_alarms


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
