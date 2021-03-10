from app import app
from influxdb import InfluxDBClient
import json
from flask import request
from flask_cors import cross_origin
import os

from dotenv import load_dotenv
load_dotenv()

HOST = os.environ['INFLUX_HOST']
PORT = os.environ['INFLUX_PORT']
USER = os.environ['USER']
PASSWORD = os.environ['PASSWORD']
DBNAME = os.environ['DBNAME']

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/lapin/<measurement>/<group_id>', methods=['GET', 'OPTIONS'])
@cross_origin()
def get_lapin(measurement, group_id):
    print("GET_LAPIN")
    # Database name as query param or default
    dbname = request.args.get('dbname')
    if not dbname:
        dbname = DBNAME

    # Connect to Database
    client = InfluxDBClient(HOST, PORT, USER, PASSWORD, DBNAME)

    # Prepare query
    field = request.args.get('field')
    if not field:
        field = "*" # get all
    query = 'select {0} from {1} where \"group\"=\'{2}\' '.format(field, measurement, group_id)
    limit = request.args.get('limit')
    if limit:
        query += 'limit {0};'.format(limit)
    else:
        query += ';'
    print("Querying data: " + query)

    # Send query and respond
    result = client.query(query)
    response = list(result.get_points())
    print("Result: {0}".format(response))
    return json.dumps(response)

