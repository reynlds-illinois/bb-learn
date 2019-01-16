from flask import Flask, jsonify, request, abort
from flaskext.mysql import MySQL
from functools import wraps
import os, ssl, json

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'my_sql_user'
app.config['MYSQL_DATABASE_PASSWORD'] = 'my_sql_password'
app.config['MYSQL_DATABASE_DB'] = 'my_db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)

# The actual decorator function
def require_appkey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'     # <- replace with your API key
        if request.headers.get('Authorization') and request.headers.get('Authorization') == key:
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function


# define app route
@app.route('/caliper', methods=['POST'])
@require_appkey
def post():

    add_event = """INSERT INTO caliper.table1 (c_actor_netid, c_action, c_eventTime) VALUES (%s, %s, %s)"""

    EVENT = {

#        'mysensor': request.json['sensor'],
#        'mytype': request.json['data'][0]['actor']['extensions']['bb:user.id']
#        'myactor_pk1': request.json['data'][0]['actor']['extensions']['bb:user.id'],
        'myactor_netid': request.json['data'][0]['actor']['extensions']['bb:user.externalId'],
        'myaction': request.json['data'][0]['action'],
#        'myobject': request.json['data'][0]['object']['type'],
        'myeventTime': request.json['data'][0]['eventTime']
#        'target': request.json['target'],
#        'generated': request.json['generated'],
#        'edApp': request.json['edApp'],
#        'referrer': request.json['referreer'],
#        'group': request.json['group'],
#        'membership': request.json['membership'],
#        'session': request.json['session'],
#        'federatedSession': request.json['federatedSession'],
#        'extensions': request.json['extensions'],
    }

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(add_event, (EVENT['myactor_netid'], EVENT['myaction'], EVENT['myeventTime']))
    conn.commit()

    return jsonify({'event': EVENT}), 201

# define additional app routes
@app.route('/test', methods=['POST', 'GET'])
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
    app.run(host='0.0.0.0', ssl_context='adhoc')     # <-- listens on all, uses default, unsigned ssl for testing

