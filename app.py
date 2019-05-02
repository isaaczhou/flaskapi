from datetime import timedelta

from flask import Flask
from flask_cors import CORS
from flask_jwt import JWT
from flask_restful import Api

from resources.employee import Employee, Employees
from resources.employeets import EmployeeTS, AllEmployeeTS
from resources.location import Location, LocationList
from resources.locationts import LocationTSList, LocationTS
from resources.team import TeamList, Team
from resources.teamts import TeamTS, TeamTSList
from resources.user import UserRegister
from security import authenticate, identity

app = Flask(__name__)
CORS(app)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:Isaac800@localhost/mpdemo"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://fe0oo2iwbrajs3ta:yp9uuiewsjm2m782@r4919aobtbi97j46.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/a18rfhusjbbdpn2z"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'isaac'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=86400)
jwt = JWT(app, authenticate, identity)

api.add_resource(Employee, "/employee/employee_id=<string:employee_id>")
api.add_resource(Employees, "/employees")
api.add_resource(Location, "/location/location_id=<string:location_id>")
api.add_resource(LocationList, "/locations")
api.add_resource(Team, "/team/team_id=<string:team_id>")
api.add_resource(TeamList, "/teams")
api.add_resource(LocationTS, "/locationts/location_id=<string:location_id>")
api.add_resource(LocationTSList, "/locationts")
api.add_resource(TeamTS, "/teamts/team_id=<string:team_id>")
api.add_resource(TeamTSList, "/teamts")
api.add_resource(EmployeeTS, "/employeets/employee_id=<string:employee_id>")
api.add_resource(AllEmployeeTS, "/employeets")
api.add_resource(UserRegister, "/register")

if __name__ == "__main__":
    from db import db

    db.init_app(app)
    app.run(port=5000, debug=True)
