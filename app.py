from datetime import timedelta

from flask import Flask
from flask_cors import CORS
from flask_jwt import JWT
from flask_restful import Api

from resources.employee import Employee, Team
from resources.location import Location, LocationList
from resources.user import UserRegister
from security import authenticate, identity

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'isaac'
CORS(app)
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
jwt = JWT(app, authenticate, identity)

api.add_resource(Employee, "/employee/<string:id>")
api.add_resource(Team, "/employees")
api.add_resource(Location, "/location/<string:id>")
api.add_resource(LocationList, "/locations")
api.add_resource(UserRegister, "/register")

if __name__ == "__main__":
    from db import db

    db.init_app(app)
    app.run(port=5000, debug=True)
