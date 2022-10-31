from init import db, ma # Imports start at the root folder. 
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
    password = db.Column(db.String)

    

class TeacherSchema(ma.Schema):
    # This allows the models to be serialized and deserialized to and from JSON.
    #  Here we only have to list the fields we want to be jsonified.  We don't want to include a password in the schema even though it's encrypted. 
    class Meta:
        fields = ('employee_id', 'title', 'first_name', 'middle_name', 'last_name', 'school_email', 'personal_email', 'phone', 'employment_status', 'pay_scale','gender', 'password')
        ordered = True # puts the keys in the same order as the fields lists above otherwise it will be alphabetical order. 