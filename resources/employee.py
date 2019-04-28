import math
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.employee import EmployeeModel


class Employee(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("firstname", type=str,
                        required=True, help="This field cannot be left blank!")
    parser.add_argument("lastname", type=str,
                        required=True, help="This field cannot be left blank!")

    @jwt_required()
    def get(self, employee_id):
        employee = EmployeeModel.find_by_id(employee_id)
        if employee:
            return employee.json_ts(), 200
        return {"msg": "No Employee with that ID"}, 404

    @jwt_required()
    def post(self, employee_id):
        employee = EmployeeModel.find_by_id(employee_id)
        if employee:
            return {"msg": "An item with id {a} already exists".format(a=employee_id)}, 400

        data = self.parser.parse_args()
        new_employee = EmployeeModel(employee_id, **data)
        try:
            new_employee.save_to_db()
        except:
            return {"msg": "An error occurred inserting the item"}, 500

        return new_employee.json(), 201

    @jwt_required()
    def delete(self, employee_id):
        employee = EmployeeModel.find_by_id(employee_id)
        if employee:
            employee.delete_from_db()
            return {"msg": "Item with ID {a} was deleted".format(a=employee_id)}, 200
        else:
            return {"msg": "Item with ID {a} was not found".format(a=employee_id)}, 400

    @jwt_required()
    def put(self, employee_id):
        data = self.parser.parse_args()

        employee = EmployeeModel.find_by_id(employee_id)

        if employee is None:
            employee = EmployeeModel(employee_id, **data)

        else:
            employee.firstname = data["firstname"]
            employee.lastname = data["lastname"]

        employee.save_to_db()
        return employee.json()


class Employees(Resource):

    def get(self):
        employees = EmployeeModel.query.all()
        to_return = {
            "code": 0,
            "result": {
                "page": 1,
                "page_size": 10,
                "total_count": len(employees),
                "page_count": math.ceil(len(employees) / 10),
                "data_list": [employee.json() for employee in employees]
            }
        }
        return to_return
