# This module contains the CRUD operations for the Address model.
from flask import Blueprint, request
from init import db, bcrypt
from models.address import Address, AddressSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

# Adding a blueprint for addresses. This will automatically add the prefix users to the
# start of all URL's with this blueprint. 
addresses_bp = Blueprint('addresses', __name__, url_prefix='/addresses') # addresses is a resource made available through the API

#CREATE
# A route to create one new address resource 
@addresses_bp.route('/', methods=['POST'])
# @jwt_required()
def create_address():
    # Create a new Teacher model instance
    # load applies the validation rules set on the schema. 
    data = AddressSchema().load(request.json)

    address = Address(
            complex_number = data['complex_number'], 
            street_number = data['street_number'], 
            street_name = data['street_name'], 
            suburb = data['suburb'], 
            postcode = data['postcode']
            )
    # Add and commit card to DB
    db.session.add(address)
    db.session.commit()
    # Respond to client
    return AddressSchema().dump(address), 201

# READ
@addresses_bp.route('/') # because of the url prefix the blueprint will automatically make this /cards/
#This attaches the route to the blueprint
def get_all_addresses():
    # A route to return all instances of the users resource in assending alphabetical order by last_name (select * from users)
    #Build the query
    stmt = db.select(Address)
    # Execute the query
    addresses = db.session.scalars(stmt)
    return AddressSchema(many=True).dump(addresses)


@addresses_bp.route('/<int:id>')
# This specifies a restful parameter of id that will be an integer. It will only match if the value passed in is an integer. 
def get_one_address(id):
    # A route to retrieve a single user resource based on their id
    stmt = db.select(Address).filter_by(id=id)
    user = db.session.scalar(stmt) # change this to scalar singular as this is only one we are retrieving 
    if user: 
        return AddressSchema().dump(user) # remove the many=True because we are only returning a single Card. 
    else:
        # This is the error that will be returned if there is no employee with that ID.
        #  This will return a not found 404 error.  
        return {'error': f'Address not found with id {id}.'}, 404

# UPDATE
@addresses_bp.route('/<int:id>/', methods=['PUT', 'PATCH'])
# @jwt_required()
def update_one_address(id):
    # A route to update one address resource
    stmt = db.select(Address).filter_by(id=id)
    address = db.session.scalar(stmt)

    data = AddressSchema().load(request.json)
    if address:
        address.complex_number = data.get('complex_number') or address.complex_number # The get method will return none if the key doesn't exist rather than raising an exception. 
        address.street_number = data.get('street_number') or address.street_number
        address.street_name = data.get('street_name') or address.street_name
        address.suburb = data.get('suburb') or address.suburb
        address.postcode = data.get('postcode') or address.postcode
        
        db.session.commit()      
        return AddressSchema().dump(address)
    else:
        return {'error': f'Address not found with id {id}.'}, 404

# DELETE
@addresses_bp.route('/<int:id>/', methods=['DELETE'])
# @jwt_required()
def delete_one_address(id):
    # authorize()
    # A route to delete one address resource
    # select the address
    stmt = db.select(Address).filter_by(id=id)
    address = db.session.scalar(stmt)
    # if the user's employee_id exsists delete their records from the database
    if address:
        db.session.delete(address)
        db.session.commit()
        return {'message': f'The records for address ID {address.id} located on {address.street_name}, {address.suburb} were deleted successfully.'}
    # If the employee_id doesn't exist in the database return a not found (404) error
    else:
        return {'error': f'Address not found with id {id}.'}, 404



test_data= {
        "complex_number": 14,
        "street_number": 20,
        "street_name": "Captain Road",
        "suburb": "West End",
        "postcode": 4006
    }