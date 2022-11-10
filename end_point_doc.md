# API Endpoints Documentation

## User Routes

### /users/

#### Methods: POST  

- Arguments: None  
- Description: Creates a new address and user instance in the database  
- Authentication: @jwt_required()  
- Headers-Authorization: Bearer {Token} - all users are authorised to create a new address and user.  
- Request Body:

```JSON
{   "complex_number": 14,
    "street_number": 20,
    "street_name": "Captain Road",
    "suburb": "West End",
    "postcode": 4006,
    "users": [{
        "title": "Ms",
        "first_name": "Rachael",
        "middle_name": "Anne",
        "last_name": "Cook",
        "password": "hamAnd335*",
        "email": "test.coggfg4hhttt@bgbc.edu.au",
        "phone": "0414563531",
        "dob": "1980-09-02",
        "gender": "female",
        "type": "Student"
    }]
}
```

- Request response:

 ```JSON
  {
{
    "id": 7,
    "title": "Ms",
    "first_name": "Rachael",
    "middle_name": "Anne",
    "last_name": "Cook",
    "email": "test.coggfg4hhttt@bgbc.edu.au",
    "phone": "0414563531",
    "dob": "1980-09-02",
    "gender": "female",
    "type": "Student",
    "student": null,
    "employee": null,
    "address": {
        "id": 6,
        "complex_number": 14,
        "street_number": 20,
        "street_name": "Captain Road",
        "suburb": "West End",
        "postcode": 4006
    },
    "student_relations": []
}
    }
```

If not authorised:  

```JSON
{
    "error": "You are not authorized to perform this action"
}
```

#### Methods: GET  

- Arguments: None  
- Description: Returns a JSON list of all the users stored in the database ordered in ascending order by last name. The user's address is also nested at the end.
- Authentication: @jwt_required()  
- Headers-Authorization: Bearer {Token} - employees with admin access only.  
- Request Body: None
- Request Response:  

```JSON
[
    {
        "id": 2,
        "title": "Mr",
        "first_name": "Damion",
        "middle_name": "George",
        "last_name": "Burns",
        "email": "damion.burns@bgbc.edu.au",
        "phone": "0405301451",
        "dob": "1985-04-07",
        "gender": "male",
        "type": "Employee",
        "address": {
            "id": 2,
            "complex_number": 12,
            "street_number": 24,
            "street_name": "Sand Street",
            "suburb": "Milton",
            "postcode": 4066
        }
    },...]
```

If not authorised:  

```JSON
{
    "error": "You are not authorized to perform this action"
}
```
### /userss/\<int:id\>  

- Methods: GET  
- Arguments: id (an integer of the user ID whose record is to be  returned)
- Description: Returns the user instance of the user with the id number provided in the URI parameter with a nested address object included.
- Authentication: @jwt_required()  
- Headers-Authorization: Bearer {Token}-only employees with admin access or the user with the id in the restful URI parameter provided.
- Request Body: None
- Request Response:

```JSON
{
{
    "id": 1,
    "title": "Miss",
    "first_name": "Danielle",
    "middle_name": "Jane",
    "last_name": "Clark",
    "email": "danielle.clark@bgbc.edu.au",
    "phone": "0416393531",
    "dob": "1987-12-07",
    "gender": "female",
    "type": "Employee",
    "address": {
        "id": 1,
        "complex_number": 2,
        "street_number": 20,
        "street_name": "Rose Street",
        "suburb": "Toowong",
        "postcode": 4066
    }
}
}
```

#### Methods:  ['PUT', 'PATCH']

- Arguments: id (an integer of the user ID to update)
- Description: Allows an authorised user to update one user instance.
- Authentication: @jwt_required()  
- Headers-Authorization: Bearer {Token}- only employees with admin access or the user with the id in the restful URI parameter provided.
- Request Body: Include any fields you wish to update:

```JSON
{
    "title": "Mrs",
    "first_name": "Rachael",
    "middle_name": "Anne",
    "last_name": "Aaron",
    "password": "hamAnd335*",
    "email": "rachael.cook@bgbc.edu.au",
    "phone": "0414563531",
    "dob": "1980-09-02",
    "gender": "female",
    "type": "Caregiver"

}

```

- Request Response: (all fields are returned)
```JSON
{
    "id": 9,
    "title": "Mrs",
    "first_name": "Rachael",
    "middle_name": "Anne",
    "last_name": "Aaron",
    "email": "rachael.cook@bgbc.edu.au",
    "phone": "0414563531",
    "dob": "1980-09-02",
    "gender": "female",
    "type": "Caregiver",
    "student": null,
    "employee": null,
    "address": {
        "id": 8,
        "complex_number": 14,
        "street_number": 20,
        "street_name": "Captain Road",
        "suburb": "West End",
        "postcode": 4006
    }
}
```

