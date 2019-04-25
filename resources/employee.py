import sqlite3

from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.employee import EmployeeModel


class Employee(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("teamID", type=str,
                        required=True, help="This field cannot be left blank!")
    parser.add_argument("prodHours", type=float,
                        required=True, help="This field cannot be left blank!")

    @jwt_required()
    def get(self, id):
        employee = EmployeeModel.find_by_id(id)
        if employee:
            return employee.json(), 200
        return {"msg": "No Employee with that ID"}, 404

    @jwt_required()
    def post(self, id):
        employee = EmployeeModel.find_by_id(id)
        if employee:
            return {"msg": "An item with id {a} already exists".format(a=id)}, 400

        data = self.parser.parse_args()
        new_employee = EmployeeModel(id, data["prodHours"], data["teamID"])
        try:
            new_employee.insert_employee()
        except:
            return {"msg": "An error occurred inserting the item"}, 500

        return new_employee.json(), 201

    @jwt_required()
    def delete(self, id):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "DELETE FROM employees WHERE employeeID = ?"
        cursor.execute(query, (id,))
        connection.commit()
        connection.close()
        return {"msg": "Item with ID {a} was deleted".format(a=id)}

    @jwt_required()
    def put(self, id):
        data = self.parser.parse_args()

        employee = EmployeeModel.find_by_id(id)
        new_employee = EmployeeModel(id, data["prodHours"], data["teamID"])

        if employee is None:
            try:
                new_employee.insert_employee()
            except:
                return {"msg": "An error occurred inserting the item"}, 500
        else:
            new_employee.update()

        return new_employee.json()


class Team(Resource):
    @classmethod
    @jwt_required()
    def get_all(cls):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT * FROM employees"
        result = cursor.execute(query)
        rows = result.fetchall()
        connection.close()
        all_employees = []
        if rows:
            for row in rows:
                all_employees.append(
                    {"employee": {
                        "employeeID": row[0],
                        "prodHours": row[1],
                        "teamID": row[2]
                    }})
        return all_employees

    def get(self):
        return {"team": self.get_all()}
