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
    stmt = db.select(Teacher).filter_by(school_email=request.json['school_email'])
    teacher = db.session.scalar(stmt)
    # If user exists and password is correct
    if teacher and bcrypt.check_password_hash(teacher.password, request.json['password']):
        # return UserSchema(exclude=['password']).dump(user)
        token = create_access_token(identity=str(teacher.employee_id), expires_delta=timedelta(days=1))
        return {'email': teacher.school_email, 'token': token}
    else:
        return {'error': 'Invalid email or password'}, 401
    
# I can import this into other modules and call it whenever it is needed. 
def authorize():
    employee_id = get_jwt_identity()
    stmt = db.select(Teacher).filter_by(employee_id=employee_id)
    teacher = db.session.scalar(stmt)
    # if not user.is_admin:
    #     abort(401)
