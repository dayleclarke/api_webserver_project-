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
    is_admin = db.Column(db.Boolean, defalut=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True) # perhaps make this unique to force only one user
    
    user = db.relationship('User', back_populates='employee')

    subject_classes = db.relationship('SubjectClass', back_populates='employee', cascade='all, delete') 


class EmployeeSchema(ma.Schema):
    # This allows the models to be serialized and deserialized to and from JSON.    
    user = fields.Nested(UserSchema, exclude= ['password', 'student', 'employee', 'student_relations', 'address'])
    # enrollments = fields.List(fields.Nested('EnrollmentSchema', only = ['date', 'subject_class']))
    subject_classes = fields.List(fields.Nested('SubjectClassSchema', only=['id','subject.name']))
    # Validations
    hired_date = fields.Date()
    job_title = fields.String(required=True, validate=And(
        Length(min=5, error='Job title must be at least 5 characters long'),
        Regexp('^[a-zA-Z ]+$', error='Only letters, and spaces are allowed in a job title.')
    ))
    department = fields.String(required=True, validate=And(
        Length(min=5, error='Department must be at least 5 characters long'),
        Regexp('^[a-zA-Z ]+$', error='Only letters, and spaces are allowed in department names.')
    ))
    is_admin = fields.Boolean(defalut=False)
    
    @validates('hired_date') 
    def validate_hired_date(self, value): # The value is the hired date entered by the user. 
        #If the enrollment date is after today's date than raise a validation error.
        if value > date.today():
            raise ValidationError("Hired date occures after today's date and must be an error.")

    
    class Meta:
        fields = ('id','user', 'hired_date', 'job_title', 'department', 'is_admin', 'subject_classes')
        ordered = True # puts the keys in the same order as the fields lists above otherwise it will be alphabetical order.
