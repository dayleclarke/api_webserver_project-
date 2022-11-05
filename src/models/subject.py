from email.policy import default
from init import db, ma # Imports start at the root folder. 
from marshmallow import fields

class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.String(15), primary_key=True)
    name = db.Column(db.String(50), nullable = False)
    year_level = db.Column(db.Integer, nullable = False)
    max_students = db.Column(db.Integer, default = 30)
    department = db.Column(db.String(15))
    
    subject_classes = db.relationship('SubjectClass', back_populates='subject', cascade='all, delete') 
  

class SubjectSchema(ma.Schema):
    # This allows the models to be serialized and deserialized to and from JSON.
    #  Here we only have to list the fields we want to be jsonified.  We don't want to include a password in the schema even though it's encrypted. 
    # enrollments = fields.List(fields.Nested('EnrollmentSchema', only = ['date', 'student'])) 
    subject_classes = fields.List(fields.Nested('SubjectClassSchema', exclude=['subject']))

    
    class Meta:
        fields = ('id', 'name', 'year_level', 'max_students', 'department', 'subject_classes')
        ordered = True # puts the keys in the same order as the fields lists above otherwise it will be alphabetical order. 