import math
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.location import LocationModel


class Location(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("location_name", type=str,
                        required=True, help="This field cannot be left blank!")

    @jwt_required()
    def get(self, location_id):
        location = LocationModel.find_by_id(location_id)
        if location:
            return location.json(), 200
        return {"msg": "Location Not Found"}, 404

    @jwt_required()
    def post(self, location_id):
        if LocationModel.find_by_id(location_id):
            return {"msg": "Location already exist"}, 400
        data = self.parser.parse_args()
        new_loc = LocationModel(location_id, **data)
        new_loc.save_to_db()
        return new_loc.json(), 201

    @jwt_required()
    def delete(self, location_id):
        location = LocationModel.find_by_id(location_id)
        if location:
            location.delete_from_db()
            return {"msg": "Location Deleted"}, 200
        return {"msg": "Location Not Found"}, 404

    @jwt_required()
    def put(self, location_id):
        data = self.parser.parse_args()

        location = LocationModel.find_by_id(location_id)

        if location is None:
            location = LocationModel(location_id, **data)

        else:
            location.location_name = data["location_name"]

        location.save_to_db()
        return location.json()


class LocationList(Resource):
    @jwt_required()
    def get(self):
        locations = [loc.json() for loc in LocationModel.query.all()]
        to_return = {
            "code": 0,
            "result": {
                "page": 1,
                "page_size": 10,
                "total_count": len(locations),
                "page_count": math.ceil(len(locations) / 10),
                "data_list": locations
            }
        }
        return to_return