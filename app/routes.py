from app import app
from influxdb import InfluxDBClient
import json
from flask import request, make_response
from flask_cors import cross_origin
import os
from io import StringIO
import csv

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

@app.route('/lapin/csv/<measurement>/<group_id>', methods=['GET', 'OPTIONS'])
@cross_origin()
def get_lapin_csv(measurement, group_id):
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

    # Send query
    result = client.query(query)
    data = list(result.get_points())
    print(data)

    # Convert to CSV
    si = StringIO()
    csv_writer = csv.writer(si)
    # Counter used for writing headers to the CSV 
    count = 0
    for line in data: 
        print(line)
        if count == 0: 
            # Writing headers of CSV file 
            header = line.keys() 
            csv_writer.writerow(header) 
            count += 1
        # Writing data of CSV file 
        csv_writer.writerow(line.values()) 

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    print(output)
    return output


    # print(result)

    # return result
    """
    No caso onde o codigo anterior não funcionasse, tente com este aqui...
    Mas também teria que descomentar o codigo no frontend correspondente ao
    tratamento de dados json...
    response = list(result)
    return json.dumps(response)
    """
