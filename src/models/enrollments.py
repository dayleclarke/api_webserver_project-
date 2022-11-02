from init import db, ma # Imports start at the root folder. 
from marshmallow import fields

class Enrollment(db.Model):
    __tablename__ = 'enrollments'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    
    subject_class_id = db.Column(db.String(15), db.ForeignKey('subject_classes.id'), nullable=False) # perhaps make this unique to force only one user
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)

    subject_class = db.relationship('SubjectClass', back_populates='enrollments')
    student = db.relationship('Student', back_populates='enrollments')


class EnrollmentSchema(ma.Schema):
    # This allows the models to be serialized and deserialized to and from JSON.
    #  Here we only have to list the fields we want to be jsonified.  We don't want to include a password in the schema even though it's encrypted. 
    subject_class = fields.Nested('SubjectClassSchema', only=['subject_id'])
    student = fields.Nested('StudentSchema')
    
    class Meta:
        fields = ('id', 'date','subject_class', 'student')
        ordered = True 