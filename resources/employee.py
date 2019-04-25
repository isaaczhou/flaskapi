from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.employee import EmployeeModel


class Employee(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("team_id", type=str,
                        required=True, help="This field cannot be left blank!")
    parser.add_argument("prod_hours", type=float,
                        required=True, help="This field cannot be left blank!")
    parser.add_argument("location_id", type=int,
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
        new_employee = EmployeeModel(id, **data)
        try:
            new_employee.save_to_db()
        except:
            return {"msg": "An error occurred inserting the item"}, 500

        return new_employee.json(), 201

    @jwt_required()
    def delete(self, id):
        employee = EmployeeModel.find_by_id(id)
        if employee:
            employee.delete_from_db()
            return {"msg": "Item with ID {a} was deleted".format(a=id)}, 200
        else:
            return {"msg": "Item with ID {a} was not found".format(a=id)}, 400

    @jwt_required()
    def put(self, id):
        data = self.parser.parse_args()

        employee = EmployeeModel.find_by_id(id)

        if employee is None:
            employee = EmployeeModel(id, **data)

        else:
            employee.prod_hours = data["prod_hours"]
            employee.team_id = data["team_id"]
            employee.location_id = data["location_id"]

        employee.save_to_db()
        return employee.json()


class Team(Resource):

    def get(self):

        employees = EmployeeModel.query.all()
        return [employee.json() for employee in employees], 200
