import pymongo
import json
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse


client = pymongo.MongoClient("mongodb://elia:squiggle@db-hacksc-shard-00-00-thwez.gcp.mongodb.net:27017,db-hacksc-shard-00-01-thwez.gcp.mongodb.net:27017,db-hacksc-shard-00-02-thwez.gcp.mongodb.net:27017/test?ssl=true&replicaSet=db-hacksc-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.plants


def hacksc_http(request):
    res = {}
    payload = request.get_json(silent=False)
    if payload is None:
        status = "Incorrect request: no payload detected"
        res['status'] = status
        return json.dumps(res)

    disease = payload.get('disease_name', None)
    if disease is None:
        status = "Incorrect request: no disease found"
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
