import math
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.team import TeamModel


class Team(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("team_name", type=str,
                        required=True, help="This field cannot be left blank!")

    @jwt_required()
    def get(self, team_id):
        team = TeamModel.find_by_id(team_id)
        if team:
            return team.json(), 200
        return {"msg": "Team Not Found"}, 404

    @jwt_required()
    def post(self, team_id):
        if TeamModel.find_by_id(team_id):
            return {"msg": "Team already exist"}, 400
        data = self.parser.parse_args()
        new_team = TeamModel(team_id, **data)
        new_team.save_to_db()
        return new_team.json(), 201

    @jwt_required()
    def delete(self, team_id):
        team = TeamModel.find_by_id(team_id)
        if team:
            team.delete_from_db()
            return {"msg": "Team Deleted"}, 200
        return {"msg": "Team Not Found"}, 404

    @jwt_required()
    def put(self, team_id):
        data = self.parser.parse_args()

        team = TeamModel.find_by_id(team_id)

        if team is None:
            team = TeamModel(team_id, **data)

        else:
            team.team_name = data["team_name"]

        team.save_to_db()
        return team.json()


class TeamList(Resource):
    @jwt_required()
    def get(self):
        teams = [loc.json() for loc in TeamModel.query.all()]
        to_return = {
            "code": 0,
            "result": {
                "page": 1,
                "page_size": 10,
                "total_count": len(teams),
                "page_count": math.ceil(len(teams) / 10),
                "data_list": teams
            }
        }
        return to_return
