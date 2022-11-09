# This module contains the CRUD operations for the Students model.
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from init import db, bcrypt
from models.student import Student, StudentSchema
from models.user import User, UserSchema

# Adding a blueprint for students. This will automatically add the prefix students to the start of all URL's with this blueprint. 
students_bp = Blueprint('students', __name__, url_prefix='/students') # students is a resource made available through the API

# #CREATE
# A route to create one new student resource 
@students_bp.route('/', methods=['POST'])
# @jwt_required()
def create_user_and_student():
    # Create a new student and user model instance for the new student.     fggffgdf
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

    student = Student(
        user_id = user.id,
        homegroup = data['student']['homegroup'],
        enrollment_date = data['student']['enrollment_date'],
        year_level = data['student']['year_level'],
        birth_country = data['student']['birth_country']
    )
    db.session.add(student)
    db.session.commit()
    return StudentSchema().dump(student), 201
    # return UserSchema().dump(user), 201

# READ
@students_bp.route('/') 
def get_all_students():
# A route to return all instances of the students resource in assending order by ID (SQL: select * from students order by ID number)
    stmt = db.select(Student).order_by(Student.id) # Build query
    students = db.session.scalars(stmt) # Execute query
    return StudentSchema(many=True).dump(students) # Respond to client

# This specifies a restful parameter of student_id that will be an integer. It will only match if the value passed in is an integer. 
@students_bp.route('/<int:student_id>/') # Note this is student_id not user_id
def get_one_student(student_id):
    # A route to retrieve a single student resource based on their student_id
    # (SQL: select * from users where id=student_id)
    stmt = db.select(Student).filter_by(id=student_id) # Build query
    student = db.session.scalar(stmt) # Execute query (scalar is singular as only one user instance is returned. 
    if student:  # If the student_id belongs to an exsiting student then return that user instance
        return StudentSchema().dump(student) # remove the many=True because we are only returning a single Student. 
    else:
        # A 404 error with a custom message will be returned if there is no student with that student_id.  
        return {'error': f'Student not found with id {student_id}.'}, 404

# # UPDATE
# @students_bp.route('/<int:id>/', methods=['PUT', 'PATCH'])
# # @jwt_required()
# def update_one_user(id):
#     # A route to update one user resource
#     stmt = db.select(User).filter_by(id=id)
#     user = db.session.scalar(stmt)
#     if user:
#         user.title = request.json.get('title') or user.title # The get method will return none if the key doesn't exist rather than raising an exception. 
#         user.first_name = request.json.get('first_name') or user.first_name
#         user.middle_name = request.json.get('middle_name') or user.middle_name
#         user.last_name = request.json.get('last_name') or user.last_name
#         #password?
#         user.email = request.json.get('email') or user.email
#         user.phone = request.json.get('phone') or user.phone
#         user.dob = request.json.get('dob') or user.dob
#         user.gender = request.json.get('gender') or user.gender
#         user.type = request.json.get('type') or user.type

        
#         db.session.commit()      
#         return UserSchema().dump(user)
#     else:
#         return {'error': f'User not found with id {id}'}, 404

# DELETE
@students_bp.route('/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_one_user(id):
    # authorize()
    # A route to delete one user resource
    # select the card
    stmt = db.select(Student).filter_by(id=id)
    student = db.session.scalar(stmt)
    # if the user's employee_id exsists delete their records from the database
    if student:
        db.session.delete(student)
        db.session.commit()
        return {'message': f'The records for {student.first_name} {student.last_name} were deleted successfully'}
    # If the employee_id doesn't exist in the database return a not found (404) error
    else:
        return {'error': f'Student not found with id {id}'}, 404



{   "title": "Ms",
    "first_name": "Rachael",
    "middle_name": "Anne",
    "last_name": "Cook",
    "password": "hamAnd335*",
    "email": "test.coggfg4ttt@bgbc.edu.au",
    "phone": "0414563531",
    "dob": "1980-09-02",
    "gender": "female",
    "type": "Student",
    "address": {
            "complex_number": 14,
            "street_number": 20,
            "street_name": "Captain Road",
            "suburb": "West End",
            "postcode": 4006
    },
    "student": {
            "homegroup": "WH01",
            "enrollment_date": "2020-01-01",
            "year_level": 9,
            "birth_country": "Australia"
        }
}

