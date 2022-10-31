# Auth will make use of the teachers model but indirectly. 
from flask import Blueprint, request, abort
from init import db, bcrypt
from datetime import timedelta
from models.teacher import Teacher, TeacherSchema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/teachers/')
def get_teachers():
    stmt = db.select(Teacher)
    users = db.session.scalars(stmt)
    return TeacherSchema(many=True, exclude=['password']).dump(users)    


@auth_bp.route('/register/', methods=['POST'])
def auth_register():
    try:
        # Create a new User model instance from the user_info
        teacher = Teacher(
            school_email = request.json['school_email'],
            password = bcrypt.generate_password_hash(request.json['password']).decode('utf8'),
            first_name = request.json.get('first_name'),
            middle_name = request.json.get('middle_name'),
            last_name = request.json.get('middle_name')
        )
        # Add and commit user to DB
        db.session.add(teacher)
        db.session.commit()
        # Respond to client
        return TeacherSchema(exclude=['password']).dump(teacher), 201
    except IntegrityError:
        return {'error': 'Email address already in use'}, 409


@auth_bp.route('/login/', methods=['POST'])
def auth_login():
    # Find a user by email address
    stmt = db.select(Teacher).filter_by(email=request.json['email'])
    user = db.session.scalar(stmt)
    # If user exists and password is correct
    if user and bcrypt.check_password_hash(user.password, request.json['password']):
        # return UserSchema(exclude=['password']).dump(user)
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        return {'email': user.email, 'token': token, 'is_admin': user.is_admin}
    else:
        return {'error': 'Invalid email or password'}, 401
    

def authorize():
    user_id = get_jwt_identity()
    stmt = db.select(Teacher).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if not user.is_admin:
        abort(401)
