from datetime import datetime

import math
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.employeets import EmployeeTSModel


class EmployeeTS(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("workdate", type=lambda x: datetime.strptime(x, '%Y-%m-%dT'),
                        required=True, help="This field cannot be left blank!")
    parser.add_argument("firstname", type=str,
                        required=True, help="This field cannot be left blank!")
    parser.add_argument("lastname", type=str,
                        required=True, help="This field cannot be left blank!")
    parser.add_argument("employee_id", type=int,
                        required=True, help="This field cannot be left blank!")
    parser.add_argument("fullname", type=str,
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

    @jwt_required()
    def get(self, employee_id):
        employeets = EmployeeTSModel.find_by_id(employee_id)
        if employeets:
            return [emp_ts.json() for emp_ts in employeets]
        return {"msg": "No Record with that ID"}, 404

    @jwt_required()
    def post(self, employee_ts_id):
        record = EmployeeTSModel.find_by_id(employee_ts_id)
        if record:
            return {"msg": "A record with id {a} already exists".format(a=employee_ts_id)}, 400

        data = self.parser.parse_args()
        new_record = EmployeeTSModel(employee_ts_id, **data)
        try:
            new_record.save_to_db()
        except:
            return {"msg": "An error occurred inserting the item"}, 500

        return new_record.json(), 201

    @jwt_required()
    def delete(self, employee_ts_id):
        record = EmployeeTSModel.find_by_id(employee_ts_id)
        if record:
            record.delete_from_db()
            return {"msg": "Record with ID {a} was deleted".format(a=employee_ts_id)}, 200
        else:
            return {"msg": "Record with ID {a} was not found".format(a=employee_ts_id)}, 400

    @jwt_required()
    def put(self, employee_ts_id):
        data = self.parser.parse_args()

        record = EmployeeTSModel.find_by_id(employee_ts_id)

        if record is None:
            record = EmployeeTSModel(employee_ts_id, **data)

        else:
            record = {k: v for k, v in data.iteritems()}
            record.id = employee_ts_id

        record.save_to_db()
        return record.json()


class AllEmployeeTS(Resource):

    def get(self):
        employees_ts = EmployeeTSModel.query.all()
        to_return = {
            "code": 0,
            "result": {
                "page": 1,
                "page_size": 10,
                "total_count": len(employees_ts),
                "page_count": math.ceil(len(employees_ts) / 10),
                "data_list": [employeets.json() for employeets in employees_ts]
            }
        }
        return to_return
