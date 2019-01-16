#!/usr/bin/env python

import os

from flask import Flask, jsonify, request, abort
from functools import wraps
import ssl, json, time, datetime

app = Flask(__name__)

targePath = '/home/ec2-user/apps/caliper/data/'  #<-- change if needed

# The actual decorator function
def require_appkey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        if request.headers.get('Authorization') and request.headers.get('Authorization') == key:
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function

# remove null entries in the event POST
def removeNull(d):
    if not isinstance(d, (dict, list)):
        return d
    if isinstance(d, list):
        return [v for v in (removeNull(v) for v in d) if v]
    return {k: v for k, v in ((k, removeNull(v)) for k, v in d.items()) if v}

# define app route
@app.route('/caliper', methods=['POST'])
@require_appkey
def post():
    today = time.strftime('%Y-%m-%d_%H') #<-- change to M for minute (log rotation)
    fileName = targetPath + today + '.json'
    myFile = open(fileName,'a')
    incomingEvent = request.get_json()
    parsedEvent = removeNull(incomingEvent)
    json.dump(parsedEvent, myFile)
    myFile.close()
    return jsonify({'event': parsedEvent}), 201

# define additional app routes
@app.route('/test', methods=['POST'])
def create_event():
    if not request.json or not 'id' in request.json:
        abort(400)
    EVENT = {
        'id': request.json['id'],
        'type': request.json['type'],
        'actor': request.json['actor'],
        'action': request.json['action'],
        'object': request.json['object'],
    }
    return jsonify({'event': EVENT}), 201

# run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', ssl_context='adhoc')

