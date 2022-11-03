# This module contains the CRUD operations for the users model.
from flask import Blueprint, request
from init import db, bcrypt
from models.subject_class import SubjectClass, SubjectClassSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

# Adding a blueprint for users. This will automatically add the prefix users to the
# start of all URL's with this blueprint. 
subjects_bp = Blueprint('subjects', __name__, url_prefix='/subjects') # users is a resource made available through the API

#CREATE
# A route to create one new subject_class
@subjects_bp.route('/', methods=['POST'])
# @jwt_required()
def create_subject_class():
    # Create a new Teacher model instance
    data = SubjectClass().load(request.json)

    subject_class = SubjectClass(
        id = data['id'],
        employee_id = data['empoyee_id'],
        room = data['room'],
        timetable_line = data['timetable_line'],
        subject_id = data['subject_id']
    )
    # Add and commit card to DB
    db.session.add(subject_class)
    db.session.commit()
    # Respond to client
    return SubjectClassSchema().dump(subject_class), 201

# READ
@subjects_bp.route('/') # because of the url prefix the blueprint will automatically make this /cards/
#This attaches the route to the blueprint
def get_all_subject_classes():
    # A route to return all instances of the users resource in assending alphabetical order by last_name
    stmt = db.select(SubjectClass)
    subject_classes = db.session.scalars(stmt)
    return SubjectClassSchema(many=True).dump(subject_classes)

# This specifies a restful parameter of employee_id that will be an integer. It will only match if the value passed in is an integer. 
@subjects_bp.route('/<int:id>/')
def get_one_user(id):
    # A route to retrieve a single user resource based on their employee_id
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt) # change this to scalar singular as this is only one we are retrieving 
    if user:
        return UserSchema().dump(user) # remove the many=True because we are only returning a single Card. 
    else:
        # This is the error that will be returned if there is no employee with that ID.
        #  This will return a not found 404 error.  
        return {'error': f'User not found with id {id}.'}, 404