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
    
    # create the instances of our components
    db.init_app(app) # Here I have used the init_app method and passed it the app. Init is a method of SQLAlchemy.
    ma.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(db_commands)
    app.register_blueprint(teachers_bp) 

    
    # app.register_blueprint(cards_bp) 

    
    return app
