from init import db, ma # Imports start at the root folder. 
from marshmallow import fields, validates
from models.user import User, UserSchema
from marshmallow.exceptions import ValidationError
from datetime import date
from marshmallow.validate import Length, OneOf, And, Regexp, Range

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    homegroup = db.Column(db.String(20))
    enrollment_date = db.Column(db.Date) # Date of enrollment to the school
    year_level = db.Column(db.Integer)
    birth_country = db.Column(db.String(56)) # The United Kingdom of Great Britain and Northern Ireland is the country with the longest name at 56 characters.
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True) # perhaps make this unique to force only one user
    
    user = db.relationship('User', back_populates='student')
    enrollments = db.relationship('Enrollment', back_populates='student', cascade= 'all, delete') # Enrollment is plural as a student can have many enrollments but student is singular as each enrollment relates to exactly one student. Student is the parent enrollment is the child. If a student is deleted all their enrollments need to be deleted too. Back populates is an attribute name that exsists in the related model which in this case is enrollment. 


class StudentSchema(ma.Schema):
    # This allows the models to be serialized and deserialized to and from JSON.    
    user = fields.Nested(UserSchema, exclude= ['password', 'employee'])
    # enrollments = fields.List(fields.Nested('EnrollmentSchema', only = ['date', 'subject_class']))
    
    # Validations
    
    homegroup = fields.String(required=True, validate=And(
        Length(min=3, max= 20, error='Homegroup must be between 3 and 20 characters long'),
        Regexp('^[a-zA-Z0-9 ]+$', error='Only letters, numbers and spaces are allowed in a homegroup.')
    ))
    enrollment_date = fields.Date()
    year_level = fields.Integer(required=True, validate=Range(min=7, max=12))
    birth_country = fields.String(validate=And(
        Length(min=2, max=56, error='Country names must be between 2 and 56 characters long'))
        )
    
    @validates('enrollment_date') 
    def validate_enrollment_date(self, value): # The value is the enrollment date entered by the user. 
        #If the enrollment date is after today's date than raise a validation error.
        if value > date.today():
            raise ValidationError("Date of school enrollment occures after today's date and must be an error.")


    
    class Meta:
        fields = ('user', 'homegroup', 'enrollment_date', 'year_level', 'birth_country')
        ordered = True # puts the keys in the same order as the fields lists above otherwise it will be alphabetical order.

