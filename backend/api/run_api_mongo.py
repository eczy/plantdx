import pymongo
import json
from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

client = pymongo.MongoClient("mongodb://elia:squiggle@db-hacksc-shard-00-00-thwez.gcp.mongodb.net:27017,db-hacksc-shard-00-01-thwez.gcp.mongodb.net:27017,db-hacksc-shard-00-02-thwez.gcp.mongodb.net:27017/test?ssl=true&replicaSet=db-hacksc-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.plants


# todo: this will connect to mongoDB
@app.route('/json', methods=['POST'])
class PlantDxAPI(Resource):
    def post(request):
        res = {}
        payload = request.get_json(silent=True)
        if payload is None:
            status = "Incorrect request"
            res['status'] = status
            return json.dumps(res)

        disease = payload.get('disease_name', None)
        if disease is None:
            status = "Incorrect request"
            res['status'] = status
            return json.dumps(res)

        treatments = None
        lookup = db.treatments.find({'disease_name': disease})
        for plantDx in lookup:
            res['disease_name'] = disease
            res['treatments'] = plantDx['treatments']
            status = "OK"
            res['status'] = status
            return json.dumps(res)

        status = "No treatmennts found"
        res['status'] = status
        return json.dumps(res)

# todo: this is handle request, and then translate
api.add_resource(PlantDxAPI, "/plantdx")

if __name__ == '__main__':
    app.run(debug=True, port=4747)


import requests
dictToSend = {'disease_name':'Cedar apple rust'}
endpoint = 'http://127.0.0.1:4747/plantdx'
r = requests.post(endpoint, json=dictToSend)
