from flask import Blueprint
from init import db, bcrypt
from datetime import date
from models.user import User
from models.student import Student
from models.subject_class import SubjectClass
from models.enrollments import Enrollment
from models.subject import Subject

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
            # middle_name = 'Jane',
            last_name = 'Clark',
            password=bcrypt.generate_password_hash('ExamplePassword').decode('utf-8'),
            email = 'danielle.clark@bgbc.edu.au',
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
            email = 'damion.burns@bgbc.edu.au',
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
            email = 'Isabelle.Smith@bgbc.edu.au',
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
            email = 'gabriella.jones@bgbc.edu.au',
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
            user = users[3]
        )
    ]
    db.session.add_all(students)
    db.session.commit()
    subjects = [
        Subject(
            id = '09EE',
            name = 'Enterprise Education',
            year_level = 9,
            max_students = 28,
            department = 'Business'

        ),
        Subject(
            id = '09MAB',
            name = 'Maths Beta',
            year_level = 9,
            max_students = 25,
            department = 'Maths'
        ),
        Subject(
            id = '09ENG',
            name = 'Junior English',
            year_level = 9,
            max_students = 28,
            department = 'English'
        )
    ]    
    db.session.add_all(subjects)
    db.session.commit()
    subject_classes = [
        SubjectClass(
            id = '09EE01-2023',
            employee_id = 1,
            room = 'MB2.2',
            timetable_line = 2,  
            subject_id = '09EE'
        ),
        SubjectClass(
            id = '09EE02-2023',
            employee_id = 2,
            room = 'MB2.4',
            timetable_line = 1,  
            subject_id = '09EE'
        ),
        SubjectClass(
            id = '09MAB01-2023',
            employee_id = 3,
            room = 'SA1.4',
            timetable_line = 3,  
            subject_id = '09MAB'
        ),
        SubjectClass(
            id = '09ENG05-2023',
            employee_id = 4,
            room = 'SA4.4',
            timetable_line = 4,  
            subject_id = '09ENG'
        )
    ]    
    db.session.add_all(subject_classes)
    db.session.commit()

    enrollments = [
        Enrollment(
            date = '01-01-2023',
            subject_class = subject_classes[0],
            student = students[0]
        ),
        Enrollment(
            date = '01-01-2023',
            subject_class = subject_classes[0],
            student = students[1]
        ),
        Enrollment(
            date = '01-01-2023',
            subject_class = subject_classes[2],
            student = students[0]
        ),
        Enrollment(
            date = '01-01-2023',
            subject_class = subject_classes[2],
            student = students[1]
        ),
    ]
    
    db.session.add_all(subject_classes)
    db.session.commit()
 
    

    print('Tables seeded')
