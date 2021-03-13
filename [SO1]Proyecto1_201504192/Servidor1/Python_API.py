from flask import Flask, request, json, Response
import logging as log
import requests
import json

app = Flask(__name__)


@app.route('/')
def base():
    return Response(response=json.dumps({"Status": "UP"}),
                    status=200,
                    mimetype='application/json')


@app.route('/mongodb', methods=['POST'])
def mongo_write():
    data = request.json
    direccion = ''
    resp1 = requests.get('http://52.72.70.41:80/mongodb')
    datos_a = len(resp1.json())
    resp2 = requests.get('http://3.80.218.121:80/mongodb')
    datos_b = len(resp2.json())
    if datos_a < datos_b:
        direccion = 'http://52.72.70.41:80/mongodb'
    elif datos_a > datos_b:
        direccion = 'http://3.80.218.121:80/mongodb'
    else:
        resp1 = requests.get('http://52.72.70.41:80/getRam')
        datos_a = json.loads(json.dumps(resp1.json()))['ramLibre']
        resp2 = requests.get('http://3.80.218.121:80/getRam')
        datos_b = json.loads(json.dumps(resp2.json()))['ramLibre']
        if datos_a < datos_b:
            direccion = 'http://3.80.218.121:80/mongodb'
        elif datos_a > datos_b:
            direccion = 'http://52.72.70.41:80/mongodb'
        else:
            resp1 = requests.get('http://52.72.70.41:80/getCPU')
            datos_a = json.loads(json.dumps(resp1.json()))['cpuLibre']
            resp2 = requests.get('http://3.80.218.121:80/getCPU')
            datos_b = json.loads(json.dumps(resp2.json()))['cpuLibre']
            if datos_a < datos_b:
                direccion = 'http://3.80.218.121:80/mongodb'
            elif datos_a > datos_b:
                direccion = 'http://52.72.70.41:80/mongodb'
            else:
                direccion = 'http://52.72.70.41:80/mongodb'
    response = requests.post(direccion, json = data)
    return Response(response=json.dumps(response.json()),
                    status=200,
                    mimetype='application/json')



if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
