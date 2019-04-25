from flask import Flask
from flask_cors import CORS
from flask_jwt import JWT, jwt_required
from flask_restful import Api, Resource, reqparse

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'random'
CORS(app)
api = Api(app)
jwt = JWT(app, authenticate, identity)

employees = []


class Employee(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("teamID", type=str,
                        required=True, help="This field cannot be left blank!")
    parser.add_argument("prodHours", type=float,
                        required=True, help="This field cannot be left blank!")

    @jwt_required()
    def get(self, id):
        employee = next(filter(lambda x: x["employeeID"] == id, employees), None)
        # This is the same as following
        # for employee in employees:
        #     if employee["employeeID"] == id:
        #         return employee
        return {"employee": employee}, 200 if employee else 404

    def post(self, id):
        employee = next(filter(lambda x: x["employeeID"] == id, employees), None)
        if employee is not None:
            return {"msg": "An item with id {a} already exists".format(a=id)}, 400

        data = self.parser.parse_args()
        new_employee = {
            "employeeID": id,
            "prodHours": data["prodHours"],
            "teamID": data["teamID"]
        }
        employees.append(new_employee)

        return new_employee, 201

    def delete(self, id):
        global employees
        employees = list(filter(lambda x: x["employeeID"] != id, employees))
        return {"msg": "Item with ID {a} was deleted".format(a=id)}

    def put(self, id):
        data = self.parser.parse_args()

        employee = next(filter(lambda x: x["employeeID"] == id, employees), None)
        if employee is None:
            return self.post(id)
        else:
            employee.update(data)
        return employee


class Team(Resource):
    def get(self):
        return {"team": employees}


api.add_resource(Employee, "/employee/<string:id>")
api.add_resource(Team, "/employees")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
