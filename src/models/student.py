from init import db, ma # Imports start at the root folder. 
from marshmallow import fields
from models.user import User, UserSchema

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    homegroup = db.Column(db.String(10))
    enrollment_date = db.Column(db.Date)
    year_level = db.Column(db.Integer)
    birth_country = db.Column(db.String(50))
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # perhaps make this unique to force only one user
    
    user = db.relationship('User', back_populates='student')
    enrollments = db.relationship('Enrollment', back_populates='student', cascade= 'all, delete') # Enrollment is plural as a student can have many enrollments but student is singular as each enrollment relates to exactly one student. Student is the parent enrollment is the child. If a student is deleted all their enrollments need to be deleted too. Back populates is an attribute name that exsists in the related model which in this case is enrollment. 


class StudentSchema(ma.Schema):
    # This allows the models to be serialized and deserialized to and from JSON.
    #  Here we only have to list the fields we want to be jsonified.  We don't want to include a password in the schema even though it's encrypted. 
    user = fields.Nested(UserSchema)
    enrollments = fields.List(fields.Nested('EnrollmentSchema', only = ['date','subject_class']))

    
    class Meta:
        fields = ('user', 'homegroup', 'enrollment_date', 'year_level', 'birth_country', 'enrollments')
        ordered = True # puts the keys in the same order as the fields lists above otherwise it will be alphabetical order.