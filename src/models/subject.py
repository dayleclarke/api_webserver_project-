from email.policy import default
from init import db, ma # Imports start at the root folder. 
from marshmallow import fields
from marshmallow.validate import Length, OneOf, And, Regexp, Range

class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.String(15), primary_key=True)
    name = db.Column(db.String(50), nullable = False)
    year_level = db.Column(db.Integer, nullable = False)
    max_students = db.Column(db.Integer, default = 28)
    department = db.Column(db.String(50))
    
    subject_classes = db.relationship('SubjectClass', back_populates='subject', cascade='all, delete') 
  

class SubjectSchema(ma.Schema):
    # This allows the models to be serialized and deserialized to and from JSON.
    #  Here we only have to list the fields we want to be jsonified.

    # enrollments = fields.List(fields.Nested('EnrollmentSchema', only = ['date', 'student'])) 
    subject_classes = fields.List(fields.Nested('SubjectClassSchema', exclude=['subject']))
    # validation

    id = fields.String(required=True, validate=And(
        Length(min=4, error='Subject ID must be at least 4 characters long'),
        Regexp('^[a-zA-Z0-9 ]+$', error='Only letters, numbers and spaces are allowed')
    ))
    
    name = fields.String(required=True, validate=And(
        Length(min=5, error='Title must be at least 5 characters long'),
        Regexp('^[a-zA-Z0-9 ]+$', error='Only letters, numbers and spaces are allowed in subject names')
    ))
    year_level = fields.Integer(required=True, validate=Range(min=7, max=12))
    max_students = fields.Integer(load_default= 28, validate=Range(max=30))
    department = fields.String(required=True, validate=And(
        Length(min=5, error='Department must be at least 5 characters long'),
        Regexp('^[a-zA-Z ]+$', error='Only letters, and spaces are allowed in department names.')
    ))


    
    class Meta:
        fields = ('id', 'name', 'year_level', 'max_students', 'department', 'subject_classes')
        ordered = True # puts the keys in the same order as the fields lists above otherwise it will be alphabetical order. 