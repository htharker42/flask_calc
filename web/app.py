from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import os
from pymongo import MongoClient


app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.aNewDB
UserNum = db["UserNum"]

UserNum.insert({
    'num_of_users':0
})

class Visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]['num_of_users']
        new_num = 1 + prev_num
        UserNum.update({}, {"$set":{'num_of_users':new_num}})
        return str("Hello User " + str(new_num))

@app.route('/')
def running():
    return "Up and Running"

def checkPostedData(postedData, functionName):
    if (functionName == "add" or functionName == "subtract" or functionName == "multiply"):
        if "x" not in postedData or "y" not in postedData:
            return 301
        else:
            return 200
    elif (functionName == "divide"):
        if "x" not in postedData or "y" not in postedData:
            return 301
        elif int(postedData["y"]) == 0:
            return 302
        else:
            return 200

class Add(Resource):
    def post(self):
        postedData = request.get_json()
        status_code = checkPostedData(postedData, "add")
        if status_code != 200:
            retJson = {
                "Message": "Incomplete Data Error",
                "Status Code": 301
            }
            return jsonify(retJson)

        x = postedData["x"]
        y = postedData["y"]

        x = int(x)
        y = int(y)

        ret = x + y
        retMap = {
            "Message": ret,
            "Status Code": status_code
        }
        return jsonify(retMap)

class Subtract(Resource):
  def post(self):
        postedData = request.get_json()
        status_code = checkPostedData(postedData, "subtract")
        if status_code != 200:
            retJson = {
                "Message": "Error",
                "Status Code": 301
            }
            return jsonify(retJson)

        x = postedData["x"]
        y = postedData["y"]

        x = int(x)
        y = int(y)

        ret = x - y
        retMap = {
            "Message": ret,
            "Status Code": status_code
        }
        return jsonify(retMap)


class Multiply(Resource):
  def post(self):
        postedData = request.get_json()
        status_code = checkPostedData(postedData, "multiply")
        if status_code != 200:
            retJson = {
                "Message": "Error",
                "Status Code": 301
            }
            return jsonify(retJson)

        x = postedData["x"]
        y = postedData["y"]

        x = int(x)
        y = int(y)

        ret = x * y
        retMap = {
            "Message": ret,
            "Status Code": status_code
        }
        return jsonify(retMap)


class Divide(Resource):
  def post(self):
        postedData = request.get_json()
        status_code = checkPostedData(postedData, "divide")
        if status_code != 200:
            retJson = {
                "Message": "Error",
                "Status Code": status_code
            }
            return jsonify(retJson)

        x = postedData["x"]
        y = postedData["y"]

        x = int(x)
        y = int(y)

        ret = x / y
        retMap = {
            "Message": ret,
            "Status Code": status_code
        }
        return jsonify(retMap)


api.add_resource(Add, "/add")
api.add_resource(Subtract, "/subtract")
api.add_resource(Multiply, "/multiply")
api.add_resource(Divide, "/divide")
api.add_resource(Visit, "/hello")

if __name__ == "__main__":
    app.run(host='0.0.0.0')
