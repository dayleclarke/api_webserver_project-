from flask import Flask
from init import db, ma, bcrypt
from controllers.cli_controller import db_commands
from controllers.teachers_controller import teachers_bp 

# from controllers.cards_controller import cards_bp # this will import the cards blueprint. 
import os


def create_app(): 
    app = Flask (__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JSON_SORT_KEYS']= False

    # This will change the error message returned with a 404 status code. It will catch any 404 that happens and return the error message in JSON instead of HTML. 
    @app.errorhandler(404)
    def not_found(err): # It automatically passes in an error object. 
        return {'error': str(err)}, 404

    
    # create the instances of our components
    db.init_app(app) # Here I have used the init_app method and passed it the app. Init is a method of SQLAlchemy.
    ma.init_app(app)
    bcrypt.init_app(app)

    # register the following blueprints:

    app.register_blueprint(db_commands)
    app.register_blueprint(teachers_bp) 


    
    return app
