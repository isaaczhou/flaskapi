from db import db


class TeamModel(db.Model):
    """
    Locations Model
    """
    __tablename__ = "teams"
    team_id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(80))
    num_employees = db.Column(db.Integer)
    prod_hours = db.Column(db.Float)
    sales = db.Column(db.Float)
    avg_speed_answer = db.Column(db.Float)
    avg_handle = db.Column(db.Float)
    first_call_resolution = db.Column(db.Float)
    customer_satisfaction = db.Column(db.Float)
    absenteeism = db.Column(db.Float)
    input_data_error = db.Column(db.Float)
    contact_quality = db.Column(db.Float)
    ratings = db.Column(db.Float)
    active_counts = db.Column(db.Float)

    # back reference
    employees = db.relationship("EmployeeModel", lazy="dynamic")

    def __init__(self, location_id, location_name):
        self.location_id = location_id
        self.location_name = location_name

    def json(self):
        return {
            "location_id": self.location_id,
            "location_name": self.location_name,
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
