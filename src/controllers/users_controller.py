# This module contains the CRUD operations for the User model.
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db, bcrypt
from models.address import Address, AddressSchema
from models.user import User, UserSchema
from controllers.auth_controller import auth_admin, auth_self
from sqlalchemy.exc import IntegrityError

# Adding a blueprint for users. This will automatically add the prefix users to the start of all the following URL's with this blueprint. 
users_bp = Blueprint('users', __name__, url_prefix='/users') # users is a resource made available through the API

#CREATE
# A route to create one new address and user resource at the same time. 
@users_bp.route('/', methods=['POST'])
@jwt_required()
def create_address_and_user():
    # Create a new Address model instance (SQL: Insert into addresses (complex_number,...) values...)
    data = AddressSchema().load(request.json) # Load applies the validation rules set on the schema. 
    address = Address(
            complex_number = data.get('complex_number'), # Get allows this field to be left blank
            street_number = data['street_number'], 
            street_name = data['street_name'], 
            suburb = data['suburb'], 
            postcode = data['postcode']
            )
    # Add and commit address to DB
    db.session.add(address)
    db.session.commit()
       
    # Now create a new user instance (SQL: Insert into users (title, first_name...) values...)
    try:

        user = User(
            title = data['users'][0]['title'],
            first_name = data['users'][0]['first_name'],
            middle_name = data['users'][0]['middle_name'],
            last_name = data['users'][0]['last_name'],
            password = bcrypt.generate_password_hash(request.json['users'][0]['password']).decode('utf8'),
            email = data['users'][0]['email'],
            phone = data['users'][0]['phone'],
            dob = data['users'][0]['dob'],
            gender = data['users'][0]['gender'],
            address_id = address.id,
            type = data['users'][0]['type'] 
        )
        # Add and commit user to DB
        db.session.add(user)
        db.session.commit()
        # Respond to client
        return UserSchema().dump(user), 201
    except IntegrityError:
        return {'error': 'Email address already in use'}, 409

# READ
@users_bp.route('/')
@jwt_required() 
def get_all_users():
    auth_admin()
    # A route to return all instances of the users resource in assending alphabetical order by last_name (SQL: select * from users order by last_name)

    stmt = db.select(User).order_by(User.last_name) # Build query
    users = db.session.scalars(stmt) # Execute query
    # Respond to client
    return UserSchema(many=True, exclude= ['student_relations', 'student', 'employee']).dump(users)

@users_bp.route('/<int:id>')
@jwt_required() 
# This specifies a restful parameter of id that will be an integer. It will only match if the value passed in is an integer. 
def get_one_user(id):
    auth_self(id)
    # A route to retrieve a single user resource based on their id
    # (SQL: select * from users where id=id)
    stmt = db.select(User).filter_by(id=id) # Build query
    user = db.session.scalar(stmt) # Execute query (scalar is singular as only one user instance is returned. 
    if user: # If the id belongs to an exsiting user then return that user instance
        return UserSchema(exclude= ['student', 'employee']).dump(user) # remove the many=True because we are only returning a single User. 
    else:
        # A 404 error with a custom message will be returned if there is no user with that ID.
        return {'error': f'User not found with id {id}.'}, 404

# UPDATE
@users_bp.route('/<int:id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_user(id):
    auth_self(id)
    # A route to update one user resource (SQL: Update users set .... where id = id)
    stmt = db.select(User).filter_by(id=id) # Build query
    user = db.session.scalar(stmt) # Execute query

    data = UserSchema().load(request.json, partial=True) # this applies the validation rules set on the schema.
    
    if user: # If a user with that id exsists then update any provided fields
        user.title = data.get('title') or user.title # The get method will return none if the key doesn't exist rather than raising an exception. 
        user.first_name = data.get('first_name') or user.first_name
        user.middle_name = data.get('middle_name') or user.middle_name
        user.last_name = data.get('last_name') or user.last_name
        user.password = bcrypt.generate_password_hash(data.get('password')).decode('utf8') or user.password
        user.email = data.get('email') or user.email
        user.phone = data.get('phone') or user.phone
        user.dob = data.get('dob') or user.dob
        user.gender = data.get('gender') or user.gender
        user.type = data.get('type') or user.type
        
        db.session.commit()      
        return UserSchema().dump(user) # Respond to client
    else:# If there is no user in a database with that provided id return a not found (404) error with a custom error message.
        return {'error': f'User not found with user id {id}.'}, 404

# DELETE
@users_bp.route('/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_one_user(id):
    auth_admin()
    # A route to delete one user resource (SQL: Delete from users where id=id)
    stmt = db.select(User).filter_by(id=id) # build query to select card
    user = db.session.scalar(stmt) # execute query
    # if the user's user_id exsists delete their records from the database
    if user:
        db.session.delete(user)
        db.session.commit()
        return {'message': f'The records for {user.first_name} {user.last_name} were deleted successfully.'} # Respond to client
    # If the user_id doesn't exist in the database return a not found (404) error
    else:
        return {'error': f'User not found with id {id}.'}, 404
