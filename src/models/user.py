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
    
    student = db.relationship('Student', back_populates='user', cascade='all, delete', uselist=False) 


class UserSchema(ma.Schema):
    student = fields.Nested('StudentSchema', exclude=['user'])
    
    class Meta:
        fields = ('id', 'title', 'first_name', 'middle_name', 'last_name', 'password', 'school_email', 'personal_email', 'phone', 'dob', 'gender', 'type', 'student')
        ordered = True # puts the keys in the same order as the fields lists above otherwise it will be alphabetical order. 