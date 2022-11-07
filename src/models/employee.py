from init import db, ma # Imports start at the root folder. 
from marshmallow import fields, validates
from models.user import User, UserSchema
from marshmallow.exceptions import ValidationError
from datetime import date
from marshmallow.validate import Length, OneOf, And, Regexp, Range

class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    hired_date = db.Column(db.Date, nullable=False) 
    job_title = db.Column(db.String(128), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True) # perhaps make this unique to force only one user
    
    user = db.relationship('User', back_populates='employee')


class EmployeeSchema(ma.Schema):
    # This allows the models to be serialized and deserialized to and from JSON.    
    user = fields.Nested(UserSchema, exclude= ['password'])
    # enrollments = fields.List(fields.Nested('EnrollmentSchema', only = ['date', 'subject_class']))
    
    # Validations

    
    class Meta:
        fields = ('user', 'hired_date', 'job_title', 'department', 'is_admin')
        ordered = True # puts the keys in the same order as the fields lists above otherwise it will be alphabetical order.
