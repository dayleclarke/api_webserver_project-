# Auth will make use of the users model but indirectly. 
from flask import Blueprint, request, abort
from init import db, bcrypt
from datetime import timedelta
from models.user import User, UserSchema
from models.employee import Employee, EmployeeSchema
from models.address import Address, AddressSchema
from models.user import User, UserSchema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
#CREATE
# A route to create one new address and user resource at the same time. 

@auth_bp.route('/register', methods=['POST'])
@jwt_required()
def create_address_and_user():
    # Create a new Address model instance (SQL: Insert into addresses (complex_number,...) values...)
    data = AddressSchema().load(request.json) # Load applies the validation rules set on the schema. 
    address = Address(
            complex_number = data.get('complex_number'), # Get allows this field to be left blank
            street_number = data['street_number'], 
            street_name = data['street_name'], 
            suburb = data['suburb'], 
            postcode = data['postcode']
            )
    # Add and commit address to DB
    db.session.add(address)
    db.session.commit()
       
    # Now create a new user instance (SQL: Insert into users (title, first_name...) values...)
    try:

        user = User(
            title = data['users'][0]['title'],
            first_name = data['users'][0]['first_name'],
            middle_name = data['users'][0]['middle_name'],
            last_name = data['users'][0]['last_name'],
            password = bcrypt.generate_password_hash(request.json['users'][0]['password']).decode('utf8'),
            email = data['users'][0]['email'],
            phone = data['users'][0]['phone'],
            dob = data['users'][0]['dob'],
            gender = data['users'][0]['gender'],
            address_id = address.id # Note that type cannot be set here. Type can only be set by an admin employee.  The default value of TBC will be set for each user. 
        )
        # Add and commit user to DB
        db.session.add(user)
        db.session.commit()
        # Respond to client
        return UserSchema(exclude=['employee', 'student', 'student_relations']).dump(user), 201
    except IntegrityError:
        return {'error': 'Email address already in use'}, 409

@auth_bp.route('/login/', methods=['POST'])
def auth_login():
    # Find a user by email address
    stmt = db.select(User).filter_by(email=request.json['email']) # Build the query to select the user with the incoming email address. 
    user = db.session.scalar(stmt) # Execute the query
    # If user exists (if user is truthy) and the incoming password is correct create a JWT token and return it.
    if user and bcrypt.check_password_hash(user.password, request.json['password']):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=5)) # Timedelta is a function that allows a time period to be specified in any unit and it will calculate and return how many minutes that is. This token will expire after 5 days. # change this to one before deployment. Delta means difference.
        # The token isn't stored on the server. Instead the server uses the secret key to validate the token.
        return {'email': user.email, 'token': token, 'type': user.type} # The payload of the token identifys the user. 
    else:
        return {'error': 'Invalid email or password'}, 401 # For security reasons users are not told which one is incorrect. This prevents brute force attacks.

