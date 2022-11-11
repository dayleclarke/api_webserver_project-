# This module contains the CRUD operations for the Student model.
from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from init import db, bcrypt
from models.student import Student, StudentSchema
from models.student_relation import StudentRelation, StudentRelationSchema
from models.user import User, UserSchema
from controllers.auth_controller import authorize, auth_employee

# Adding a blueprint for students. This will automatically add the prefix students to the start of all URL's with this blueprint. 
students_bp = Blueprint('students', __name__, url_prefix='/students') # students is a resource made available through the API

#CREATE User and Student 
# A route to create one new student resource 
@students_bp.route('/', methods=['POST'])
@jwt_required() #Route protected by JWT but accessible by all users
def create_user_and_student():
    # Create a new student and user model instance for the new student.  
    # first create a new instance of the user based on the provided input. (SQL: Insert into users (title, first_name...) values...)
    data = UserSchema().load(request.json)
    user =  User(
        title = data['title'],
        first_name = data['first_name'],
        middle_name = data['middle_name'],
        last_name = data['last_name'],
        password = bcrypt.generate_password_hash(request.json['password']).decode('utf8'),
        email = data['email'],
        phone = data['phone'],
        dob = data['dob'],
        gender = data['gender'],
        type = data['type'] 
    )
    db.session.add(user)
    db.session.commit() # commit new user to the db
    
    # Now create a new student instance (SQL: Insert into student (homegroup, enrolment_date...) values...)
    student = Student(
        user_id = user.id,
        homegroup = data['student']['homegroup'],
        enrollment_date = data['student']['enrollment_date'],
        year_level = data['student']['year_level'],
        birth_country = data['student']['birth_country']
    )
    db.session.add(student)
    db.session.commit()
    return StudentSchema().dump(student), 201

# READ Student
@students_bp.route('/')
@jwt_required() 
def get_all_students():
    auth_employee() # only users who are employees can access this route. 

# A route to return all instances of the students resource in assending order by ID (SQL: select * from students order by id)
    stmt = db.select(Student).order_by(Student.id) # Build query
    students = db.session.scalars(stmt) # Execute query
    return StudentSchema(many=True).dump(students) # Respond to client

# This specifies a restful parameter of student_id that will be an integer. It will only match if the value passed in is an integer. 
@students_bp.route('/<int:student_id>/') # Note this is student_id not user_id
@jwt_required() 
def get_one_student(student_id):
    
    # Find the user who made the request and check they have authorisation to view that student's details
    authorize(student_id)



    # A route to retrieve a single student resource based on their student_id
    # (SQL: select * from students where id=student_id)
    stmt = db.select(Student).filter_by(id=student_id) # Build query
    student = db.session.scalar(stmt) # Execute query (scalar is singular as only one student instance is returned. 
    if student:  # If the student_id belongs to an exsiting student then return that student instance
        return StudentSchema().dump(student) # remove the many=True because we are only returning a single Student. 
    else:
        # A 404 error with a custom message will be returned if there is no student with that student_id.  
        return {'error': f'Student not found with id {student_id}.'}, 404

