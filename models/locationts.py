from json import dumps

from db import db


class LocationTSModel(db.Model):
    """
    Locations Model
    """
    __tablename__ = "locationts"
    location_ts_id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer)
    location_name = db.Column(db.String(80))
    date = db.Column(db.DATE)
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

    def __init__(self, location_ts_id, location_id, location_name, date, num_employees,
                 prod_hours, sales, avg_speed_answer, avg_handle,
                 first_call_resolution, customer_satisfaction, absenteeism,
                 input_data_error, contact_quality, ratings):
        self.location_ts_id = location_ts_id
        self.location_id = location_id
        self.location_name = location_name
        self.date = date
        self.num_employees = num_employees
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
            "location_ts_id": self.location_ts_id,
            "location_id": self.location_id,
            "location_name": self.location_name,
            "date": dumps(self.date, default=str),
            "num_employees": self.num_employees,
            "prod_hours": self.prod_hours,
            "sales": self.sales,
            "avg_speed_answer": self.avg_speed_answer,
            "avg_handle": self.avg_handle,
            "first_call_resolution": self.first_call_resolution,
            "customer_satisfaction": self.customer_satisfaction,
            "absenteeism": self.absenteeism,
            "input_data_error": self.input_data_error,
            "contact_quality": self.contact_quality,
            "ratings": self.ratings}

    @classmethod
    def find_by_id(cls, location_id):
        return cls.query.filter_by(location_id=location_id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
