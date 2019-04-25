from flask_restful import Resource, reqparse

from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str,
                        required=True, help="This field cannot be left blank!")
    parser.add_argument("password", type=str,
                        required=True, help="This field cannot be left blank!")

    def post(self):
        data = self.parser.parse_args()

        # if user already exists, then done register
        if UserModel.find_by_username(data["username"]):
            return {"msg": "A user with that username already exists"}, 400

        new_user = UserModel(**data)
        new_user.save_to_db()
        return {"msg": "New User added successfully"}, 201
