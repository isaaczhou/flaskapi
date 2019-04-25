from db import db


class LocationModel(db.Model):
    """
    Locations Model
    """
    __tablename__ = "locations"
    location_id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(80))

    # back reference
    employees = db.relationship("EmployeeModel", lazy="dynamic")

    def __init__(self, location_name):
        self.fullname = location_name

    def json(self):
        return {"location_name": self.location_name,
                "employees": [employee.json() for employee in self.employees.all()]}

    @classmethod
    def find_by_id(cls, location_id):
        return cls.query.filter_by(location_id=location_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
