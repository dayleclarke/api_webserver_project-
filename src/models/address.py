from init import db, ma # Imports start at the root folder. 
from marshmallow import fields, validates
from models.user import User, UserSchema
from marshmallow.exceptions import ValidationError
from datetime import date
from marshmallow.validate import Length, Regexp, Range

class Address(db.Model):
    __tablename__ = 'addresses' # Renames the table to be plural

    id = db.Column(db.Integer, primary_key=True) 
    complex_number = db.Column(db.Integer, default= None) # make sure it's possible for them to be able to leave this blank in the JSON body as many addresses do not contain a complex_number
    street_number = db.Column(db.Integer, nullable= False)
    street_name = db.Column(db.String(128), nullable= False)
    suburb = db.Column(db.String(128), nullable= False)
    postcode = db.Column(db.Integer, nullable= False) 
    # Overseas addresses are not permitted in this system. This may be updated in future sprints which would involve changing this to a string to allow letters/country codes. Then another table would be required to indicate the country each postcode relates to. 
    # States are also not recorded in the database. That could also be added (requiring an additional table) in a future sprint. 

    users = db.relationship('User', back_populates='address')     # This will provide a list of all the users who live at this address. Now address.cards can be used to return a python list of all the users at that address. Each element in the list will be a user object (an instance of the user model).
    # relationship() will take a number of parameters. The first parameter indicates which other model (class name) it relates to as a string. User will encapsulate data that's in the User model.  
#back_populates adds a propery to User called address so that if I want to get the whole address object for a user I can say user.address. 
# 
#Here casacade delete was not set because if an address is deleted we don't want any users who have that address listed to be deleted too. By leaving this parameter out it will de-associate each user from the address by setting their foreign key reference to NULL. 
 

# Using a mapping as follows: 
# select from dbo.Address where id = 1 => AND select from dbo.buildings where id == address.building_id
# address = {
#     id = 1
#     cn = 1
#     str_num = 2
#     sub = "foo"
#     building_id = 123
#     buidling = {
#         id = 2
#         landlord = "john"
#     }
# }
# send_letter(address)
# def send_letter(building):
#     "to {BUILDING_LANDLORD} - {NUM} {STREET} {SUBURB}"
#     pass

class AddressSchema(ma.Schema):
    # This allows the models to be serialized and deserialized to and from JSON.    
    # Validations
    complex_number = fields.Integer(load_defalt=None)
    street_number = fields.Integer(required=True)
    street_name = fields.String(required=True, validate=
        Length(min=2, error='Street name must be at least 2 characters long'))
    suburb = fields.String(required=True, validate=
        Length(min=2, error='Suburb name must be at least 2 characters long'))
    postcode = fields.Integer(required=True, validate=Range(min=200, max=9999)) # smallest Australian postcode is 200 (in the ACT) and the largest is 9999 (in QLD)
    users = fields.List(fields.Nested('UserSchema', exclude=['address','student_relations', 'student', 'employee'] ))
 
    
    class Meta:
        fields = ('id','complex_number', 'street_number', 'street_name', 'suburb', 'postcode', 'users')
        ordered = True # puts the keys in the same order as the fields lists above otherwise it will be alphabetical order.

# only = ['id', 'first_name', 'last_name', 'type']