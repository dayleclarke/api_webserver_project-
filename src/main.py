from flask import Flask
from init import db, ma, bcrypt, jwt
from controllers.cli_controller import db_commands
from controllers.users_controller import users_bp 
from controllers.auth_controller import auth_bp 
from controllers.students_controller import students_bp 
from controllers.subjects_controller import subjects_bp 
from marshmallow.exceptions import ValidationError
import os

def create_app(): 
    app = Flask (__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JSON_SORT_KEYS']= False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

    # Each of the following errorhandler functions will change the error message returned with the specified status code. It will catch the specific error that happens (anywhere in the app) and return the error message in JSON instead of HTML. This provides consistency across the app's responses.  

    @app.errorhandler(400)
    def bad_request(err): # It automatically passes in an error object. 
        return {'error': str(err)}, 400
    
    @app.errorhandler(401)
    def unauthorized(err):
        return {'error': 'You are not authorized to perform this action'}, 401
    
    @app.errorhandler(404)
    def not_found(err): 
        return {'error': str(err)}, 404
    
    @app.errorhandler(KeyError)
    def key_error(err):
        return {'error': f'The field {err} is required.'}, 400
    
    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {'error': err.messages}, 400

    
    # create the instances of our components
    db.init_app(app) # Here I have used the init_app method and passed it the app. Init is a method of SQLAlchemy.
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # register the following blueprints:

    app.register_blueprint(db_commands)
    app.register_blueprint(users_bp)
    app.register_blueprint(students_bp)  
    app.register_blueprint(auth_bp) 
    app.register_blueprint(subjects_bp) 
    


    
    return app
