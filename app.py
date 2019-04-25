from flask import Flask
from flask_cors import CORS
from flask_jwt import JWT
from flask_restful import Api

from employee import Employee, Team
from security import authenticate, identity
from user import UserRegister

app = Flask(__name__)
app.secret_key = 'random'
CORS(app)
api = Api(app)
jwt = JWT(app, authenticate, identity)

api.add_resource(Employee, "/employee/<string:id>")
api.add_resource(Team, "/employees")
api.add_resource(UserRegister, "/register")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