```JSON
{
    "id": 1,
    "complex_number": 1,
    "street_number": 15,
    "street_name": "Rosey Street",
    "suburb": "Milton",
    "postcode": 4065,
    "users": [
        {
            "id": 1,
            "first_name": "Danielle",
            "last_name": "Clark",
            "type": "Employee"
        }
    ]
}
```

If not authorised:  

```JSON
{
    "error": "You are not authorized to perform this action"
}
```

#### Methods:  ['Delete']

- Arguments: id (an integer of the user ID to update)
- Description: Allows an authorised user to delete one user instance.
- Authentication: @jwt_required()  
- Headers-Authorization: Bearer {Token}- only employees with admin access
- Request Body: None

```JSON
{
    "message": "The records for Danielle Clark were deleted successfully."
}
```

If not authorised:  

```JSON
{
    "error": "You are not authorized to perform this action"
}
```

## Address Routes

### /addresses/

- Methods: POST  
- Arguments: None  
- Description: Creates a new address in the database  
- Authentication: @jwt_required()  
- Headers-Authorization: Bearer {Token} - all users are authorised to create a new address.  
- Request Body:

```JSON
{   
    "complex_number": 14,
    "street_number": 20,
    "street_name": "Captain Road",
    "suburb": "West End",
    "postcode": 4006
}
```

- Request response:

 ```JSON
  {
    "id": 4,
    "complex_number": 14,
    "street_number": 20,
    "street_name": "Captain Road",
    "suburb": "West End",
    "postcode": 4006
    }
```

- Methods: GET  
- Arguments: None  
- Description: Returns a JSON list of all the addresses stored in the database ordered by postcode. A nested list of all the users listed at that address is also returned.
- Authentication: @jwt_required()  
- Headers-Authorization: Bearer {Token} - employees with admin access only.  
- Request Body: None
- Request Response:  

```JSON
[
    {
        "id": 1,
        "complex_number": 2,
        "street_number": 20,
        "street_name": "Rose Street",
        "suburb": "Toowong",
        "postcode": 4066,
        "users": [
            {
                "id": 1,
                "first_name": "Danielle",
                "last_name": "Clark",
                "type": "Employee"
            }
        ]
    },
    {
        "id": 2,
        "complex_number": 12,
        "street_number": 24,
        "street_name": "Sand Street",
        "suburb": "Milton",
        "postcode": 4066,
        "users": [
            {
                "id": 2,
                "first_name": "Damion",
                "last_name": "Burns",
                "type": "Employee"
            }
        ]
    }
]
```

If not authorised:  

```JSON
{
    "error": "You are not authorized to perform this action"
}
```

If email address already exists in the database:

```JSON
{
    "error": "Email address already in use"
}
```

### /addresses/\<int:id\>  

- Methods: GET  
- Arguments: id (an integer of the address ID to return)
- Description: Returns the address instance of the address with the id number provided in the URI parameter.
- Authentication: @jwt_required()  
- Headers-Authorization: Bearer {Token}- users who have this address listed as theirs as well as employees with admin access only.
- Request Body: None
- Request Response:

```JSON
{
    "id": 1,
    "complex_number": 2,
    "street_number": 20,
    "street_name": "Rose Street",
    "suburb": "Toowong",
    "postcode": 4066,
    "users": [
        {
            "id": 1,
            "first_name": "Danielle",
            "last_name": "Clark",
            "type": "Employee"
        }
    ]
}


If not authorised:  

```JSON
{
    "error": "You are not authorized to perform this action"
}
```

- Methods:  ['PUT', 'PATCH']
- Arguments: id (an integer of the address ID to update)
- Description: Allows an authorised user to update one address instance.
- Authentication: @jwt_required()  
- Headers-Authorization: Bearer {Token}- users who have this address listed as theirs as well as employees with admin access.
- Request Body: Include any fields you wish to update:

```JSON
{
    "complex_number": 1,
    "street_number": 15,
    "street_name": "Rosey Street",
    "suburb": "Milton",
    "postcode": 4065,
}
```

- Request Response: (all fields are returned)

```JSON
{
    "id": 1,
    "complex_number": 1,
    "street_number": 15,
    "street_name": "Rosey Street",
    "suburb": "Milton",
    "postcode": 4065,
    "users": [
        {
            "id": 1,
            "first_name": "Danielle",
            "last_name": "Clark",
            "type": "Employee"
        }
    ]
}
```

If not authorised:  

```JSON
{
    "error": "You are not authorized to perform this action"
}
```

- Methods:  [DELETE]
- Arguments: id (an integer of the address ID to update)
- Description: Allows an authorised user to delete one address instance.
- Authentication: @jwt_required()  
- Headers-Authorization: Bearer {Token}- users who have this address listed as theirs as well as employees with admin access.
- Request Body: None
- Request Response: (all fields are returned)

```JSON
{
    "message": "The records for address ID 1 located on Rose Street in West End were deleted successfully."
}
```

If not authorised:  

```JSON
{
    "error": "You are not authorized to perform this action"
}
```

## Subject Routes

### /Subjects/

- Methods: POST  
- Arguments: None  
- Description: Creates a new subject instance in the database  
- Authentication: @jwt_required()  
- Headers-Authorization: Bearer {Token} - Bearer {Token}- employees with admin access only
- Request Body:

```JSON
{
    "id": "09SCI",
    "name": "Junior Science",
    "year_level": 9,
    "max_students": 20,
    "department": "Science"
  
}
```

- Request response:

 ```JSON
  {
{
    "id": "09SCI",
    "name": "Junior Science",
    "year_level": 9,
    "max_students": 20,
    "department": "Science",
    "subject_classes": []
}
    }
