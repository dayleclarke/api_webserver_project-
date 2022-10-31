# This module contains the CRUD operations for the teachers model.
from flask import Blueprint, request
from init import db
from models.teacher import Teacher, TeacherSchema

# Adding a blueprint for teachers. This will automatically add the prefix teachers to the
# start of all URL's with this blueprint. 
teachers_bp = Blueprint('teachers', __name__, url_prefix='/teachers') # teachers is a resource made available through the API

#CREATE
# A route to create one new teacher resource 
@teachers_bp.route('/', methods=['POST'])
# @jwt_required()
def create_teacher():
    # Create a new Teacher model instance
    data = TeacherSchema().load(request.json)

    teacher = Teacher(
        title = data['title'],
        first_name = data['first_name'],
        middle_name = data['middle_name'],
        last_name = data['last_name'],
        school_email = data['school_email'],
        personal_email = data['personal_email'],
        phone = data['phone'],
        employment_status = data['employment_status'],
        pay_scale = data['pay_scale'],
        gender = data['gender'] 
    )
    # Add and commit card to DB
    db.session.add(teacher)
    db.session.commit()
    # Respond to client
    return TeacherSchema().dump(teacher), 201

# READ
@teachers_bp.route('/') # because of the url prefix the blueprint will automatically make this /cards/
#This attaches the route to the blueprint
def get_all_teachers():
    # A route to return all instances of the teachers resource in assending alphabetical order by last_name
    stmt = db.select(Teacher).order_by(Teacher.last_name)
    teachers = db.session.scalars(stmt)
    return TeacherSchema(many=True).dump(teachers)

# This specifies a restful parameter of employee_id that will be an integer. It will only match if the value passed in is an integer. 
@teachers_bp.route('/<int:employee_id>/')
def get_one_teacher(employee_id):
    # A route to retrieve a single teacher resource based on their employee_id
    stmt = db.select(Teacher).filter_by(employee_id=employee_id)
    teacher = db.session.scalar(stmt) # change this to scalar singular as this is only one we are retrieving 
    if teacher:
        return TeacherSchema().dump(teacher) # remove the many=True because we are only returning a single Card. 
    else:
        # This is the error that will be returned if there is no employee with that ID.
        #  This will return a not found 404 error.  
        return {'error': f'Teacher not found with employee_id {employee_id}'}, 404

# UPDATE
@teachers_bp.route('/<int:employee_id>/', methods=['PUT', 'PATCH'])
# @jwt_required()
def update_one_teacher(employee_id):
    # A route to update one teacher resource
    stmt = db.select(Teacher).filter_by(employee_id=employee_id)
    teacher = db.session.scalar(stmt)
    if teacher:
        teacher.title = request.json.get('title') or teacher.title # The get method will return none if the key doesn't exist rather than raising an exception. 
        teacher.first_name = request.json.get('first_name') or teacher.first_name
        teacher.middle_name = request.json.get('middle_name') or teacher.middle_name
        teacher.last_name = request.json.get('last_name') or teacher.last_name
        teacher.school_email = request.json.get('school_email') or teacher.school_email
        teacher.personal_email =request.json.get('personal_email') or teacher.personal_email
        teacher.phone = request.json.get('phone') or teacher.phone
        teacher.employment_status = request.json.get('employment_status') or teacher.employment_status
        teacher.pay_scale = request.json.get('pay_scale') or teacher.pay_scale
        teacher.gender = request.json.get('gender') or teacher.gender
        
        db.session.commit()      
        return TeacherSchema().dump(teacher)
    else:
        return {'error': f'Teacher not found with employee_id {employee_id}'}, 404

# DELETE
@teachers_bp.route('/<int:employee_id>/', methods=['DELETE'])
# @jwt_required()
def delete_one_teacher(employee_id):
    # authorize()
    # A route to delete one teacher resource
    # select the card
    stmt = db.select(Teacher).filter_by(employee_id=employee_id)
    teacher = db.session.scalar(stmt)
    # if the teacher's employee_id exsists delete their records from the database
    if teacher:
        db.session.delete(teacher)
        db.session.commit()
        return {'message': f'The employee records for {teacher.first_name} {teacher.last_name} were deleted successfully'}
    # If the employee_id doesn't exist in the database return a not found (404) error
    else:
        return {'error': f'Teacher not found with employee_id {employee_id}'}, 404