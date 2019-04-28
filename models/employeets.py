from json import dumps

from db import db


class EmployeeTSModel(db.Model):
    """
    Employees Model
    """
    __tablename__ = "employeets"
    employee_ts_id = db.Column(db.Integer, primary_key=True)
    workdate = db.Column(db.DATE)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.employee_id"))
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    fullname = db.Column(db.String(80))
    team_id = db.Column(db.Integer)
    # team_id = db.Column(db.Integer, db.ForeignKey("teams.team_id"))
    team_name = db.Column(db.String(80))
    location_id = db.Column(db.Integer, db.ForeignKey("locations.location_id"))
    location_name = db.Column(db.String(80))
    prod_hours = db.Column(db.Float(precision=2))
    sales = db.Column(db.Float(precision=2))
    avg_speed_answer = db.Column(db.Float(precision=2))
    avg_handle = db.Column(db.Float(precision=2))
    first_call_resolution = db.Column(db.Float(precision=2))
    customer_satisfaction = db.Column(db.Float(precision=2))
    absenteeism = db.Column(db.Float(precision=2))
    input_data_error = db.Column(db.Float(precision=2))
    contact_quality = db.Column(db.Float(precision=2))
    ratings = db.Column(db.Float(precision=2))
    # define foreign key
    employee = db.relationship("EmployeeModel")
    location = db.relationship("LocationModel")

    def __init__(self, employee_ts_id, workdate, employee_id,
                 firstname, lastname, fullname, team_id, team_name,
                 location_id, location_name, prod_hours, sales, avg_speed_answer,
                 avg_handle, first_call_resolution, customer_satisfaction,
                 absenteeism, input_data_error, contact_quality, ratings):
        self.employee_ts_id = employee_ts_id
        self.workdate = workdate
        self.employee_id = employee_id
        self.firstname = firstname
        self.lastname = lastname
        self.fullname = fullname
        self.team_id = team_id
        self.team_name = team_name
        self.location_id = location_id
        self.location_name = location_name
        self.prod_hours = prod_hours
        self.sales = sales
        self.avg_speed_answer = avg_speed_answer
        self.avg_handle = avg_handle
        self.first_call_resolution = first_call_resolution
        self.customer_satisfaction = customer_satisfaction
        self.absenteeism = absenteeism
        self.input_data_error = input_data_error
        self.contact_quality = contact_quality
        self.ratings = ratings

    def json(self):
        return {
            "employee_ts_id": self.employee_ts_id,
            "workdate": dumps(self.workdate, default=str),
            "employee_id": self.employee_id,
            "firstname": self.firstname.strip() if self.firstname else None,
            "lastname": self.lastname.strip() if self.lastname else None,
            # "fullname": self.firstname.strip() + " " + self.lastname.strip(),
            "team_id": self.team_id,
            "team_name": self.team_name,
            "location_id": self.location_id,
            "location_name": self.location_name,
            "sales": self.sales,
            "prod_hours": self.prod_hours,
            "avg_speed_answer": self.avg_speed_answer,
            "avg_handle": self.avg_handle,
            "first_call_resolution": self.first_call_resolution,
            "customer_satisfaction": self.customer_satisfaction,
            "absenteeism": self.absenteeism,
            "input_data_error": self.input_data_error,
            "contact_quality": self.contact_quality,
            "ratings": self.ratings,
        }

    @classmethod
    def find_by_id(cls, employee_id):
        return cls.query.filter_by(employee_id=employee_id).all()

    @classmethod
    def find_by_fullname(cls, fullname):
        return cls.query.filter_by(fullname=fullname).first()

    @classmethod
    def find_by_firstname(cls, firstname):
        return cls.query.filter_by(firstname=firstname).all()

    @classmethod
    def find_by_lastname(cls, lastname):
        return cls.query.filter_by(lastname=lastname).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
