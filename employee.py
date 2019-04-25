import sqlite3

from flask_jwt import jwt_required
from flask_restful import Resource, reqparse


class Employee(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("teamID", type=str,
                        required=True, help="This field cannot be left blank!")
    parser.add_argument("prodHours", type=float,
                        required=True, help="This field cannot be left blank!")

    @classmethod
    def find_by_id(cls, id):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT * FROM employees WHERE employeeID = ?"
        result = cursor.execute(query, (id,))
        row = result.fetchone()
        connection.close()
        if row:
            return {"employee": row}

    @jwt_required()
    def get(self, id):
        employee = self.find_by_id(id)
        if employee:
            return employee, 200
        return {"msg": "No Employee with that ID"}, 404

    @jwt_required()
    def post(self, id):
        employee = self.find_by_id(id)
        if employee:
            return {"msg": "An item with id {a} already exists".format(a=id)}, 400

        data = self.parser.parse_args()
        new_employee = {
            "employeeID": id,
            "prodHours": data["prodHours"],
            "teamID": data["teamID"]
        }

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "INSERT INTO employees VALUES (?,?,?)"
        cursor.execute(query, (new_employee["employeeID"],
                               new_employee["prodHours"],
                               new_employee["teamID"]))
        connection.commit()
        connection.close()
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
