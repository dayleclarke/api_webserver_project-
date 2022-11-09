from flask import Blueprint, request
from init import db, bcrypt
from models.enrollment import Enrollment, EnrollmentSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

# Create enrollments blueprint
enrollments_bp = Blueprint('enrollments', __name__, url_prefix='/enrollments') 

#CREATE New Enrollment
# A route to create one new enrollment
@enrollments_bp.route('/', methods=['POST'])
# @jwt_required()
def create_enrollment():
    # Create a new enrollment model instance
    # This allows the user's JSON input to be passed through the Schema to apply validation. 
    data = EnrollmentSchema().load(request.json)

    enrollment = Enrollment(
        date = data['date'],
        subject_class_id = data['subject_class_id'],
        student_id = data['student_id']
    )
    # Add and commit enrollment to DB
    db.session.add(enrollment)
    db.session.commit()
    # Respond to client
    return EnrollmentSchema().dump(enrollment), 201

# READ Enrollment
@enrollments_bp.route('/') 
def get_all_enrollments():
    # A route to return all instances of the enrollments resource in assending order by subject_class_id 
    # (select * from enrollments order by subject_class_id;)
    
    stmt = db.select(Enrollment).order_by(Enrollment.subject_class_id) # Build query
    enrollments = db.session.scalars(stmt) # Execute the query
    # Return the results to the user in JSON format
    return EnrollmentSchema(many=True).dump(enrollments)


@enrollments_bp.route('/<int:id>/') 
def get_one_enrollment(id):
    # A route to return one instance of a enrollment based on the enrollment id. 
    # (select * from enrollments where id = id;)
    #Make the query
    stmt = db.select(Enrollment).filter_by(id=id) # Build query
    enrollment = db.session.scalar(stmt) # Execute query
    # If an enrollment exists with the specified id return the resource in JSON format
    if enrollment:    
        return EnrollmentSchema().dump(enrollment)
    else:
        # A 404 error with a custom message will be returned if there is no enrolment with that id.    
        return {'error': f'Enrolment not found with id {id}.'}, 404

# UPDATE Enrollment
@enrollments_bp.route('/<int:id>/', methods=['PUT', 'PATCH'])
# @jwt_required()
def update_one_enrollment(id):
    # A route to update one enrollment resource (SQL: Update enrollments set .... where id = id)
    # Select the correct enrollement resource through a query
    stmt = db.select(Enrollment).filter_by(id=id) # Build  query
    enrollment = db.session.scalar(stmt) # Execute query
    # If an enrollment exists with the specified id update the resource attributes to match those provided in the JSON body. If a field is not provided leave it as it was before.
    data = EnrollmentSchema().load(request.json) # This allows the user's JSON input to be passed through the Schema to apply validation.
    if enrollment: 
        enrollment.id = data.get('id') or enrollment.id 
        enrollment.date = data.get('date') or enrollment.date
        enrollment.subject_class_id = data.get('subject_class_id') or enrollment.subject_class_id
        enrollment.student_id = data.get('student_id') or enrollment.student_id   

        db.session.commit() # Commit update      
        return EnrollmentSchema().dump(enrollment)
    else:
    # A 404 error with a custom message will be returned if there is no enrolment with that id. 
        return {'error': f'Enrolment not found with enrolment_id {id}.'}, 404

# DELETE Enrollment
@enrollments_bp.route('/<int:id>/', methods=['DELETE'])
# @jwt_required()
def delete_one_enrollment(id):
    # A route to delete one enrollment resource
    #(Delete from enrollments where id = id;)
    #Select the correct enrollement resource through a query
    stmt = db.select(Enrollment).filter_by(id=id)
    enrollment = db.session.scalar(stmt)# Execute query
     # If an enrollment exists with the specified id delete the enrollment and return a message in JSON stating the deletion was successul. 
    if enrollment:
        db.session.delete(enrollment)
        db.session.commit()
        return {'message': f'The student with student_id {enrollment.student_id} was unenrolled from {enrollment.subject_class_id} successfully.'}
    # If the resource doesn't exist return a 404 with a descriptive error message. 
    else:
        return {'error': f'Enrollment not found with enrollment_id {id}.'}, 404

test_enrollment = {
    "date": "2023-01-01",
    "subject_class_id": "09EE01-2023",
    "student_id": 1
}
        