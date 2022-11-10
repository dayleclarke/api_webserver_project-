# This module contains the CRUD operations for the Subject and SubjectClass models.
from flask import Blueprint, request
from init import db, bcrypt
from models.subject_class import SubjectClass, SubjectClassSchema
from models.subject import Subject, SubjectSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from pprint import pprint
from controllers.auth_controller import auth_admin, auth_self

# Add a blueprint for subjects. This will automatically add the prefix subject to the start of all URL's with this blueprint. 
subjects_bp = Blueprint('subjects', __name__, url_prefix='/subjects') 

#CREATE Subject
# A route to create one new subject
@subjects_bp.route('/', methods=['POST'])
@jwt_required()
def create_subject():
    auth_admin()
    # Create a new Subject model instance (SQL: Insert into subjects (id, name...) values...)
    data = SubjectSchema().load(request.json) # This applies the validation rules set on the schema. 
    subject = Subject(
        id = data['id'], # Subject_id's are a semantic string 
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
    stmt = db.select(Subject).order_by(Subject.id) # Build query
    subjects = db.session.scalars(stmt) # Execute query
    return SubjectSchema(many=True, exclude=["subject_classes"]).dump(subjects) # Respond to client

@subjects_bp.route('/<string:id>/') # subject id's are strings (for semantic identification) It consists of the year level and a 2-3 letter abbreviation of the subject name
@jwt_required() 
def get_one_subject(id):
    
    # A route to return one instance of a subject resource based on the subject id. 
    # (select * from subjects where id=id)
    stmt = db.select(Subject).filter_by(id=id) # Build the query
    subject = db.session.scalar(stmt) # Execute the query
    if subject: # If the subject_id belongs to an exsiting subject then return that subject instance   
        return SubjectSchema().dump(subject) # Respond to client
    else:
        # A 404 error with a custom message will be returned if there is no subject with that id.    
        return {'error': f'Subject not found with id {id}.'}, 404

# UPDATE Subject
@subjects_bp.route('/<string:id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_subject(id):
    auth_admin()
    # A route to update one subject resource (SQL: Update subjects set .... where id = id)
    stmt = db.select(Subject).filter_by(id=id) # Build query
    subject = db.session.scalar(stmt) # Execute query
    data = SubjectSchema().load(request.json, partial=True) # This applies the validation rules set on the schema. 
    # If a subject with that id exsists then update any provided fields
    if subject: 
        subject.id = data.get('id') or subject.id 
        subject.name = data.get('name') or subject.name
        subject.year_level = data.get('year_level') or subject.year_level
        subject.max_students = data.get('max_students') or subject.max_students
        subject.department = data.get('department') or subject.department
              
        db.session.commit()      
        return SubjectSchema().dump(subject)
    else:
    # A 404 error with a custom message will be returned if there is no subject with that id. 
        return {'error': f'Subject not found with id {id}.'}, 404

# DELETE Subject
@subjects_bp.route('/<string:id>/', methods=['DELETE'])
@jwt_required()
def delete_one_subject(id):
    auth_admin()
    # A route to delete one subject resource (SQL: Delete from subjects where id=id)
    stmt = db.select(Subject).filter_by(id=id) # Build query
    subject = db.session.scalar(stmt) # Execute query
    if subject:  # if the subject_id exsists delete the subject record from the database
        db.session.delete(subject)
        db.session.commit() # Commit transaction
        return {'message': f'Year {subject.year_level} {subject.name} ({subject.id}) was deleted successfully.'}

    else:
        return {'error': f'Subject not found with id {id}.'}, 404

# CREATE SubjectClass
@subjects_bp.route('/<string:subject_id>/classes', methods=['POST'])
@jwt_required()
def create_subject_class(subject_id):
    auth_admin()
    # Create a new SubjectClass model instance
    # Select the subject to add a class to based on the incoming subject_id
    data = SubjectClassSchema().load(request.json) # This applies the validation rules set on the schema. 
    # Build the query to select the correct subject. 
    stmt = db.select(Subject).filter_by(id=subject_id)
    subject = db.session.scalar(stmt) # Execute query
    # if the subject included in the URL parameter is valid then add an instance of the SubjectClass
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
        return SubjectClassSchema(exclude=['enrollments']).dump(subject_class), 201
    # If there is no subject in a database with that provided id return a not found (404) error with a custom error message.
    else:
        return {'error': f'Subject not found with id {subject_id}.'}, 404


# READ SubjectClass
@subjects_bp.route('/classes') 
def get_all_subject_classes():
    # A route to return all instances of the classes resource. (SQL: select * from subject_classes)
    stmt = db.select(SubjectClass) # Build query
    subject_classes = db.session.scalars(stmt) # Execute query
    return SubjectClassSchema(many=True).dump(subject_classes) # Respond to client


@subjects_bp.route('/classes/<string:subject_class_id>') 
def get_one_subject_class(subject_class_id):
    # A route to return one instance of a subject class based on the subject_class_id. 
    stmt = db.select(SubjectClass).filter_by(id=subject_class_id)
    subject_classes = db.session.scalar(stmt)
    if subject_classes:    
        return SubjectClassSchema().dump(subject_classes)
    else:
        # This is the error that will be returned if there is no subject with that ID.
        #  This will return a not found 404 error.  
        return {'error': f'Class not found with id {subject_class_id}.'}, 404

# UPDATE SubjectClass
@subjects_bp.route('/classes/<string:subject_class_id>/', methods=['PUT', 'PATCH']) 
def update_one_subject_class(subject_class_id):
# A route to update one subject_class resource (SQL: Update subjects_classes set .... where id = id)
    stmt = db.select(SubjectClass).filter_by(id=subject_class_id) # Build query
    subject_class = db.session.scalar(stmt) # Execute query

    data = SubjectClassSchema().load(request.json) # this applies the validation rules set on the schema.
    if subject_class:  # If a subject_class with that id exsists then update any provided fields  
        subject_class.id = data.get('id') or subject_class.id,
        subject_class.employee_id = data.get('employee_id') or subject_class.employee_id,
        subject_class.room = data.get('room') or subject_class.room,
        subject_class.timetable_line = data.get('timetable_line') or subject_class.timetable_line
    
        # Add and commit subject_class to DB
        db.session.add(subject_class)
        db.session.commit()
        # Respond to client
        return SubjectClassSchema().dump(subject_class), 201
    # If there is no student in a database with that provided id return a not found (404) error with a custom error message.
    else:  
        return {'error': f'Class not found with id {subject_class_id}.'}, 404

# DELETE SubjectClass
@subjects_bp.route('/classes/<string:subject_class_id>/', methods=['DELETE'])
# @jwt_required()
def delete_one_subject_class(subject_class_id):
    # authorize()
    # A route to delete one subject_class resource (SQL: Delete from subject_classes where id=subject_class_id)
    stmt = db.select(SubjectClass).filter_by(id=subject_class_id) # Build query to select the subject_class
    subject_class = db.session.scalar(stmt) # Execute query
    # if the subject_class_id exsists delete its records from the database
    if subject_class:
        db.session.delete(subject_class)
        db.session.commit()
        return {'message': f'The records for the Subject Class ID {subject_class_id} were deleted successfully'} # Respond to client
    # If the subject_class_id doesn't exist in the database return a not found (404) error
    else:
        return {'error': f'Subject Class not found with id {subject_class_id}'}, 404