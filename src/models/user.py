from datetime import date
from init import db, ma # Imports start at the root folder. 
from marshmallow import fields, validates
from marshmallow.validate import Length, OneOf, And, Regexp
from marshmallow.exceptions import ValidationError

# This is a constant containing a tuple of all the valid types of users that are excepted for the User type attrbitue 
VALID_TYPES = ('Employee', 'Caregiver', 'Student', 'Other')

class User(db.Model):
    #A model is created for the User entity to provide an abstract representation the users table. A model is a python class that represents a table where each class attribute is a field (column) of the table.  This class inherits from the db.Model. 

    __tablename__ = 'users' # This names the table (otherwise SQLAlchemy will name it after the class which is singular: User). Tables must be plural. 
    
    # The following class attributes are defined to represent a field (column) of the table.   Here we include information such as a name, datatype, and constraints.  
    id = db.Column(db.Integer, primary_key=True) # This is the primary key which is a required unique identifier allowing row differentiation.
    title = db.Column(db.String(50)) # to store honorific titles
    first_name = db.Column(db.String(50), nullable= False) # Nullable = False means that the attribute cannot be left null. Each user must have a first name listed.
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable= False)
    password = db.Column(db.String, nullable= False)
    email = db.Column(db.String(100), unique=True, nullable= False) # Unique = True means no two users are permitted to have the same email address. Each instance of the user model must have a unique email attribute. 
    phone = db.Column(db.String(20), nullable= False)
    dob = db.Column(db.Date) 
    gender = db.Column(db.String(50))
    type = db.Column(db.String(9), nullable= False)

    # User is linked to the addresses table by the foreign key addresses id (which is that model’s primary key). User represents the child side of this one-to-many relationship as each user has only one address, but each address can belong to multiple users.
    
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id')) 
    # The relation then needs to be defined with Relationship().  This takes numerous parameters. The first parameter indicates which other model (class name) it relates to as a string. Address will encapsulate data from the Address model.  This allows an address object to be provided for each user. The second parameter back_populates is used to specify the other side of the relationship.  It adds a field to each address called user that will return the entire user object for an address. 
    address = db.relationship('Address', back_populates='users')

    
    # Establish a one-to-one relationship between user and employee. One user can have zero to one employee information stored about them (not all users are employees) and each employee will have exactly one entry in the user’s table to store their personal information. Employee is singular as a user can only relate to one employee.  
     
    employee = db.relationship('Employee', back_populates='user', cascade='all, delete', uselist=False) # Relationship() is specified on the user to link the user to the employee model Again the first parameter indicates which model it relates to.  This allows an employee object to be provided for a user. Back_populates is again used to specify the other side of the relationship. It will add a property to employee called user that will return the entire address object for a user.  Cascade all delete was added which means that if a user is deleted their related resource in the employee or student table will also be deleted.  Uselist=False was added here because this is a one-to-one relationship, and this indicates the result is a single object (rather than a list). 

    # The same process is then repeated to link user to student.  This is another one-to-one relationship: 

    student = db.relationship('Student', back_populates='user', cascade='all, delete', uselist=False) 
    
    # Users are also linked to the student_relations table. This is a one-to-one relationship as one user can have many student relations (they may be a caregiver to multiple siblings). Cascade all delete was added which means that if a user is deleted their related student_relations record will also be deleted. . 

    student_relations = db.relationship('StudentRelation', back_populates='user', cascade= 'all, delete')

# Add any defaults in both places
class UserSchema(ma.Schema):
    # Marshmallow allows SQLAlchemy models to be converted into JSON.  The following schema is required to define which model fields are to be converted. 
    
    # Where a field represents an object from a related table Marshmallow needs to be told what schema to use to process the attribute so that it can be represented as a nested field.  
    address = fields.Nested('AddressSchema', exclude=['users']) # When it needs to process address it should process it as a nested field using the Address Schema.  
    student = fields.Nested('StudentSchema', exclude=['user']) # User details are excluded to avoid duplication of data and a RecursionError.   
    employee = fields.Nested('EmployeeSchema', exclude=['user'])
    
     # The student_relations attribute will be represented as a nested list of all the user's studentsrelations. Each element in the list is a student_relations object. This is a list because each user can be a caregiver to multiple students.  
    student_relations = fields.List(fields.Nested('StudentRelationSchema', exclude = ['user']))

    # Marshmallow has a more extensive and useful validation system than SQLAlchemy so the following validation requirements have been added here to the schema.    
    
    title = fields.String(load_default=None, validate= Regexp('^[a-zA-Z. &:;]+$', error='Please enter a valid title or honorific, such as Mr. Ms. Dr. or Mx.')) # only letters and specific punctuation characters are permitted. Load default will set the title to None allowing the field to be empty. 
    first_name = fields.String(required = True, validate=Length(min=1, error='First name must be at least 1 character in length')) # This is a required field that must be at least 1 character long. 
    middle_name = fields.String(validate=Length(min=1, error='Middle name must be at least 1 character in length')) 
    last_name = fields.String(required = True, validate=Length(min=1, error='Last name must be at least 1 character in length'))
    password = fields.String(load_only=True, validate= Regexp("""^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$#$^()!%*?&]{8,}$""", error='Password must contain a minimum of eight characters, at least one uppercase letter, one lowercase letter, one number and one special character.'))
    email = fields.String(required = True, validate= Regexp("""^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$""", error="Please provide a valid email address"))
    phone= fields.String(required = True, validate= Regexp('^[0-9 ()+]+$', error="Please provide a valid phone number"))
    dob = fields.Date()
    gender = fields.String(load_default=None, validate= Regexp('^[a-zA-Z. &-:;]+$', error='You have entered a character that is not permitted when describing gender such as a number or special character'))
    type = fields.String(required = True, validate=OneOf(VALID_TYPES, error="The user type must be either an 'Employee', 'Student','Caregiver' or 'Other'."))

    @validates('dob') 
    def validate_dob(self, value): # The value is the dob entered by the user. 
        #If the date of birth is after today's date than raise a validation error.
        if value > date.today():
            raise ValidationError("Date of birth occurs after today's date and must be an error.")


    class Meta:
        # Define which model fields are to be converted into a permitted object so that it can be Jsonified. 
        fields = ('id', 'title', 'first_name', 'middle_name', 'last_name', 'password', 'email', 'phone', 'dob', 'gender', 'type', 'student', 'employee', 'address', 'student_relations')
        ordered = True # puts the keys in the same order as the fields lists above otherwise it will be alphabetical order. 
    