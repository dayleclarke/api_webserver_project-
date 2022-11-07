from datetime import date
from init import db, ma # Imports start at the root folder. 
from marshmallow import fields, validates
from marshmallow.validate import Length, OneOf, And, Regexp
from marshmallow.exceptions import ValidationError

# This is a constant containing a tuple of all the valid types of users that are excepted for the User type attrbitue 
VALID_TYPES = ('Employee', 'Caregiver', 'Student', 'Other')

class User(db.Model):
    # A model (which is a Python Class) is created for each entity in the database to provide an abstract representation each table. This class inherits from the db.Model.

    __tablename__ = 'users' # This names the table (otherwise SQLAlchemy will name it after the class which is singular: User). Tables must be plural. 

    # The following class attributes are defined to represent a field (column) of the table.   Here we include information such as a name, datatype and constraints.  

    id = db.Column(db.Integer, primary_key=True) # This is the primary key which is a required unique identifier allowing row differentiation
    title = db.Column(db.String(50)) # to store honorific titles
    first_name = db.Column(db.String(50), nullable= False) # Nullable = False means that the attribute cannot be left null.
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable= False)
    password = db.Column(db.String, nullable= False)
    email = db.Column(db.String(100), unique=True, nullable= False) # Unique = True means that this attrbitute cannot have two instances with the same value. No two users are permitted to have the same email address. 
    phone = db.Column(db.String(20), nullable= False)
    dob = db.Column(db.Date) 
    gender = db.Column(db.String(50))
    type = db.Column(db.String(9), nullable= False)
    # Establish a foreign key to link the user to their address in the addresses table. This represents the one-to-many relationship. Each user has only one address but each address can belong to multiple users. 
    address_id = db.Column(db.Integer, db.ForeighKey('addresses.id')) # Adds a foreign key address_id into users. This links to the id (which is the primary key) of the addresses model. This is one side of the relationship. 

    
    # Establish a one-to-one relationship between user and employee. One user can have zero to one employee record (not all users are employees) and each employee will have exactly one entry in the user’s table to store their personal information (each employee must also have information about them stored in the users table).
    #This establishes a relationship between the user and the employee table. The user is the parent table and employee is the child table. 
     
    employee = db.relationship('Employee', cascade='all, delete', uselist=False) # Cascade = 'all, delete' means that if a user is deleted their related resource in the employee table will also be deleted. 

    student = db.relationship('Student', cascade='all, delete', uselist=False) 

# Add any defaults in both places
class UserSchema(ma.Schema):
    student = fields.Nested('StudentSchema', exclude=['user'])
    employee = fields.Nested('EmployeeSchema', exclude=['user'])
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
        fields = ('id', 'title', 'first_name', 'middle_name', 'last_name', 'password', 'email', 'phone', 'dob', 'gender', 'type', 'student', 'employee')
        ordered = True # puts the keys in the same order as the fields lists above otherwise it will be alphabetical order. 
    