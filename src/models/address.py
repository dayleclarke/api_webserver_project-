from init import db, ma # Imports start at the root folder. 
from marshmallow import fields, validates
from models.user import User, UserSchema
from marshmallow.exceptions import ValidationError
from datetime import date
from marshmallow.validate import Length, OneOf, And, Regexp, Range

class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    complex_number = db.Column(db.Integer, default= None) # make sure it's possible for them to be able to leave this blank in the JSON body
    street_number = db.Column(db.Integer, nullable= False)
    street_name = db.Column(db.String(128), nullable= False)
    suburb = db.Column(db.String(128), nullable= False)
    postcode = db.Column(db.Integer, nullable= False) # decide whether you want to allow overseas addresses or not here with validation. If so change this to a string to allow letters/country codes. Then you'd need another table to indicate the state/country 
    

class AddressSchema(ma.Schema):
    # This allows the models to be serialized and deserialized to and from JSON.    
   
    # Validations
    complex_number = fields.Integer(load_defalt=None)
    street_number = fields.Integer(required=True)
    street_name = fields.String(required=True, validate=
        Length(min=2, error='Street name must be at least 2 characters long'))
    suburb = fields.String(required=True, validate=
        Length(min=2, error='Street name must be at least 2 characters long'))
    postcode = fields.Integer(required=True, validate=Range(min=200, max=9999)) # smallest postcode is 200 (in the ACT) and the largest is 9999 (in QLD)
    
    class Meta:
        fields = ('complex_number', 'street_number', 'street_name', 'suburb', 'postcode')
        ordered = True # puts the keys in the same order as the fields lists above otherwise it will be alphabetical order.

