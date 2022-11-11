# Auth will make use of the users model but indirectly. 
from flask import Blueprint, request, abort
from init import db, bcrypt
from datetime import timedelta
from models.user import User, UserSchema
from models.employee import Employee, EmployeeSchema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

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

# UPDATE
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
def auth_employee():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if not user.type == 'Employee':
        abort(401) # Abort will immediately terminate the request response cycle and send an error response message back to the client. 
def auth_admin():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if not user.type == 'Employee':
        abort(401) # Abort will immediately terminate the request response cycle and send an error response message back to the client.
    elif not user.employee.is_admin:
        abort(401)


def auth_employee_or_self(student_id):
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    # If it is any student other than the student who's details they are trying to access then terminate the request response cycle and send an error response message back to the client.
    if (user.type == 'Student'):
        if not user.student.id == student_id:  
            abort(401)
    elif not user.type == 'Employee': 
        abort(401)

def auth_admin_or_self(employee_id):
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if not user.type == 'Employee': # if the user is any type other than an employee abort
        abort(401) 
        # If not the owner of the employee card request or an admin user abort. 
    elif not ((user.employee.id == employee_id) or (user.employee.is_admin)):  
            abort(401)

def auth_address(address_id):
    user_id = get_jwt_identity() # Get user_id from the JWT token
    stmt = db.select(User).filter_by(id=user_id) # build query to select the user object at that id
    user = db.session.scalar(stmt) # execute query
    if not user.address.id == address_id: # if the user does not have the address listed as their address then
        if not user.type == 'Employee': 
            abort(401) # Abort will immediately terminate the request response cycle and send an error response message back to the client.
        elif not user.employee.is_admin: # if the user is not an admin the request is terminated 
            abort(401)

def auth_self(id):
    user_id = get_jwt_identity() # Get user_id from the JWT token
    stmt = db.select(User).filter_by(id=user_id) # build query to select the user object at that id
    user = db.session.scalar(stmt) # execute query
    if not user.id == id: # if the user does not have the same user id as the one they are attempting to select
        if not user.type == 'Employee':  
            abort(401) # Abort will immediately terminate the request response cycle and send an error response message back to the client.
        elif not user.employee.is_admin:
            abort(401)
