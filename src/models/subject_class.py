from init import db, ma # Imports start at the root folder. 
from marshmallow import fields
from marshmallow.validate import Length, OneOf, And, Regexp, Range

class SubjectClass(db.Model):
    __tablename__ = 'subject_classes'

    id = db.Column(db.String(15), primary_key=True)
    employee_id = db.Column(db.Integer, nullable=False) # represents the user of the class
    room = db.Column(db.String(7))
    timetable_line = db.Column(db.Integer) # often a school will strcuture their timetable so that each subject will have schedualed classes base on a specified timetable line (for example 1-6). Classes occuring at the same timetable line will occur at the same time. 
    subject_id = db.Column(db.String(15), db.ForeignKey('subjects.id'), nullable=False)
    subject = db.relationship('Subject', back_populates='subject_classes')
    
    enrollments = db.relationship('Enrollment', back_populates='subject_class', cascade= 'all, delete') # If a subject_class is deleted all of the enrollments in the class will also be deleted. 
  

class SubjectClassSchema(ma.Schema):
    subject = fields.Nested('SubjectSchema', exclude=['subject_classes'])
    enrollments = fields.List(fields.Nested('EnrollmentSchema', only = ['date', 'student_id', 'student']))
    
    # Validations
    id = fields.String(required=True, validate=And(
        Length(min=6, max=15, error='Class id must be between 6 and 15 characters long.'),
        Regexp('^[a-zA-Z0-9-]+$', error='Only letters, numbers and hyphens are allowed in a class id.')
    ))
    room = fields.String(validate=And(
        Length(min=4, max=7, error='Room must be at least 4 and up to 7 characters long'),
        Regexp('^[a-zA-Z0-9.]+$', error='Only letters, numbers and periods (dots) are allowed')
    ))
    timetable_line = fields.Integer(validate=Range(min=1, max=6))
    
    class Meta:
        fields = ('id', 'employee_id', 'room', 'timetable_line', 'subject', 'enrollments')
        ordered = True # puts the keys in the same order as the fields lists above otherwise it will be alphabetical order. 

