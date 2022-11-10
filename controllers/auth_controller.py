# Auth will make use of the users model but indirectly. 
from flask import Blueprint, request, abort
from init import db, bcrypt
from datetime import timedelta
from models.user import User, UserSchema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# @auth_bp.route('/users/')
# def get_users():
#     stmt = db.select(User)
#     users = db.session.scalars(stmt)
#     return UserSchema(many=True, exclude=['password']).dump(users)    


# @auth_bp.route('/register/', methods=['POST'])
# def auth_register():
#     try:
#         # Create a new User model instance from the user_info
#         user = User(
#             email = request.json['email'],
#             password = bcrypt.generate_password_hash(request.json['password']).decode('utf8'),
#             first_name = request.json.get('first_name'),
#             middle_name = request.json.get('middle_name'),
#             last_name = request.json.get('middle_name')
#         )
#         # Add and commit user to DB
#         db.session.add(user)
#         db.session.commit()
#         # Respond to client
#         return UserSchema(exclude=['password']).dump(user), 201
#     except IntegrityError:
#         return {'error': 'Email address already in use'}, 409


@auth_bp.route('/login/', methods=['POST'])
def auth_login():
    # Find a user by email address
    stmt = db.select(User).filter_by(email=request.json['email']) # Build the query to select the user with the incoming email address. 
    user = db.session.scalar(stmt) # Execute the query
    # If user exists (if user is truthy) and the incoming password is correct create a JWT token and return it.
    if user and bcrypt.check_password_hash(user.password, request.json['password']):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=5)) # Timedelta is a function that allows a time period to be specified in any unit and it will calculate and return how many minutes that is. This token will expire after 5 days. # change this to one before deployment. Delta means difference.
        # The token isn't stored on the server. Instead the server uses the secret key to validate the token.
        return {'email': user.email, 'token': token, 'type': user.type} # The payload of the token identifys the user. 
    else:
        return {'error': 'Invalid email or password'}, 401 # For security reasons users are not told which one is incorrect. This prevents brute force attacks.
    
# This can be imported this into other modules and called when required. 
def authorize():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if not user.type == 'Employee':
        abort(401) # Abort will immediately terminate the request response cycle and send an error response message back to the client. 
