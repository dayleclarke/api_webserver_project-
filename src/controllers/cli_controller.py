from flask import Blueprint
from init import db, bcrypt
from datetime import date
from models.teacher import Teacher

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print("Tables created")

@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command('seed')
def seed_db():
    teachers = [
        Teacher(
            title = 'Miss',
            first_name = 'Danielle',
            middle_name = 'Jane',
            last_name = 'Clark',
            school_email = 'danielle.clark@bgbc.edu.au',
            personal_email = 'danielle.clark08@gmail.com',
            phone = '0416393531',
            employment_status = 'permanent full-time',
            pay_scale = 'B2S1',
            gender = 'female',
            password=bcrypt.generate_password_hash('ExamplePassword').decode('utf-8')
        ),
        Teacher(
            title = 'Mr',
            first_name = 'Damion',
            middle_name = 'George',
            last_name = 'Burns',
            school_email = 'damion.burns@bgbc.edu.au',
            personal_email = 'damion.burns7@gmail.com',
            phone = '0405301451',
            employment_status = 'permanent full-time',
            pay_scale = 'B2S2',
            gender = 'male',
            password=bcrypt.generate_password_hash('ChangeMe').decode('utf-8')
        )
    ]

    db.session.add_all(teachers)
    db.session.commit()

    print('Tables seeded')
