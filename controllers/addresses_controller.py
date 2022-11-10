# This module contains the CRUD operations for the Address model.
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db, bcrypt
from models.address import Address, AddressSchema

# Adding a blueprint for addresses. This will automatically add the prefix addresses to the
# start of all URL's with this blueprint. 
addresses_bp = Blueprint('addresses', __name__, url_prefix='/addresses') # addresses is a resource made available through the API

#CREATE

# Routes are declared with a decorator on the app
@addresses_bp.route('/', methods=['POST'])
# @jwt_required()
# A function is defined that the decorator applies to (the route handler).
def create_address(): 
    # Create a new Address model instance (SQL: Insert into addresses (complete_number, strret_number...) values...)
    data = AddressSchema().load(request.json)  # this applies the validation rules set on the schema.
    address = Address(
            complex_number = data.get('complex_number'),  # Get allows this field to be left blank
            street_number = data['street_number'], 
            street_name = data['street_name'], 
            suburb = data['suburb'], 
            postcode = data['postcode']
            )
    # Add and commit address to DB
    db.session.add(address)
    db.session.commit()
    #  The following return statement will be the response the server sends across the network to the client:  
    return AddressSchema().dump(address), 201 # The result is automatically Jsonified.

# READ
@addresses_bp.route('/') 
def get_all_addresses():
    # A route to return all instances of the addresses resource in ascending order by postcode (select * from addresses order by postcode)
    stmt = db.select(Address).order_by(Address.postcode) # Build the query
    addresses = db.session.scalars(stmt) # Execute the query
    return AddressSchema(many=True).dump(addresses) # Respond to client


@addresses_bp.route('/<int:id>')
# This specifies a restful parameter of id that will be an integer. It will only match if the value passed in is an integer. 
def get_one_address(id):
    # A route to retrieve a single user resource based on the restful id parameter.
     # (select * from subjects where id=id)
    # Build the query
    stmt = db.select(Address).filter_by(id=id) # stmt is short for statement
    # Execute the query
    user = db.session.scalar(stmt) # Scalar is now singular as only one Address is returned 
    if user: # If the id belongs to an exsiting address then return that address instance
        return AddressSchema().dump(user) # remove the many=True because we are only returning a single Address instance. 
    else:
        # A 404 error with a custom message will be returned if there is no address with that ID. 
        return {'error': f'Address not found with id {id}.'}, 404

# UPDATE
@addresses_bp.route('/<int:id>/', methods=['PUT', 'PATCH'])
# @jwt_required()
def update_one_address(id):
    # A route to update one address resource (SQL: Update addresses set .... where id = id)
    stmt = db.select(Address).filter_by(id=id) # Build the query
    address = db.session.scalar(stmt) # Execute the query
    data = AddressSchema().load(request.json) # this applies the validation rules set on the schema.
    if address:  # If an address with that id exsists then update any provided fields
        address.complex_number = data.get('complex_number') or address.complex_number # The get method will return none if the key doesn't exist rather than raising an exception. 
        address.street_number = data.get('street_number') or address.street_number
        address.street_name = data.get('street_name') or address.street_name
        address.suburb = data.get('suburb') or address.suburb
        address.postcode = data.get('postcode') or address.postcode
        
        db.session.commit()      
        return AddressSchema().dump(address) # Respond to client
    else: # If there is no address in a database with that provided id return a not found (404) error with a custom error message. 
        return {'error': f'Address not found with id {id}.'}, 404

# DELETE
@addresses_bp.route('/<int:id>/', methods=['DELETE'])
# @jwt_required()
def delete_one_address(id):
    # authorize()
    # A route to delete one address resource (SQL: Delete from addresses where id=id)
    stmt = db.select(Address).filter_by(id=id) # Build query 
    address = db.session.scalar(stmt) # Execute query
    #  If an address with that id exsists then delete the entire instance of that address
    if address: 
        db.session.delete(address)
        db.session.commit()
        return {'message': f'The records for address ID {address.id} located on {address.street_name} in {address.suburb} were deleted successfully.'}
    # If the address_id doesn't exist in the database return a not found (404) error
    else:
        return {'error': f'Address not found with id {id}.'}, 404



test_data= {
        "complex_number": 14,
        "street_number": 20,
        "street_name": "Captain Road",
        "suburb": "West End",
        "postcode": 4006
    }