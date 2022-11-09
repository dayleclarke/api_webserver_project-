# This module contains the CRUD operations for the users model.
from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, UserSchema
from models.address import Address, AddressSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

# Adding a blueprint for users. This will automatically add the prefix users to the start of all the following URL's with this blueprint. 
users_bp = Blueprint('users', __name__, url_prefix='/users') # users is a resource made available through the API

#CREATE
# A route to create one new address and user resource at the same time. 
@users_bp.route('/', methods=['POST'])
# @jwt_required()
def create_address_and_user():
    # Create a new Address model instance (SQL: Insert into addresses (complex_number,...) values...)
    # Load applies the validation rules set on the schema. 
    data = AddressSchema().load(request.json)

    address = Address(
            complex_number = data.get('complex_number'), 
            street_number = data['street_number'], 
            street_name = data['street_name'], 
            suburb = data['suburb'], 
            postcode = data['postcode']
            )
    # Add and commit address to DB
    db.session.add(address)
    db.session.commit()
       
    # Now create a new user instance (Insert into users)

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
    # Add and commit card to DB
    db.session.add(user)
    db.session.commit()
    # Respond to client
    return UserSchema().dump(user), 201

# READ
@users_bp.route('/') 
def get_all_users():
    # A route to return all instances of the users resource in assending alphabetical order by last_name (select * from users order by last_name)
    #Build the query
    stmt = db.select(User).order_by(User.last_name)
    # Execute the query
    users = db.session.scalars(stmt)
    return UserSchema(many=True, exclude=['password']).dump(users)


@users_bp.route('/<int:id>')
# This specifies a restful parameter of id that will be an integer. It will only match if the value passed in is an integer. 
def get_one_user(id):
    # A route to retrieve a single user resource based on their id
    # (select * from users where id=<int:id)
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt) # change this to scalar singular as this is only one we are retrieving 
    if user: 
        return UserSchema(exclude=['password']).dump(user) # remove the many=True because we are only returning a single User. 
    else:
        # This is the error that will be returned if there is no user with that ID. This will return a not found 404 error.  
        return {'error': f'User not found with id {id}.'}, 404

# UPDATE
@users_bp.route('/<int:id>/', methods=['PUT', 'PATCH'])
# @jwt_required()
def update_one_user(id):
    # A route to update one user resource
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)

    data = UserSchema().load(request.json)
    
    if user:
        user.title = data.get('title') or user.title # The get method will return none if the key doesn't exist rather than raising an exception. 
        user.first_name = data.get('first_name') or user.first_name
        user.middle_name = data.get('middle_name') or user.middle_name
        user.last_name = data.get('last_name') or user.last_name
        user.password = bcrypt.generate_password_hash(data['password']).decode('utf8') or user.password
        user.email = data.get('email') or user.email
        user.phone = data.get('phone') or user.phone
        user.dob = data.get('dob') or user.dob
        user.gender = data.get('gender') or user.gender
        user.type = data.get('type') or user.type
        
        db.session.commit()      
        return UserSchema().dump(user)
    else:
        return {'error': f'User not found with user id {id}.'}, 404

# DELETE
@users_bp.route('/<int:id>/', methods=['DELETE'])
# @jwt_required()
def delete_one_user(id):
    # authorize()
    # A route to delete one user resource
    # select the card
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    # if the user's user_id exsists delete their records from the database
    if user:
        db.session.delete(user)
        db.session.commit()
        return {'message': f'The records for {user.first_name} {user.last_name} were deleted successfully.'}
    # If the user_id doesn't exist in the database return a not found (404) error
    else:
        return {'error': f'User not found with id {id}.'}, 404


create_data = {   "complex_number": 14,
    "street_number": 20,
    "street_name": "Captain Road",
    "suburb": "West End",
    "postcode": 4006,
    "users": [{
        "title": "Ms",
        "first_name": "Rachael",
        "middle_name": "Anne",
        "last_name": "Cook",
        "password": "hamAnd335*",
        "email": "test.coggfg4hhttt@bgbc.edu.au",
        "phone": "0414563531",
        "dob": "1980-09-02",
        "gender": "female",
        "type": "Student"
    }]
}

update_data = {
    "title": "Ms",
        "first_name": "Rachael",
        "middle_name": "Anne",
        "last_name": "Cook",
        "password": "hamAnd335*",
        "email": "rachael.cook@bgbc.edu.au",
        "phone": "0414563531",
        "dob": "1980-09-02",
        "gender": "female",
        "type": "Student"

}
