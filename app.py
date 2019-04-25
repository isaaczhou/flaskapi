from datetime import timedelta
from flask import Flask
from flask_cors import CORS
from flask_jwt import JWT
from flask_restful import Api

from resources.employee import Employee, Team
from security import authenticate, identity
from resources.user import UserRegister

app = Flask(__name__)
app.secret_key = 'random'
CORS(app)
api = Api(app)
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
jwt = JWT(app, authenticate, identity)

api.add_resource(Employee, "/employee/<string:id>")
api.add_resource(Team, "/employees")
api.add_resource(UserRegister, "/register")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
