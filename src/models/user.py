from init import db, ma # Imports start at the root folder. 
from marshmallow import fields

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10))
    first_name = db.Column(db.String(50))
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    password = db.Column(db.String)
    school_email = db.Column(db.String, unique=True)
    personal_email = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    dob = db.Column(db.Date) 
    gender = db.Column(db.String(50))
    type = db.Column(db.String(50))
    
    students = db.relationship('Student', back_populates='user', cascade='all, delete') 
    
    # This will return the entire user resource that relates to the student. If a user is detleted delete the student details relating to that user. 
    # employment_status = db.Column(db.String(50))
    # pay_scale = db.Column(db.String(50))
    # hired_date = db.Column(db.Date)

class UserSchema(ma.Schema):
    # This allows the models to be serialized and deserialized to and from JSON.
    #  Here we only have to list the fields we want to be jsonified.  We don't want to include a password in the schema even though it's encrypted. 
    class Meta:
        fields = ('id', 'title', 'first_name', 'middle_name', 'last_name', 'password', 'school_email', 'personal_email', 'phone', 'dob', 'gender', 'type' )
        ordered = True # puts the keys in the same order as the fields lists above otherwise it will be alphabetical order. 