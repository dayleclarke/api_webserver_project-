from init import db, ma # Imports start at the root folder. 
from marshmallow import fields

class SubjectClass(db.Model):
    __tablename__ = 'subject_classes'

    id = db.Column(db.String(15), primary_key=True)
    employee_id = db.Column(db.Integer) # represents the user of the class
    room = db.Column(db.String(7))
    timetable_line = db.Column(db.Integer) # often a school will strcuture their timetable so that each subject will have schedualed classes base on a specified timetable line (for example 1-6). Classes occuring at the same timetable line will occur at the same time. 
    subject_id = db.Column(db.String(7))
    
    enrollments = db.relationship('Enrollment', back_populates='subject_class', cascade= 'all, delete') # If a subject_class is deleted all of the enrollments in the class will also be deleted. 
  

class SubjectClassSchema(ma.Schema):
    # This allows the models to be serialized and deserialized to and from JSON.
    #  Here we only have to list the fields we want to be jsonified.  We don't want to include a password in the schema even though it's encrypted. 
    # enrollments = fields.List(fields.Nested('EnrollmentSchema', only = ['date', 'student'])) 

    class Meta:
        fields = ('id', 'employee_id', 'room', 'timetable', 'subject_id')
        ordered = True # puts the keys in the same order as the fields lists above otherwise it will be alphabetical order. 