from flask import Flask, request, json, Response
from pymongo import MongoClient
import logging as log

app = Flask(__name__)

class MongoAPI:
    def __init__(self, data):
        log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s:\n%(message)s\n')
        #self.client = MongoClient("mongodb://localhost:27017/")  # When only Mongo DB is running on Docker.
        self.client = MongoClient("mongodb://mymongo_1:27017/")     # When both Mongo and This application is running on
                                                                    # Docker and we are using Docker Compose

        database = data['database']
        collection = data['collection']
        cursor = self.client[database]
        self.collection = cursor[collection]
        self.data = data

    def read(self):
        log.info('Reading All Data')
        documents = self.collection.find()
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output

    def write(self, data):
        log.info('Writing Data')
        new_document = data['Document']
        response = self.collection.insert_one(new_document)
        output = {'Status': 'Successfully Inserted',
                  'Document_ID': str(response.inserted_id)}
        return output

@app.route('/')
def base():
    return Response(response=json.dumps({"Status": "UP"}),
                    status=200,
                    mimetype='application/json')

@app.route('/getRam')
def get_ram():
    file = open('/elements/procs/ram.txt','r')
    data = file.readline()
    file.close()
    datos = data.split(',')
    return Response(response=json.dumps({"ramLibre":datos[2]}),
                    status=200,
                    mimetype='application/json') 

@app.route('/getCPU')
def get_cpu():
    file = open('/elements/procs/stat.txt','r')
    data = file.readline()
    file.close()
    datos = data.split(' ')
    t_total = int(datos[2]) + int(datos[3]) + int(datos[4]) + int(datos[5]) + int(datos[6]) + int(datos[7]) + int(datos[8]) + int(datos[9])
    t_idle = int(datos[5]) + int(datos[6])
    t_usage = int(t_total) - int(t_idle)
    cpu_porcentaje = 100 - ((t_usage * 100) / t_total)
    return Response(response=json.dumps({"cpuLibre":cpu_porcentaje}),
                status=200,
                mimetype='application/json') 


@app.route('/mongodb', methods=['GET'])
def mongo_read():
    data = {
        "database": "baseSopes",
        "collection": "oracion"
    }
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    response = obj1.read()
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


@app.route('/mongodb', methods=['POST'])
def mongo_write():
    data = request.json
    if data is None or data == {} or 'Document' not in data:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    response = obj1.write(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')