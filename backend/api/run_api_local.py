from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

plantsWithDx = [
    {
        "disease_name": "blight",
        "treatments": ["rap music", "cats"]
    },
    {
        "disease_name": "fungi",
        "treatments": ["salicylic acid"]
    }
]


# todo: this will connect to mongoDB
@app.route('/json', methods=['POST'])
class PlantDxAPI(Resource):

    def post(self):
        res = {}
        payload = request.json
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
        for plantDx in plantsWithDx:
            if disease == plantDx['disease_name']:
                res['disease_name'] = disease
                res['treatments'] = plantDx['treatments']
                status = "OK"
                res['status'] = status
                return json.dumps(res)

        status = "No treatmennts found"
        res['status'] = status
        return json.dumps(res)

    def get(self, dx):
        pass

    def put(self, dx):
        pass

    def delete(self, dx):
        pass

# todo: this is handle request, and then translate
api.add_resource(PlantDxAPI, "/plantdx")

if __name__ == '__main__':
    app.run(debug=True, port=4747)
