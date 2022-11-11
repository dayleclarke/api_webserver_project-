# This module contains the CRUD operations for the Employee model.
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from init import db, bcrypt
from models.employee import Employee, EmployeeSchema
from models.user import User, UserSchema
from controllers.auth_controller import auth_admin, auth_address

# Adding a blueprint for employees. This will automatically add the prefix employees to the start of all URL's with this blueprint. 
employees_bp = Blueprint('employees', __name__, url_prefix='/employees') # employees is a resource made available through the API

#CREATE
# A route to create one new employee resource 
@employees_bp.route('/', methods=['POST'])
@jwt_required()
def create_user_and_employee():
    # Create a new user and employee model instance for the new employee. 
    # first create a new instance of the user based on the provided input.(SQL: Insert into users (title,first_name,...) values...)
    data = UserSchema().load(request.json) # Load applies the validation rules set on the schema.
    user =  User(
        title = data['title'],
        first_name = data['first_name'],
        middle_name = data['middle_name'],
        last_name = data['last_name'],
        password = bcrypt.generate_password_hash(request.json['password']).decode('utf8'),
        email = data['email'],
        phone = data['phone'],
        dob = data['dob'],
        gender = data['gender'],
        type = data['type'] 
    )
    db.session.add(user)
    db.session.commit()
    # next create a new instance of the employee based on the provided input. (SQL: Insert into employees (hired_date,job_title,...) values...)
    employee = Employee(
        user_id = user.id,
        hired_date = data['employee']['hired_date'],
        job_title = data['employee']['job_title'],
        department = data['employee']['department'],
        is_admin = data['employee']['is_admin']
    )
    db.session.add(employee)
    db.session.commit()
    return EmployeeSchema().dump(employee), 201

# READ
@employees_bp.route('/') 
@jwt_required()
def get_all_employees():
    auth_admin()
    # A route to return all instances of the employees resource in assending order by ID (SQL: select * from employees order by id)
    stmt = db.select(Employee).order_by(Employee.hired_date.desc()) # Build query
    employees = db.session.scalars(stmt) # Execute query
    return EmployeeSchema(many=True).dump(employees) # Respond to client

# This specifies a restful parameter of employee_id that will be an integer. It will only match if the value passed in is an integer. 
@employees_bp.route('/<int:employee_id>/') # Note this is employee_id not user_id
# @jwt_required()
def get_one_employee(employee_id):
    # A route to retrieve a single employee resource based on their employee_id
    # (SQL: select * from employees where id=employee_id)
    stmt = db.select(Employee).filter_by(id=employee_id) # Build query
    employee = db.session.scalar(stmt) # Execute query (scalar is singular as only one employee instance is returned. 
    if employee:  # If the employee_id belongs to an exsiting employee then return that employee instance
        return EmployeeSchema().dump(employee) # remove the many=True because we are only returning a single employee. 
    else:
        # A 404 error with a custom message will be returned if there is no employee with that employee_id. 
        return {'error': f'Employee not found with id {employee_id}.'}, 404

# UPDATE
@employees_bp.route('/<int:employee_id>/', methods=['PUT', 'PATCH'])
# @jwt_required()
def update_one_empoyee(employee_id):
    # A route to update one employee resource (SQL: Update employees set .... where id = id)
    stmt = db.select(Employee).filter_by(id=employee_id) # Build query
    employee = db.session.scalar(stmt) # Execute query
 
    data = EmployeeSchema().load(request.json) # this applies the validation rules set on the schema.
    
    if employee: # If an employee with that id exsists then update any provided fields
        employee.hired_date = data.get('hired_date') or employee.hired_date # The get method will return none if the key doesn't exist rather than raising an exception. 
        employee.job_title = data.get('job_title') or employee.job_title
        employee.department = data.get('department') or employee.department
        employee.is_admin = data.get('is_admin') or employee.is_admin
   
        db.session.commit() # commit all changes to db      
        return EmployeeSchema().dump(employee) # Respond to client
    else:# If there is no employee in a database with that provided id return a not found (404) error with a custom error message.
        return {'error': f'Employee not found with employee ID {employee_id}.'}, 404

# DELETE
@employees_bp.route('/<int:employee_id>/', methods=['DELETE'])
# @jwt_required()
def delete_one_employee(employee_id):
    # authorize()
    # A route to delete one employee resource (SQL: Delete from employees where id=employee_id)
    stmt = db.select(Employee).filter_by(id=employee_id) # Build query to select the employee
    employee = db.session.scalar(stmt)
    # if the user's employee_id exsists delete their records from the database
    if employee:
        db.session.delete(employee)
        db.session.commit() # commit the deletion
        return {'message': f'The records for the employee with Employee ID {employee.id} were deleted successfully'} # Respond to client
    # If the employee_id doesn't exist in the database return a not found (404) error
    else:
        return {'error': f'Employee not found with Employee ID {employee_id}.'}, 404

test_data= {    
    "title": "Ms",
    "first_name": "Rachael",
    "middle_name": "Anne",
    "last_name": "Cook",
    "password": "hamAnd335*",
    "email": "test.coggfg4ttt@bgbc.edu.au",
    "phone": "0414563531",
    "dob": "1980-09-02",
    "gender": "female",
    "type": "Student",
    "employee": {
        "hired_date": "2009-01-01",
        "job_title": "Teacher",
        "department": "English",
        "is_admin": False
        }
}