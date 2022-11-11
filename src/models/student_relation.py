from init import db, ma # Imports start at the root folder. 
from marshmallow import fields, validates
from models.user import User, UserSchema
from models.student import Student, StudentSchema
from marshmallow.validate import Length, OneOf, And, Regexp, Range

class StudentRelation(db.Model):
    __tablename__ = 'student_relations' # Renames the table to be plural

    id = db.Column(db.Integer, primary_key=True) 
    relationship_to_student = db.Column(db.String(50))
    is_primary_contact = db.Column(db.Boolean)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    
    user = db.relationship('User', back_populates='student_relations')
    
    student = db.relationship('Student', back_populates='student_relations')
    
class StudentRelationSchema(ma.Schema):
    user = fields.Nested('UserSchema', exclude= ['id','password', 'employee', 'student', 'student_relations', 'address'])
    student = fields.Nested('StudentSchema', only = ['user.first_name', 'user.last_name'])
   
    class Meta:
        fields = ('student_id', 'student', 'user_id', 'user', 'relationship_to_student', 'is_primary_contact')
        ordered = True # puts the keys in the same order as the fields lists above otherwise it will be alphabetical order.

