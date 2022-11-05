from init import db, ma # Imports start at the root folder. 
from marshmallow import fields
from marshmallow.validate import Length, OneOf, And, Regexp

VALID_TYPES = ('Employee', 'Caregiver', 'Student', 'Other')



class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50)) # to store honorific titles
    first_name = db.Column(db.String(50), nullable= False)
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable= False)
    password = db.Column(db.String)
    email = db.Column(db.String(100), unique=True, nullable= False)
    phone = db.Column(db.String(20), nullable= False)
    dob = db.Column(db.Date) 
    gender = db.Column(db.String(50))
    type = db.Column(db.String(50), nullable= False)
    
    student = db.relationship('Student', back_populates='user', cascade='all, delete', uselist=False) 

# Add any defaults in both places
class UserSchema(ma.Schema):
    student = fields.Nested('StudentSchema', exclude=['user'])
    # Marshmallow has a more extensive and useful validation system than SQLAlchemy so the following validation requirments have been added here to the schema. 
    
    title = fields.String(required = False, load_default=None, validate= Regexp('^[a-zA-Z. &:;]+$', error='Please enter a valid title or honorific, such as Mr. Ms. Dr. or Mx.'))
    first_name = fields.String(required = True, validate=Length(min=1, error='First name must be at least 1 character in length'))
    last_name = fields.String(required = True, validate=Length(min=1, error='Last name must be at least 1 character in length'))
    password = fields.String(validate= Regexp("""^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$#$^()!%*?&]{8,}$""", error='Password must contain a minimum of eight characters, at least one uppercase letter, one lowercase letter, one number and one special character.'))
    email = fields.String(required = True, validate= Regexp("""^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$""", error="Please provide a valid email address"))
    phone= fields.String(required = True, validate= Regexp('^[0-9 ()+]+$', error="Please provide a valid phone number"))
    dob = fields.Date()
    type = fields.String(required = True, validate=OneOf(VALID_TYPES, error="The user type must be either an 'Employee', 'Student','Caregiver' or 'Other'."))

    class Meta:
        fields = ('id', 'title', 'first_name', 'middle_name', 'last_name', 'password', 'email', 'phone', 'dob', 'gender', 'type', 'student')
        ordered = True # puts the keys in the same order as the fields lists above otherwise it will be alphabetical order. 