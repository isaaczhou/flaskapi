from db import db


class EmployeeModel(db.Model):
    """
    Employees Model
    """
    __tablename__ = "employees"
    employee_id = db.Column(db.Integer, primary_key=True)
    prod_hours = db.Column(db.Float(precision=2))
    team_id = db.Column(db.String(80))
    # define foreign key
    location_id = db.Column(db.Integer, db.ForeignKey("locations.location_id"))
    location = db.relationship("LocationModel")

    def __init__(self, employee_id, prod_hours, team_id, location_id):
        self.employee_id = employee_id
        self.prod_hours = prod_hours
        self.team_id = team_id
        self.location_id = location_id

    def json(self):
        return {"employee_id": self.employee_id,
                "prod_hours": self.prod_hours,
                "team_id": self.team_id,
                "location_id": self.location_id
                }

    @classmethod
    def find_by_id(cls, employee_id):
        return cls.query.filter_by(employee_id=employee_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
