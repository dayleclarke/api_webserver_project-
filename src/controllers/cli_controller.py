from flask import Blueprint
from init import db, bcrypt
from datetime import date
from models.user import User
from models.student import Student
from models.subject_class import SubjectClass

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
    users = [
        User(
            title = 'Miss',
            first_name = 'Danielle',
            middle_name = 'Jane',
            last_name = 'Clark',
            password=bcrypt.generate_password_hash('ExamplePassword').decode('utf-8'),
            school_email = 'danielle.clark@bgbc.edu.au',
            personal_email = 'danielle.clark08@gmail.com',
            phone = '0416393531',
            dob = '1987-12-07',
            gender = 'female',
            type = 'teacher'            
        ),
        User(
            title = 'Mr',
            first_name = 'Damion',
            middle_name = 'George',
            last_name = 'Burns',
            password=bcrypt.generate_password_hash('ChangeMe').decode('utf-8'),
            school_email = 'damion.burns@bgbc.edu.au',
            personal_email = 'damion.burns7@gmail.com',
            phone = '0405301451',
            dob = '1985-04-07',
            gender = 'male',
            type = 'teacher'
        ),
        User(
            title = 'Miss',
            first_name = 'Isabelle',
            middle_name = 'Margaret',
            last_name = 'Smith',
            password=bcrypt.generate_password_hash('ChangeMe').decode('utf-8'),
            school_email = 'Isabelle.Smith@bgbc.edu.au',
            personal_email = 'issysmith1@gmail.com',
            phone = '0405301444',
            dob = '2004-04-07',
            gender = 'female',
            type = 'student'
        ),
        User(
            title = 'Miss',
            first_name = 'Gabriella',
            middle_name = 'Sasha',
            last_name = 'Jones',
            password=bcrypt.generate_password_hash('ChangeMe').decode('utf-8'),
            school_email = 'gabriella.jones@bgbc.edu.au',
            personal_email = 'gabbyjonesy@hotmail.com',
            phone = '0408301554',
            dob = '2005-04-07',
            gender = 'female',
            type = 'student'
        )
    ]
    db.session.add_all(users)
    db.session.commit()

    students = [        
        Student(
            homegroup = 'WH01',
            enrollment_date = '2020-01-01',
            year_level = 9,
            birth_country = 'Australia',
            user = users[2]
        ),
        Student(
            homegroup = 'WH05',
            enrollment_date = '2021-01-01',
            year_level = 9,
            birth_country = 'Australia',
            user = users[2]
        )
    ]
    db.session.add_all(students)
    db.session.commit()
    
    subject_classes = [
        SubjectClass(
            class_id = '09EE01-2023',
            employee_id = 1,
            room = 'MB2.2',
            timetable_line = 2,  
            subject_id = '09EE'
        ),
        SubjectClass(
            class_id = '09EE02-2023',
            employee_id = 2,
            room = 'MB2.4',
            timetable_line = 1,  
            subject_id = '09EE'
        )
    ]
    
    db.session.add_all(subject_classes)
    db.session.commit()
 
    

    print('Tables seeded')
