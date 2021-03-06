from db import db


class EmployeeModel(db.Model):
    """
    Employees Model
    """
    __tablename__ = "employees"
    employee_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    fullname = db.Column(db.String(80))

    team_id = db.Column(db.Integer, db.ForeignKey("teams.team_id"))
    team_name = db.Column(db.String(80))
    # define foreign key
    location_id = db.Column(db.Integer, db.ForeignKey("locations.location_id"))
    location_name = db.Column(db.String(80))

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
    status = db.Column(db.Integer)

    location = db.relationship("LocationModel")
    team = db.relationship("TeamModel")

    employeests = db.relationship("EmployeeTSModel", lazy="dynamic")

    def __init__(self, employee_id, firstname, lastname, team_id,
                 team_name, location_id, location_name, prod_hours, sales,
                 avg_speed_answer, avg_handle, first_call_resolution,
                 customer_satisfaction, absenteeism, input_data_error,
                 contact_quality, ratings, status):
        self.employee_id = employee_id
        self.firstname = firstname
        self.lastname = lastname
        # fullname will be calculated based on first and last name
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
        self.status = status

    def json(self):
        return {"employee_id": self.employee_id,
                 "firstname": self.firstname.strip(),
                 "lastname": self.lastname.strip(),
                 "fullname": self.firstname.strip() + " " + self.lastname.strip(),
                 "team_name": self.team_name,
                 "location_name": self.location_name,
                 "prod_hours": self.prod_hours,
                 "sales": self.sales,
                 "avg_speed_answer": self.avg_speed_answer,
                 "avg_handle": self.avg_handle,
                 "first_call_resolution": self.first_call_resolution,
                 "customer_satisfaction": self.customer_satisfaction,
                 "absenteeism": self.absenteeism,
                 "input_data_error": self.input_data_error,
                 "contact_quality": self.contact_quality,
                 "ratings": self.ratings,
                 "status": self.status,
                 }

    def json_ts(self):

        return {"employee_id": self.employee_id,
                "firstname": self.firstname.strip(),
                "lastname": self.lastname.strip(),
                "employee_ts": [employeets.json() for employeets in self.employeests.all()]
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
