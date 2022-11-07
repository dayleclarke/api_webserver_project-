from init import db, ma # Imports start at the root folder. 
from marshmallow import fields, validates
from marshmallow.validate import Length, OneOf, And, Regexp
from marshmallow.exceptions import ValidationError
from datetime import date

VALID_TYPES = ('Employee', 'Caregiver', 'Student', 'Other')

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50)) # to store honorific titles
    first_name = db.Column(db.String(50), nullable= False)
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable= False)
    password = db.Column(db.String, nullable= False)
    email = db.Column(db.String(100), unique=True, nullable= False)
    phone = db.Column(db.String(20), nullable= False)
    dob = db.Column(db.Date) 
    gender = db.Column(db.String(50))
    type = db.Column(db.String(9), nullable= False)
    
    employee = db.relationship('Employee', back_populates='user', cascade='all, delete', uselist=False) 
    student = db.relationship('Student', back_populates='user', cascade='all, delete', uselist=False) 

# Add any defaults in both places
class UserSchema(ma.Schema):
    student = fields.Nested('StudentSchema', exclude=['user'])
    # Marshmallow has a more extensive and useful validation system than SQLAlchemy so the following validation requirments have been added here to the schema. 
    
    title = fields.String(required = False, load_default=None, validate= Regexp('^[a-zA-Z. &:;]+$', error='Please enter a valid title or honorific, such as Mr. Ms. Dr. or Mx.'))
    first_name = fields.String(required = True, validate=Length(min=1, error='First name must be at least 1 character in length'))
    middle_name = fields.String(validate=Length(min=1, error='Middle name must be at least 1 character in length')) # Validate a none compulsory field that can contain any characters? 
    last_name = fields.String(required = True, validate=Length(min=1, error='Last name must be at least 1 character in length'))
    password = fields.String(load_only=True, validate= Regexp("""^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$#$^()!%*?&]{8,}$""", error='Password must contain a minimum of eight characters, at least one uppercase letter, one lowercase letter, one number and one special character.'))
    email = fields.String(required = True, validate= Regexp("""^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$""", error="Please provide a valid email address"))
    phone= fields.String(required = True, validate= Regexp('^[0-9 ()+]+$', error="Please provide a valid phone number"))
    dob = fields.Date()
    gender = fields.String(required = False, load_default=None, validate= Regexp('^[a-zA-Z. &-:;]+$', error='You have endered a character that is not permitted when describing gender such as a number or special character'))
    type = fields.String(required = True, validate=OneOf(VALID_TYPES, error="The user type must be either an 'Employee', 'Student','Caregiver' or 'Other'."))

    @validates('dob') 
    def validate_dob(self, value): # The value is the dob entered by the user. 
        #If the date of birth is after today's date than raise a validation error.
        if value > date.today():
            raise ValidationError("Date of birth occures after today's date and must be an error.")

    # def more_info()
    #     if type == "student":
    #         # return self.student
    #         # StudentSchema().find(user_id== self.id)
    #     else if type == "teacher":
            # TeacherSchema().find(user_id == self.id)
            # return self.teacher


    class Meta:
        fields = ('id', 'title', 'first_name', 'middle_name', 'last_name', 'password', 'email', 'phone', 'dob', 'gender', 'type', 'student')
        ordered = True # puts the keys in the same order as the fields lists above otherwise it will be alphabetical order. 