```

- Methods: GET  
- Arguments: None  
- Description: Returns a JSON list of all the subjects stored in the database ordered by subject_id.
- Authentication: None
- Headers-Authorization: None
- Request Body: None
- Request Response:  

```JSON
[
    {
        "id": "09EE",
        "name": "Enterprise Education",
        "year_level": 9,
        "max_students": 28,
        "department": "Business"
    },
    {
        "id": "09ENG",
        "name": "Junior English",
        "year_level": 9,
        "max_students": 28,
        "department": "English"
    },
    {
        "id": "09MAB",
        "name": "Maths Beta",
        "year_level": 9,
        "max_students": 25,
        "department": "Maths"
    }
]
```

### /subjects/\<string:id\>  

- Methods: GET  
- Arguments: id (a string of the subject ID of the subject to return)
- Description: Returns the subject instance of the subject with the id number provided in the URI parameter.It also includes a nested list of all the subject_class instances for that subject with a list of students enrolled in that class (just their first and last name).
- Authentication: @jwt_required()  
- Headers-Authorization: all authenticated users are able to access this information.
- Request Body: None
- Request Response:

```JSON
{
    "id": "09MAB",
    "name": "Maths Beta",
    "year_level": 9,
    "max_students": 25,
    "department": "Maths",
    "subject_classes": [
        {
            "id": "09MAB01-2023",
            "room": "SA1.4",
            "timetable_line": 3,
            "employee_id": 2,
            "employee": {
                "user": {
                    "first_name": "Damion",
                    "last_name": "Burns"
                }
            },
            "enrollments": [
                {
                    "student": {
                        "user": {
                            "first_name": "Isabelle",
                            "last_name": "Smith"
                        }
                    }
                },
                {
                    "student": {
                        "user": {
                            "first_name": "Gabriella",
                            "last_name": "Jones"
                        }
                    }
                }
            ]
        }
    ]
}


If not authorised:  

```JSON
{
    "error": "You are not authorized to perform this action"
}
```
If subject id provided in the URI parameter doesn't exist in the database:

```JSON
{
    "error": "Subject not found with id 11ACC."
}
```

- Methods:  ['PUT', 'PATCH']
- Arguments: id (a string of the subject ID of the subject to update)
- Description: Updates the subject instance of the subject with the id number provided in the URI parameter.
- Authentication: @jwt_required()  
- Headers-Authorization: Bearer {Token}- only employees with admin access.
- Request Body: Include any fields you wish to update:

```JSON
{
    "id": "10SCI",
    "name": "Junior Science",
    "year_level": 10,
    "max_students": 25,
    "department": "Science"
}
```

- Request Response: (all fields are returned)

```JSON
{
    "id": "10SCI",
    "name": "Junior Science",
    "year_level": 10,
    "max_students": 25,
    "department": "Science",
    "subject_classes": []
}
```

If not authorised:  

```JSON
{
    "error": "You are not authorized to perform this action"
}
```
If subject id provided in the URI parameter doesn't exist in the database:

```JSON
{
    "error": "Subject not found with id 11ACC."
}
```

- Methods:  [DELETE]
- id (a string of the subject ID of the subject to update)
- Description: Deletes the subject instance of the subject with the id number provided in the URI parameter.
- Authentication: @jwt_required()  
- Headers-Authorization: Bearer {Token}- only employees with admin access.
- Request Body: None
- Request Response: 

```JSON
{
    "message": "Year 10 Junior Science (10SCI) was deleted successfully."
}
```

If not authorised:  

```JSON
{
    "error": "You are not authorized to perform this action"
}
```

If subject id provided in the URI parameter doesn't exist in the database:

```JSON
{
    "error": "Subject not found with id 11ACC."
}
```
## Subject ClassesRoutes

### /Subjects/<string:subject_id>/Classes

