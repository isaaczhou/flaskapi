from flask_sqlalchemy import SQLAlchemy

from app import app

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:Isaac800@localhost/majorperk"

db = SQLAlchemy(app)

class Test(db.Model):
    __tablename__="employee"
    id = db.Column("employeeID", db.Integer, primary_key=True)
    avg_speed_answer = db.Column("AvgSpeedAnswer", db.Unicode)
    avg_handle = db.Column("AvgHandle", db.Unicode)
    sales = db.Column("Sales", db.Unicode)