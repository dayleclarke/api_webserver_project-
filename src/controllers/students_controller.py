# This module contains the CRUD operations for the students model.
from flask import Blueprint, request
from init import db, bcrypt
from models.student import Student, StudentSchema
from models.user import User, UserSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError

# Adding a blueprint for users. This will automatically add the prefix users to the
# start of all URL's with this blueprint. 
students_bp = Blueprint('students', __name__, url_prefix='/students') # students is a resource made available through the API

# #CREATE
# # Add one student with an exsiting user account:
# @students_bp.route('/<int:user_id>/', methods=['POST'])
# # @jwt_required()
# def create_student(user_id):
#     data = StudentSchema().load(request.json)
#     # Create a new SubjectClass model instance
#     # Select the subject to add a class to based on the incoming subject_id
#     stmt = db.select(User).filter_by(id=user_id)
#     user = db.session.scalar(stmt)
#     if user:
#         student = Student(
#             user_id = user.id,
#             homegroup = data['homegroup'],
#             enrollment_date = data['enrollment_date'],
#             year_level = data['year_level'],
#             birth_country = data['birth_country']
#         )
        
#         # Add and commit card to DB
#         db.session.add(student)
#         db.session.commit()
#         # Respond to client
#         return StudentSchema().dump(student), 201
#     else:
#         return {'error': f'User not found with id {user_id}.'}, 404

# A route to create one new student resource 
@students_bp.route('/', methods=['POST'])
# @jwt_required()
def create_user_and_student():
    # Create a new student and user model instance for the new student. 
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

    # # Add and commit the user to the database if there are no issues with the input.
    # try:
    
    #     # get the new user's id with the provided email address because it is a unique field. 
    #     stmt = db.select(User).filter_by(email=data['email'])
    #     user = db.session.scalar(stmt)

    #     #create a new student instance with the user_id from the user just created. 
    #     data = StudentSchema().load(request.json)
    #     student = Student(
    #         user_id = user.id,
    #         homegroup = data['student.homegroup'],
    #         enrollment_date = data['student.enrollment_date'],
    #         year_level = data['student.year_level'],
    #         birth_country = data['student.birth_country']
    #     )
    #     # Add and commit the new student to the DB
    #     db.session.add(student)
    #     db.session.commit()
    #     # Respond to client
        
    #     return StudentSchema().dump(student), 201
    # except IntegrityError:
    #     return {'message': 'School email address already exists'}, 409


# READ
@students_bp.route('/') # because of the url prefix the blueprint will automatically make this /cards/
#This attaches the route to the blueprint
def get_all_students():
    # A route to return all instances of the users resource in assending alphabetical order by last_name
    stmt = db.select(Student)
    students = db.session.scalars(stmt)
    return StudentSchema(many=True).dump(students)

# This specifies a restful parameter of employee_id that will be an integer. It will only match if the value passed in is an integer. 
@students_bp.route('/<int:id>/')
def get_one_student(id):
    # A route to retrieve a single user resource based on their employee_id
    stmt = db.select(Student).filter_by(id=id)
    student = db.session.scalar(stmt) # change this to scalar singular as this is only one we are retrieving 
    if student:
        return StudentSchema().dump(student) # remove the many=True because we are only returning a single Card. 
    else:
        # This is the error that will be returned if there is no employee with that ID.
        #  This will return a not found 404 error.  
        return {'error': f'Student not found with id {id}.'}, 404

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