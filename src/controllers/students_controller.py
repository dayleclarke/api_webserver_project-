# This module contains the CRUD operations for the users model.
from flask import Blueprint, request
from init import db, bcrypt
from models.student import Student, StudentSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

# Adding a blueprint for users. This will automatically add the prefix users to the
# start of all URL's with this blueprint. 
students_bp = Blueprint('students', __name__, url_prefix='/students') # students is a resource made available through the API

#CREATE
# A route to create one new student resource 
@students_bp.route('/', methods=['POST'])
# @jwt_required()
def create_student():
    # Create a new Teacher model instance
    data = StudentSchema().load(request.json)

    student = Student(
        homegroup = data['homegroup'],
        enrollment_date = data['enrollment_date'],
        year_level = data['year_level'],
        birth_country = data['birth_country'],
        user_id = data['user_id']
    )

    # Add and commit card to DB
    db.session.add(student)
    db.session.commit()
    # Respond to client
    return StudentSchema().dump(student), 201

# READ
@students_bp.route('/') # because of the url prefix the blueprint will automatically make this /cards/
#This attaches the route to the blueprint
def get_all_user():
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
#         user.school_email = request.json.get('school_email') or user.school_email
#         user.personal_email =request.json.get('personal_email') or user.personal_email
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