# UPDATE Student
@students_bp.route('/<int:student_id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_student(student_id):
    authorize_employee()
    # A route to update one student resource (SQL: Update students set .... where id = id)
    stmt = db.select(Student).filter_by(id=student_id) # Build query
    student = db.session.scalar(stmt) # Execute query
 
    data = StudentSchema().load(request.json) # this applies the validation rules set on the schema.
    
    if student: # If a student with that id exsists then update any provided fields
        student.homegroup = data.get('homegroup') or student.homegroup # The get method will return none if the key doesn't exist rather than raising an exception. 
        student.enrollment_date = data.get('enrollment_date') or student.enrollment_date
        student.year_level = data.get('year_level') or student.year_level
        student.birth_country = data.get('birth_country') or student.birth_country

        db.session.commit() # commit all changes to db      
        return StudentSchema().dump(student) # Respond to client
    else:# If there is no student in a database with that provided id return a not found (404) error with a custom error message.
        return {'error': f'Student not found with student ID{student_id}.'}, 404

# DELETE Student
@students_bp.route('/<int:student_id>/', methods=['DELETE'])
# @jwt_required()
def delete_one_student(student_id):
    # authorize()
    # A route to delete one student resource (SQL: Delete from students where id=student_id)
    stmt = db.select(Student).filter_by(id=student_id) # Build query to select the student
    student = db.session.scalar(stmt) # Execute query
    # if the user's student_id exsists delete their records from the database
    if student:
        db.session.delete(student)
        db.session.commit()
        return {'message': f'The records for the student with Student ID{student.id} were deleted successfully'} # Respond to client
    # If the student_id doesn't exist in the database return a not found (404) error
    else:
        return {'error': f'Student not found with id {student_id}'}, 404



{   "title": "Ms",
    "first_name": "Rachael",
    "middle_name": "Anne",
    "last_name": "Cook",
    "password": "hamAnd335*",
    "email": "test.coggfg4ttt@bgbc.edu.au",
    "phone": "0414563531",
    "dob": "1980-09-02",
    "gender": "female",
    "type": "Student",
    "address": {
            "complex_number": 14,
            "street_number": 20,
            "street_name": "Captain Road",
            "suburb": "West End",
            "postcode": 4006
    },
    "student": {
            "homegroup": "WH01",
            "enrollment_date": "2020-01-01",
            "year_level": 9,
            "birth_country": "Australia"
        }
}

# The following CRUD routes relate to the Student_Relations Model. This will be used to record the relationships between students and their caregivers. (the join table connecting these tables)  

#CREATE Student Relation
# A route to create one new student_relations resource.  
@students_bp.route('/relations', methods=['POST'])
# @jwt_required()
def create_student_relations():  
    # Create a new instance of the student_relation based on the provided input. (SQL: Insert into student_relations (relationship_to_student...) values...)
    data = StudentRelationSchema().load(request.json) 
    student_relation =  StudentRelation(       
        relationship_to_student = data['relationship_to_student'],
        is_primary_contact = data['is_primary_contact'],
        user_id = data['user_id'],
        student_id = data['student_id']
    )
    db.session.add(student_relation)
    db.session.commit() # commit new relationship to the db
    
    return StudentRelationSchema().dump(student_relation), 201 # Respond to client

# READ Student Relations 
@students_bp.route('/relations/') 
def get_all_student_relations():
# A route to return all student_caregiver relationships recorded in assending order by student_id (SQL: select * from student_relations order by student_id)
    stmt = db.select(StudentRelation).order_by(StudentRelation.student_id) # Build query
    student_relations = db.session.scalars(stmt) # Execute query
    return StudentRelationSchema(many=True).dump(student_relations) # Respond to client

# This specifies a restful parameter of student_id that will be an integer. It will only match if the value passed in is an integer. 
@students_bp.route('/relations/<int:student_relation_id>/') 
def get_one_student_relation(student_relation_id):
    # A route to retrieve a single student_relation resource based on their student_relation_id
    # (SQL: select * from students_relations where id=student_relation_id)
    stmt = db.select(StudentRelation).filter_by(id=student_relation_id) # Build query
    student = db.session.scalar(stmt) # Execute query (scalar is singular as only one student_relation instance is returned. 
    if student:  # If the student_relations_id belongs to an exsiting student-caregiver relationship then return that instance
        return StudentRelationSchema().dump(student) # remove the many=True because we are only returning a single student_relation. 
    else:
        # A 404 error with a custom message will be returned if there is no student_relation with that id.  
        return {'error': f'A record of the student-caregiver relationship with id {student_relation_id} was not found.'}, 404

# UPDATE
@students_bp.route('/relations/<int:student_relation_id>/', methods=['PUT', 'PATCH'])
# @jwt_required()
def update_one_student_relation(student_relation_id):
    # A route to update a single student_relation resource based on their student_relation_id (SQL: Update student_relations set .... where id = id)
    stmt = db.select(StudentRelation).filter_by(id=student_relation_id) # Build query
    student_relation = db.session.scalar(stmt) # Execute query
 
    data = StudentRelationSchema().load(request.json) # this applies the validation rules set on the schema.
    
    if student_relation: # If a student with that id exsists then update any provided fields
        student_relation.relationship_to_student = data.get('relationship_to_student') or student_relation.relationship_to_student # The get method will return none if the key doesn't exist rather than raising an exception. 
        student_relation.is_primary_contact = data.get('is_primary_contact') 
        student_relation.user_id = data.get('user_id') or student_relation.user_id
        student_relation.student_id = data.get('student_id') or student_relation.student_id

        db.session.commit() # commit all changes to db      
        return StudentRelationSchema().dump(student_relation) # Respond to client
    else:# If there is no student in a database with that provided id return a not found (404) error with a custom error message.
        return {'error': f'A record of the student-caregiver relationship with id {student_relation_id} was not found.'}, 404

# DELETE Student_Relation
@students_bp.route('/relations/<int:student_relation_id>/', methods=['DELETE'])
# @jwt_required()
def delete_one_student_relation(student_relation_id):
    # authorize()
    # A route to delete a single student_relation resource based on their student_relation_id (SQL: Delete from student_relations where id=student_relations_id)
    stmt = db.select(StudentRelation).filter_by(id=student_relation_id) # Build query to select the student/caregiver relationship to delete
    student_relation = db.session.scalar(stmt) # Execute query
    # if the user's student_relation_id exsists delete the record from the database
    if student_relation:
        db.session.delete(student_relation)
        db.session.commit()
        return {'message': f'The record of the Student-{student_relation.relationship_to_student} relationship with student_relation_id {student_relation_id} was successfully deleted'} # Respond to client
    # If the student_relation_id doesn't exist in the database return a not found (404) error
    else:
        return {'error': f'A record of the student-caregiver relationship with id {student_relation_id} was not found.'}, 404

test_student_relation = {   
    "relationship_to_student": "Mother",
    "is_primary_contact": True,
    "user_id": 1,
    "student_id": 2

}
        