- Methods: POST  
- Arguments: Subject_id (a string of the subject ID of the subject to add a subject_class instance to)  
- Description: Creates a new subject_class instance of the provided subject in the database. Each class has a maximum class size so typically subjects will have multiple classes covering the same subject area each with different students.  
- Authentication: @jwt_required()  
- Headers-Authorization: Bearer {Token} - Bearer {Token}- employees with admin access only
- Request Body:

```JSON
{
    "id": "09MAB03-2023",
    "room": "SA1.4",
    "timetable_line": 3,
    "employee_id": 2
}
  
```

- Request response: (Note: the request response includes the new instance of the subject_class encluding a nested instance of the parent subject)

 ```JSON
{
    "id": "09MAB04-2023",
    "room": "SA1.4",
    "timetable_line": 3,
    "subject": {
        "id": "09MAB",
        "name": "Maths Beta",
        "year_level": 9,
        "max_students": 25,
        "department": "Maths"
    },
    "employee_id": 2,
    "employee": {
        "user": {
            "first_name": "Damion",
            "last_name": "Burns"
        }
    }
}
```

- Methods: GET  
- Arguments: None  
- Description: Returns a JSON list of all the subjects stored in the database ordered by subject_id.
- Authentication: None
- Headers-Authorization: None
- Request Body: None
- Request Response:  

```JSON
[
    {
        "id": "09EE",
        "name": "Enterprise Education",
        "year_level": 9,
        "max_students": 28,
        "department": "Business"
    },
    {
        "id": "09ENG",
        "name": "Junior English",
        "year_level": 9,
        "max_students": 28,
        "department": "English"
    },
    {
        "id": "09MAB",
        "name": "Maths Beta",
        "year_level": 9,
        "max_students": 25,
        "department": "Maths"
    }
]
```

### /subjects/\<string:id\>  

- Methods: GET  
- Arguments: id (a string of the subject ID of the subject to return)
- Description: Returns the subject instance of the subject with the id number provided in the URI parameter.It also includes a nested list of all the subject_class instances for that subject with a list of students enrolled in that class (just their first and last name).
- Authentication: @jwt_required()  
- Headers-Authorization: all authenticated users are able to access this information.
- Request Body: None
- Request Response:

```JSON
{
    "id": "09MAB",
    "name": "Maths Beta",
    "year_level": 9,
    "max_students": 25,
    "department": "Maths",
    "subject_classes": [
        {
            "id": "09MAB01-2023",
            "room": "SA1.4",
            "timetable_line": 3,
            "employee_id": 2,
            "employee": {
                "user": {
                    "first_name": "Damion",
                    "last_name": "Burns"
                }
            },
            "enrollments": [
                {
                    "student": {
                        "user": {
                            "first_name": "Isabelle",
                            "last_name": "Smith"
                        }
                    }
                },
                {
                    "student": {
                        "user": {
                            "first_name": "Gabriella",
                            "last_name": "Jones"
                        }
                    }
                }
            ]
        }
    ]
}


If not authorised:  

```JSON
{
    "error": "You are not authorized to perform this action"
}
```
If subject id provided in the URI parameter doesn't exist in the database:

```JSON
{
    "error": "Subject not found with id 11ACC."
}
```

- Methods:  ['PUT', 'PATCH']
- Arguments: id (a string of the subject ID of the subject to update)
- Description: Updates the subject instance of the subject with the id number provided in the URI parameter.
- Authentication: @jwt_required()  
- Headers-Authorization: Bearer {Token}- only employees with admin access.
- Request Body: Include any fields you wish to update:

```JSON
{
    "id": "10SCI",
    "name": "Junior Science",
    "year_level": 10,
    "max_students": 25,
    "department": "Science"
}
```

- Request Response: (all fields are returned)

```JSON
{
    "id": "10SCI",
    "name": "Junior Science",
    "year_level": 10,
    "max_students": 25,
    "department": "Science",
    "subject_classes": []
}
```

If not authorised:  

```JSON
{
    "error": "You are not authorized to perform this action"
}
```
If subject id provided in the URI parameter doesn't exist in the database:

```JSON
{
    "error": "Subject not found with id 11ACC."
}
```

- Methods:  [DELETE]
- id (a string of the subject ID of the subject to update)
- Description: Deletes the subject instance of the subject with the id number provided in the URI parameter.
- Authentication: @jwt_required()  
- Headers-Authorization: Bearer {Token}- only employees with admin access.
- Request Body: None
- Request Response: 

```JSON
{
    "message": "Year 10 Junior Science (10SCI) was deleted successfully."
}
```

If not authorised:  

```JSON
{
    "error": "You are not authorized to perform this action"
}
```

If subject id provided in the URI parameter doesn't exist in the database:

```JSON
{
    "error": "Subject not found with id 11ACC."
}
```
