import math
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.teamts import TeamTSModel


class TeamTS(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("team_name", type=str,
                        required=True, help="This field cannot be left blank!")

    @jwt_required()
    def get(self, team_id):
        teamts = TeamTSModel.find_by_id(team_id)
        if teamts:
            return [team_ts.json() for team_ts in teamts]
        return {"msg": "Team Not Found"}, 404

    @jwt_required()
    def post(self, team_id):
        if TeamTSModel.find_by_id(team_id):
            return {"msg": "Team TS already exist"}, 400
        data = self.parser.parse_args()
        new_team = TeamTSModel(team_id, **data)
        new_team.save_to_db()
        return new_team.json(), 201

    @jwt_required()
    def delete(self, team_id):
        teamts = TeamTSModel.find_by_id(team_id)
        if teamts:
            teamts.delete_from_db()
            return {"msg": "Location Deleted"}, 200
        return {"msg": "Location Not Found"}, 404

    @jwt_required()
    def put(self, team_id):
        data = self.parser.parse_args()

        teamts = TeamTSModel.find_by_id(team_id)

        if teamts is None:
            teamts = TeamTSModel(team_id, **data)

        else:
            teamts.team_name = data["team_name"]

        teamts.save_to_db()
        return teamts.json()


class TeamTSList(Resource):
    @jwt_required()
    def get(self):
        teamts = [loc.json() for loc in TeamTSModel.query.all()]
        to_return = {
            "code": 0,
            "result": {
                "page": 1,
                "page_size": 10,
                "total_count": len(teamts),
                "page_count": math.ceil(len(teamts) / 10),
                "data_list": teamts
            }
        }
        return to_return
