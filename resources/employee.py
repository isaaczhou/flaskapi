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
    parser.add_argument("team_id", type=int,
                        required=True, help="This field cannot be left blank!")
    parser.add_argument("team_name", type=str,
                        required=True, help="This field cannot be left blank!")
    parser.add_argument("location_id", type=int,
                        required=True, help="This field cannot be left blank!")
    parser.add_argument("location_name", type=str,
                        required=True, help="This field cannot be left blank!")
    parser.add_argument("prod_hours", type=float,
                        required=True, help="This field cannot be left blank!")
    parser.add_argument("sales", type=float,
                        required=True, help="This field cannot be left blank!")
    parser.add_argument("avg_speed_answer", type=float,
                        required=True, help="This field cannot be left blank!")
    parser.add_argument("avg_handle", type=float,
                        required=True, help="This field cannot be left blank!")
    parser.add_argument("first_call_resolution", type=float,
                        required=True, help="This field cannot be left blank!")
    parser.add_argument("customer_satisfaction", type=float,
                        required=True, help="This field cannot be left blank!")
    parser.add_argument("absenteeism", type=float,
                        required=True, help="This field cannot be left blank!")
    parser.add_argument("input_data_error", type=float,
                        required=True, help="This field cannot be left blank!")
    parser.add_argument("contact_quality", type=float,
                        required=True, help="This field cannot be left blank!")
    parser.add_argument("ratings", type=float,
                        required=True, help="This field cannot be left blank!")
    parser.add_argument("status", type=int,
                        required=True, help="This field cannot be left blank!")

    # @jwt_required()
    def get(self, employee_id):
        employee = EmployeeModel.find_by_id(employee_id)

        if employee:
            temp = employee.json_ts()
            metrics = employee.json()
            temp_ts = temp["employee_ts"]
            to_return = {
                "code": 0,
                "result": {
                    "page": 1,
                    "page_size": 10,
                    "total_count": len(temp_ts),
                    "page_count": math.ceil(len(temp_ts) / 10),
                    "employee_id": temp["employee_id"],
                    "firstname": temp["firstname"],
                    "lastname": temp["lastname"],
                    "prod_hours": metrics["prod_hours"],
                    "prod_hours_max": 3000,
                    "sales": metrics["sales"],
                    "sales_max": 800,
                    "avg_speed_answer": metrics["avg_speed_answer"],
                    "avg_speed_answer_max": 15,
                    "avg_handle": metrics["avg_handle"],
                    "avg_handle_max": 10,
                    "first_call_resolution": metrics["first_call_resolution"],
                    "first_call_resolution_max": 1,
                    "customer_satisfaction": metrics["customer_satisfaction"],
                    "customer_satisfaction_max": 5,
                    "ratings": metrics["ratings"],
                    "ratings_max": 5,
                    "data_list": temp_ts
                }
            }
            return to_return
        return {"msg": "No Employee with that ID"}, 404

    @jwt_required()
    def post(self, employee_id):
        employee = EmployeeModel.find_by_id(employee_id)
        if employee:
            return {"msg": "An Employee with id {a} already exists".format(a=employee_id)}, 400

        data = self.parser.parse_args()
        new_employee = EmployeeModel(employee_id, **data)
        new_employee.fullname = new_employee.firstname.strip() + " " + new_employee.lastname.strip()
        try:
            new_employee.save_to_db()
        except:
            return {"msg": "An error occurred adding the Employee"}, 500

        return new_employee.json(), 201

    @jwt_required()
    def delete(self, employee_id):
        employee = EmployeeModel.find_by_id(employee_id)
        if employee:
            employee.delete_from_db()
            return {"msg": "Employee with ID {a} was deleted".format(a=employee_id)}, 200
        else:
            return {"msg": "Employee with ID {a} was not found".format(a=employee_id)}, 400

    @jwt_required()
    def put(self, employee_id):
        data = self.parser.parse_args()

        employee = EmployeeModel.find_by_id(employee_id)

        if employee is None:
            employee = EmployeeModel(employee_id, **data)

        else:
            employee.delete_from_db()  # delete first if find record
            employee = {k: v for k, v in data.items()}
            employee = EmployeeModel(employee_id, **employee)

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
