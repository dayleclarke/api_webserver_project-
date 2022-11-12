from init import db, ma # Imports start at the root folder. 
from marshmallow import fields
from datetime import date

class Enrollment(db.Model):
    __tablename__ = 'enrollments'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default = date.today())
    
    subject_class_id = db.Column(db.String(15), db.ForeignKey('subject_classes.id'), nullable=False) # perhaps make this unique to force only one user
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)

    subject_class = db.relationship('SubjectClass', back_populates='enrollments')
    student = db.relationship('Student', back_populates='enrollments')


class EnrollmentSchema(ma.Schema):
    # This allows the models to be serialized and deserialized to and from JSON.
    #  Here we only have to list the fields we want to be jsonified.  We don't want to include a password in the schema even though it's encrypted. 
    subject_class = fields.Nested('SubjectClassSchema')
    student = fields.Nested('StudentSchema', exclude= ['student_relations'])
    

    # Marshmallow has a more extensive and useful validation system than SQLAlchemy so the following validation requirements have been added here to the schema.
    date = fields.Date(load_default=date.today()) #Sets this field to a date with today's date as the default value.

    class Meta:
        fields = ('id', 'date','subject_class_id', 'student_id', 'student')
        ordered = True 

