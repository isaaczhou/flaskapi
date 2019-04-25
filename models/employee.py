import sqlite3

from db import db


class EmployeeModel(db.Model):
    """
    Employees Model
    """
    __tablename__ = "employees"
    employee_id = db.Column(db.Integer, primary_key=True)
    prod_hours = db.Column(db.Float(precision=2))
    team_id = db.Column(db.String(80))

    def __init__(self, employee_id, prod_hours, team_id):
        self._id = employee_id
        self.prod_hours = prod_hours
        self.team_id = team_id

    def json(self):
        return {"employeeID": self.employee_id, "prodHours": self.prod_hours, "teamID": self.team_id}

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(employee_id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
