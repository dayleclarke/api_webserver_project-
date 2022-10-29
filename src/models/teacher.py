from init import db, ma
from marshmallow import fields

class Teacher(db.Model):
    __tablename__ = 'teachers'

    employee_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10))
    first_name = db.Column(db.String(50))
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    school_email = db.Column(db.String(50))
    personal_email = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    employment_status = db.Column(db.String(50))
    pay_scale = db.Column(db.String(50))
    # dob = db.Column(db.Date) 
    # hired_date = db.Column(db.Date)
    gender = db.Column(db.String(50))
    password = db.Column(db.String, nullable=False)

    

class TeacherSchema(ma.Schema):
    class Meta:
        fields = ('employee_id', 'title', 'first_name', 'middle_name', 'last_name', 'school_email', 'personal_email', 'phone', 'employment_status', 'dob', 'hired_date', 'covid_vaccination_status', 'gender', 'password', 'payscale')
        ordered = True # puts the keys in the same order as the fields lists above otherwise it will be alphabetical order. 