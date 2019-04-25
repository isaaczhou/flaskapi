from flask_restful import Resource

from models.location import LocationModel


class Location(Resource):
    def get(self, location_id):
        location = LocationModel.find_by_id(location_id)
        print(location)
        if location:
            return location.json(), 200
        return {"msg": "Location Not Found"}, 404

    def post(self, location_id):
        if LocationModel.find_by_id(location_id):
            return {"msg": "Location already exist"}, 400
        new_loc = LocationModel(location_id)
        try:
            new_loc.save_to_db()
        except:
            return {"msg": "An error occurred while creating the store"}, 500

        return new_loc.json(), 200

    def delete(self, location_id):
        location = LocationModel.find_by_id(location_id)
        if location:
            location.delete_from_db()
            return {"msg": "Location Deleted"}, 200
        return {"msg": "Location Not Found"}, 404

class LocationList(Resource):
    def get(self):
        print(LocationModel.query.all())
        return {"locations": [loc.json() for loc in LocationModel.query.all()]}, 200