# UPDATE: Set a User Type
@auth_bp.route('/set_user_type/<int:user_id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def set_user_type(user_id):
    auth_admin() # Only admin is allowed to make a user an admin user
    # A route to update one employee resource (SQL: Update employees set .... where id = id)
    stmt = db.select(User).filter_by(id=user_id) # Build query
    user = db.session.scalar(stmt) # Execute query 
    data = UserSchema().load(request.json, partial=True) # this applies the validation rules set on the schema.

    
    if user: # If a user with that id exsists then update any provided fields
        user.title = data.get('title') or user.title # The get method will return none if the key doesn't exist rather than raising an exception. 
        user.first_name = data.get('first_name') or user.first_name
        user.middle_name = data.get('middle_name') or user.middle_name
        user.last_name = data.get('last_name') or user.last_name
        user.email = data.get('email') or user.email
        user.phone = data.get('phone') or user.phone
        user.dob = data.get('dob') or user.dob
        user.gender = data.get('gender') or user.gender
        user.type = data.get('type') or user.type
        
        db.session.commit()      
        return UserSchema().dump(user) # Respond to client
    else:# If there is no user in a database with that provided id return a not found (404) error with a custom error message.
        return {'error': f'User not found with user id {id}.'}, 404    
    


# UPDATE: Set an Admin User
@auth_bp.route('/make_admin/<int:employee_id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def make_admin(employee_id):
    auth_admin() # Only admin is allowed to make a user an admin user
    # A route to update one employee resource (SQL: Update employees set .... where id = id)
    stmt = db.select(Employee).filter_by(id=employee_id) # Build query
    employee = db.session.scalar(stmt) # Execute query 
    data = EmployeeSchema().load(request.json, partial=True) # this applies the validation rules set on the schema.
    if employee: # If an employee with that id exsists then update any provided fields
        employee.hired_date = data.get('hired_date') or employee.hired_date # The get method will return none if the key doesn't exist rather than raising an exception. 
        employee.job_title = data.get('job_title') or employee.job_title
        employee.department = data.get('department') or employee.department
        employee.is_admin = data.get('is_admin') or employee.is_admin
   
        db.session.commit() # commit all changes to db      
        return EmployeeSchema(only = ['id','user', 'hired_date', 'job_title', 'department', 'is_admin']).dump(employee) # Respond to client
    else:# If there is no employee in a database with that provided id return a not found (404) error with a custom error message.
        return {'error': f'Employee not found with employee ID {employee_id}.'}, 404


# This can be imported this into other modules and called when required.
def get_token_identity():
    user_id = get_jwt_identity()# Get user_id from the JWT token
    stmt = db.select(User).filter_by(id=user_id) # build query to select the user object at that id
    return db.session.scalar(stmt) # execute query and return the result

#  This function is used to protect a route so that is can only be accessed by employees. 
def auth_employee():
    user = get_token_identity()
    if not user.type == 'Employee':
        abort(401) # Abort will immediately terminate the request response cycle and send an error response message back to the client. 

#  This function is used to protect a route so that is can only be accessed by employees who also have admin rights. 
def auth_admin():
    user = get_token_identity()
    if not user.type == 'Employee':
        abort(401) # Abort will immediately terminate the request response cycle and send an error response message back to the client.
    elif not user.employee.is_admin:
        abort(401)

#  This function is used to protect a route so that is can only be accessed by the student with the student_id passed in as a parameter or an employee. 
def auth_employee_or_self(student_id):
    user = get_token_identity()
    # If it is any student other than the student who's details they are trying to access then terminate the request response cycle and send an error response message back to the client.
    if (user.type == 'Student'):
        if not user.student.id == student_id:  
            abort(401)
    elif not user.type == 'Employee': 
        abort(401)

#  This function is used to protect a route so that is can only be accessed by the employee with the employee_id passed in as a parameter or an employee with admin rights.
def auth_admin_or_self(employee_id):
    user = get_token_identity()
    if not user.type == 'Employee': # if the user is any type other than an employee abort
        abort(401) 
        # If not the owner of the employee card request or an admin user abort. 
    elif not ((user.employee.id == employee_id) or (user.employee.is_admin)):  
            abort(401)

#  This function is used to protect a route so that is can only be accessed by the users who live at that address or employees with admin rights.
def auth_address(address_id):
    user = get_token_identity()
    if not user.address.id == address_id: # if the user does not have the address listed as their address then
        if not user.type == 'Employee': 
            abort(401) # Abort will immediately terminate the request response cycle and send an error response message back to the client.
        elif not user.employee.is_admin: # if the user is not an admin the request is terminated 
            abort(401)

#  This function is used to protect a route so that is can only be accessed by the user with the user ID passed in as a parameter or an employee with admin rights.
def auth_self(id):
    user = get_token_identity()
    if not user.id == id: # if the user does not have the same user id as the one they are attempting to select
        if not user.type == 'Employee':  
            abort(401) # Abort will immediately terminate the request response cycle and send an error response message back to the client.
        elif not user.employee.is_admin:
            abort(401)
