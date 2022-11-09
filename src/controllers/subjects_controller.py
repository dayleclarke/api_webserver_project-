# This module contains the CRUD operations for the subjects and subject_classes models.
from flask import Blueprint, request
from init import db, bcrypt
from models.subject_class import SubjectClass, SubjectClassSchema
from models.subject import Subject, SubjectSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

# Add a blueprint for subjects. This will automatically add the prefix subject to the start of all URL's with this blueprint. 
subjects_bp = Blueprint('subjects', __name__, url_prefix='/subjects') 

#CREATE Subject
# A route to create one new subject_class
@subjects_bp.route('/', methods=['POST'])
# @jwt_required()
def create_subject():
    # Create a new Subject model instance (SQL: Insert into subjects (id, name...) values...)
    data = SubjectSchema().load(request.json) # This applies the validation rules set on the schema. 

    subject = Subject(
        id = data['id'],
        name = data['name'],
        year_level = data['year_level'],
        max_students = data.get('max_students'), # Get allows this field to be left blank and the default value to be set. 
        department = data['department']
    )
    # Add and commit subject to DB
    db.session.add(subject)
    db.session.commit()
    # Respond to client
    return SubjectSchema().dump(subject), 201

# READ Subject
@subjects_bp.route('/') 
def get_all_subjects():
    # A route to return all instances of the subjects resource in assending order by subject id (select * from subjects order by id)
    # Build the query
    stmt = db.select(Subject).order_by(Subject.id)
    # Execute the query
    subjects = db.session.scalars(stmt)
    return SubjectSchema(many=True).dump(subjects)


@subjects_bp.route('/<string:id>/') # subject id's are strings (for semantic identification)
def get_one_subject(id):
    # A route to return one instance of a subject resource based on the subject id. 
    # (select * from subjects where id=id)
    # Build the query
    stmt = db.select(Subject).filter_by(id=id)
    # Execute the query
    subject = db.session.scalar(stmt)
    if subject:    
        return SubjectSchema().dump(subject)
    else:
        # This is the error that will be returned if there is no subject with that ID.
        #  This will return a not found 404 error.  
        return {'error': f'Subject not found with id {id}.'}, 404

# UPDATE Subject
@subjects_bp.route('/<string:id>/', methods=['PUT', 'PATCH'])
# @jwt_required()
def update_one_subject(id):
    # A route to update one user resource (SQL: Update subjects set .... where id = id)
     # Build the query
    stmt = db.select(Subject).filter_by(id=id)
    # Execute the query
    subject = db.session.scalar(stmt)
    data = SubjectSchema().load(request.json) # This applies the validation rules set on the schema. 
    if subject:
        subject.id = data.get('id') or subject.id 
        subject.name = data.get('name') or subject.name
        subject.year_level = data.get('year_level') or subject.year_level
        subject.max_students = data.get('max_students') or subject.max_students
        subject.department = data.get('department') or subject.department
              
        db.session.commit()      
        return SubjectSchema().dump(subject)
    else:
        return {'error': f'Subject not found with id {id}.'}, 404

# DELETE Subject
@subjects_bp.route('/<string:id>/', methods=['DELETE'])
# @jwt_required()
def delete_one_subject(id):
    # A route to delete one subject resource (SQL: Delete from subjects where id=id)
     # Build the query
    stmt = db.select(Subject).filter_by(id=id)
    # Execute the query
    subject = db.session.scalar(stmt)
    if subject:
        db.session.delete(subject)
        db.session.commit()
        return {'message': f'Year {subject.year_level} {subject.name} ({subject.id}) was deleted successfully.'}

    else:
        return {'error': f'Subject not found with id {id}.'}, 404
       
# @subjects_bp.route('/<string:subject_id>/classes', methods=['POST'])
# # @jwt_required()
# def create_subject_class(subject_id):
#     # Create a new SubjectClass model instance
#     data = SubjectClassSchema().load(request.json)

#     subject_class = SubjectClass(
#         id = data['id'],
#         employee_id = data['empoyee_id'],
#         room = data['room'],
#         timetable_line = data['timetable_line'],
#         subject_id = data['subject_id']
#     )
#     # Add and commit card to DB
#     db.session.add(subject_class)
#     db.session.commit()
#     # Respond to client
#     return SubjectClassSchema().dump(subject_class), 201

# # CREATE Class
@subjects_bp.route('/<string:subject_id>/classes', methods=['POST'])
# @jwt_required()
def create_subject_class(subject_id):
    # Create a new SubjectClass model instance
    # Select the subject to add a class to based on the incoming subject_id
    data = SubjectClassSchema().load(request.json)
    
    stmt = db.select(Subject).filter_by(id=subject_id)
    subject = db.session.scalar(stmt)
    if subject:
        subject_class = SubjectClass(
            id = data['id'],
            employee_id = data['employee_id'],
            room = data['room'],
            timetable_line = data['timetable_line'],
            subject = subject
        )
        # Add and commit subject_class to DB
        db.session.add(subject_class)
        db.session.commit()
        # Respond to client
        return SubjectClassSchema().dump(subject_class), 201
    else:
        return {'error': f'Subject not found with id {subject_id}.'}, 404


# READ Class
@subjects_bp.route('/classes') 
def get_all_classes():
    # A route to return all instances of the classes resource in assending alphabetical order by last_name
    stmt = db.select(SubjectClass)
    subject_classes = db.session.scalars(stmt)
    return SubjectClassSchema(many=True).dump(subject_classes)


@subjects_bp.route('/classes/<string:id>') 
def get_one_class(id):
    # A route to return one instance of a subject based on the subject id. 
    stmt = db.select(SubjectClass).filter_by(id=id)
    subject_classes = db.session.scalar(stmt)
    if subject_classes:    
        return SubjectClassSchema().dump(subject_classes)
    else:
        # This is the error that will be returned if there is no subject with that ID.
        #  This will return a not found 404 error.  
        return {'error': f'Class not found with id {id}.'}, 404

# A route to return one instance of a subject based on the subject id. 
    # stmt = db.select(Subject).filter_by(id=id)
    # subject = db.session.scalar(stmt)
    # if subject:    
    #     return SubjectSchema().dump(subject)
    # else:
    #     # This is the error that will be returned if there is no subject with that ID.
    #     #  This will return a not found 404 error.  
    #     return {'error': f'Subject not found with id {id}.'}, 404

# # This specifies a restful parameter of employee_id that will be an integer. It will only match if the value passed in is an integer. 
# @subjects_bp.route('/<int:id>/')
# def get_one_user(id):
#     # A route to retrieve a single user resource based on their employee_id
#     stmt = db.select(User).filter_by(id=id)
#     user = db.session.scalar(stmt) # change this to scalar singular as this is only one we are retrieving 
#     if user:
#         return UserSchema().dump(user) # remove the many=True because we are only returning a single Card. 
#     else:
#         # This is the error that will be returned if there is no employee with that ID.
#         #  This will return a not found 404 error.  
#         return {'error': f'User not found with id {id}.'}, 404

