# This module contains the CRUD operations for the users model.
from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, UserSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

# Adding a blueprint for users. This will automatically add the prefix users to the
# start of all URL's with this blueprint. 
users_bp = Blueprint('users', __name__, url_prefix='/users') # users is a resource made available through the API

#CREATE
# A route to create one new user resource 
@users_bp.route('/', methods=['POST'])
# @jwt_required()
def create_user():
    # Create a new Teacher model instance
    data = UserSchema().load(request.json)

    user = User(
        title = data['title'],
        first_name = data['first_name'],
        middle_name = data['middle_name'],
        last_name = data['last_name'],
        password = bcrypt.generate_password_hash(request.json['password']).decode('utf8'),
        school_email = data['school_email'],
        personal_email = data['personal_email'],
        phone = data['phone'],
        dob = data['dob'],
        gender = data['gender'],
        type = data['type'] 
    )
    # Add and commit card to DB
    db.session.add(user)
    db.session.commit()
    # Respond to client
    return UserSchema().dump(user), 201

# READ
@users_bp.route('/') # because of the url prefix the blueprint will automatically make this /cards/
#This attaches the route to the blueprint
def get_all_users():
    # A route to return all instances of the users resource in assending alphabetical order by last_name (select * from users)
    #Build the query
    stmt = db.select(User).order_by(User.last_name)
    # Execute the query
    users = db.session.scalars(stmt)
    return UserSchema(many=True, exclude=['password']).dump(users)


@users_bp.route('/<int:id>/')
# This specifies a restful parameter of id that will be an integer. It will only match if the value passed in is an integer. 
def get_one_user(id):
    # A route to retrieve a single user resource based on their id
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt) # change this to scalar singular as this is only one we are retrieving 
    if user: 
        return UserSchema(exclude=['password']).dump(user) # remove the many=True because we are only returning a single Card. 
    else:
        # This is the error that will be returned if there is no employee with that ID.
        #  This will return a not found 404 error.  
        return {'error': f'User not found with id {id}.'}, 404

# UPDATE
@users_bp.route('/<int:id>/', methods=['PUT', 'PATCH'])
# @jwt_required()
def update_one_user(id):
    # A route to update one user resource
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    if user:
        user.title = request.json.get('title') or user.title # The get method will return none if the key doesn't exist rather than raising an exception. 
        user.first_name = request.json.get('first_name') or user.first_name
        user.middle_name = request.json.get('middle_name') or user.middle_name
        user.last_name = request.json.get('last_name') or user.last_name
        user.password = bcrypt.generate_password_hash(request.json['password']).decode('utf8') or user.password
        user.school_email = request.json.get('school_email') or user.school_email
        user.personal_email =request.json.get('personal_email') or user.personal_email
        user.phone = request.json.get('phone') or user.phone
        user.dob = request.json.get('dob') or user.dob
        user.gender = request.json.get('gender') or user.gender
        user.type = request.json.get('type') or user.type
        
        db.session.commit()      
        return UserSchema().dump(user)
    else:
        return {'error': f'User not found with id {id}.'}, 404

# DELETE
@users_bp.route('/<int:id>/', methods=['DELETE'])
# @jwt_required()
def delete_one_user(id):
    # authorize()
    # A route to delete one user resource
    # select the card
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    # if the user's employee_id exsists delete their records from the database
    if user:
        db.session.delete(user)
        db.session.commit()
        return {'message': f'The records for {user.first_name} {user.last_name} were deleted successfully.'}
    # If the employee_id doesn't exist in the database return a not found (404) error
    else:
        return {'error': f'User not found with id {id}.'}, 404