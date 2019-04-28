import math
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.locationts import LocationTSModel


class LocationTS(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("location_name", type=str,
                        required=True, help="This field cannot be left blank!")

    @jwt_required()
    def get(self, location_id):
        locationts = LocationTSModel.find_by_id(location_id)
        if locationts:
            return [loc_ts.json() for loc_ts in locationts]
        return {"msg": "Location Not Found"}, 404

    @jwt_required()
    def post(self, location_id):
        if LocationTSModel.find_by_id(location_id):
            return {"msg": "Location TS already exist"}, 400
        data = self.parser.parse_args()
        new_loc = LocationTSModel(location_id, **data)
        new_loc.save_to_db()
        return new_loc.json(), 201

    @jwt_required()
    def delete(self, location_id):
        locationts = LocationTSModel.find_by_id(location_id)
        if locationts:
            locationts.delete_from_db()
            return {"msg": "Location Deleted"}, 200
        return {"msg": "Location Not Found"}, 404

    @jwt_required()
    def put(self, location_id):
        data = self.parser.parse_args()

        locationts = LocationTSModel.find_by_id(location_id)

        if locationts is None:
            locationts = LocationTSModel(location_id, **data)

        else:
            locationts.location_name = data["location_name"]

        locationts.save_to_db()
        return locationts.json()


class LocationTSList(Resource):
    @jwt_required()
    def get(self):
        locationts = [loc.json() for loc in LocationTSModel.query.all()]
        to_return = {
            "code": 0,
            "result": {
                "page": 1,
                "page_size": 10,
                "total_count": len(locationts),
                "page_count": math.ceil(len(locationts) / 10),
                "data_list": locationts
            }
        }
        return to_return
