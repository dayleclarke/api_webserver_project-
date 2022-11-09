# This module contains the CRUD operations for the employees model.
from flask import Blueprint, request
from init import db, bcrypt
from models.employee import Employee, EmployeeSchema
from models.user import User, UserSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError

# Adding a blueprint for users. This will automatically add the prefix users to the
# start of all URL's with this blueprint. 
employees_bp = Blueprint('employees', __name__, url_prefix='/employees') # employees is a resource made available through the API

#CREATE
# A route to create one new employee resource 
@employees_bp.route('/', methods=['POST'])
# @jwt_required()
def create_user_and_employee():
    # Create a new employee and user model instance for the new employee. 
    # first create a new instance of the user based on the provided input.

    data = UserSchema().load(request.json)
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
    # next create a new instance of the employee based on the provided input.
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
@employees_bp.route('/') # because of the url prefix the blueprint will automatically make this /employees/
#This attaches the route to the blueprint
def get_all_employees():
    # A route to return all instances of the users resource in assending alphabetical order by last_name
    stmt = db.select(Employee)
    employees = db.session.scalars(stmt)
    return EmployeeSchema(many=True).dump(employees)

# This specifies a restful parameter of employee_id that will be an integer. It will only match if the value passed in is an integer. 
@employees_bp.route('/<int:id>/')
def get_one_employee(id):
    # A route to retrieve a single user resource based on their employee_id
    stmt = db.select(Employee).filter_by(id=id)
    employee = db.session.scalar(stmt) # change this to scalar singular as this is only one we are retrieving 
    if employee:
        return EmployeeSchema().dump(employee) # remove the many=True because we are only returning a single Card. 
    else:
        # This is the error that will be returned if there is no employee with that ID.
        #  This will return a not found 404 error.  
        return {'error': f'Employee not found with id {id}.'}, 404


# DELETE
@employees_bp.route('/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_one_employee(id):
    # authorize()
    # A route to delete one user resource
    # select the card
    stmt = db.select(Employee).filter_by(id=id)
    employee = db.session.scalar(stmt)
    # if the user's employee_id exsists delete their records from the database
    if employee:
        db.session.delete(employee)
        db.session.commit()
        return {'message': f'The records for {employee.first_name} {employee.last_name} were deleted successfully'}
    # If the employee_id doesn't exist in the database return a not found (404) error
    else:
        return {'error': f'Employee not found with id {id}'}, 404

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