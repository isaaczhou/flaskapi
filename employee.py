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
            return {"employee": {
                "employeeID": row[0],
                "prodHours": row[1],
                "teamID": row[2]
            }}

    @classmethod
    def insert_employee(cls, employee):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "INSERT INTO employees VALUES (?,?,?)"
        cursor.execute(query, (employee["employeeID"],
                               employee["prodHours"],
                               employee["teamID"]))
        connection.commit()
        connection.close()

    @classmethod
    def update(cls, employee):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "UPDATE employees SET prodHours=?, teamID=? WHERE employeeID=?"
        cursor.execute(query, (employee["prodHours"], employee["teamID"], employee["employeeID"]))
        connection.commit()
        connection.close()

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
        try:
            self.insert_employee(new_employee)
        except:
            return {"msg": "An error occurred inserting the item"}, 500

        return new_employee, 201

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

        employee = self.find_by_id(id)
        new_employee = {
            "employeeID": id,
            "prodHours": data["prodHours"],
            "teamID": data["teamID"]
        }

        if employee is None:
            try:
                self.insert_employee(new_employee)
            except:
                return {"msg": "An error occurred inserting the item"}, 500
        else:
            self.update(new_employee)

        return new_employee


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
