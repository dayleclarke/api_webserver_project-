from flask import Blueprint
from init import db
from models.teacher import Teacher, TeacherSchema

teachers_bp = Blueprint('teachers', __name__, url_prefix='/teachers')

@teachers_bp.route('/') # because of the url prefix the blueprint will automatically make this /cards/
#This attaches the route to the blueprint
# A route to return a list of all the cards
def get_all_teachers():
    stmt = db.select(Teacher).order_by(Teacher.last_name.desc())
    cards = db.session.scalars(stmt)
    return TeacherSchema(many=True).dump(cards)


@teachers_bp.route('/<int:id>/')
# A route to retrieve a single teacher based on their employee_id
def get_one_card(employee_id):
    stmt = db.select(Teacher).filter_by(employee_id=employee_id)
    card = db.session.scalar(stmt) # change this to scalar singular as this is only one we are retrieving 
    if card:
        return TeacherSchema().dump(card) # remove the many=True because we are only returning a single Card. 
    else:
        return {'error': f'Teacher not found with employee_id {employee_id}'}, 404