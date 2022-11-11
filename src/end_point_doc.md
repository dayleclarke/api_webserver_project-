# API Endpoints Documentation

## Auth Routes

### /auth/login/

- Arguments: None
- Description: A route to login and receive a token to use for authentication and authorization.
- Authentication: None
- Headers-Authorization: None
- Request Body:

For an admin user:

```JSON
{ 
    "email": "damion.burns@bgbc.edu.au",
    "password": "ChangeMe!1"
}
```

For an employee without admin rights:

```JSON
{ 
    "email": "danielle.clark@bgbc.edu.au",
    "password": "ExamplePassword1!"
}
```

For a student:

```JSON
    {
        "email": "Isabelle.Smith@bgbc.edu.au",
        "password": "ChangeMe1!"
    }
```

For a caregiver:

```JSON
{ 
    "email": "janet.stone12@gmail.com",
    "password": "ChangeMe2**"
}
```

- Request response:
  
```JSON
{
    "email": "damion.burns@bgbc.edu.au",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2ODE1Njg5NywianRpIjoiMzQwZGY5MDctNTJmMi00ODdmLWExZGEtMjcwYTcwMTllOWI0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjIiLCJuYmYiOjE2NjgxNTY4OTcsImV4cCI6MTY2ODU4ODg5N30.R_qPaD62pznFcpKzdJa5_kHpxY2tHBh5ssZ3AMm9v7A",
    "type": "Employee"
}
```

### /auth/make_admin/\<int:employee_id>/

- Arguments: id (an integer of the employee ID who is being made an admin employee)  
- Description: Updates an existing employee (specificed in the URI) record and allows them to be set as an admin employee  
- Authentication: @jwt_required()  
- Headers-Authorization: Bearer {Token} - only employees with admin access can access this route.  
- Request Body: (can include one or all the fields shown below:)

```JSON
{
        "hired_date": "2017-01-01",
        "job_title": "Secondary Teacher",
        "department": "English",
        "is_admin": true
}
```

- Request response:
  
```JSON
{
    "id": 1,
    "user": {
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
    },
    "hired_date": "2017-01-01",
    "job_title": "Secondary Teacher",
    "department": "English",
    "is_admin": true
}
```

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

### /users/\<int:id\>  

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

## Employee Routes

### /employees/

#### Methods: POST  

- Arguments: None  
- Description: Creates a new user and employee instance in the database  
- Authentication: @jwt_required()  
- Headers-Authorization: Bearer {Token} - only admin are able to create an employee instance.  
- Request Body:

```JSON
{    
    "title": "Ms",
    "first_name": "Rachael",
    "middle_name": "Anne",
    "last_name": "Cook",
    "password": "hamAnd335*",
    "email": "test.coggfg4ttt@bgbc.edu.au",
    "phone": "0414563531",
    "dob": "1980-09-02",
    "gender": "female",
    "type": "Student",
    "employee": {
        "hired_date": "2009-01-01",
        "job_title": "Teacher",
        "department": "English",
        "is_admin": false
        }
}
```

- Request response:

 ```JSON
{
    "id": 4,
    "user": {
        "id": 9,
        "title": "Ms",
        "first_name": "Rachael",
        "middle_name": "Anne",
        "last_name": "Cook",
        "email": "test.coggfg4ffttt@bgbc.edu.au",
        "phone": "0414563531",
        "dob": "1980-09-02",
        "gender": "female",
        "type": "Student"
    },
    "hired_date": "2009-01-01",
    "job_title": "Teacher",
    "department": "English",
    "is_admin": false
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
- Description: Returns a JSON list of all the employees stored in the database ordered in descending order by hired_date. There will also be a neested list of the classes they currently teach with just the subject_id and subject_name.
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token} - employees with admin access only.  
- Request Body: None
- Request Response:  

```JSON
[{
    "id": 1,
    "user": {
        "id": 1,
        "title": "Miss",
        "first_name": "Danielle",
        "middle_name": "Jane",
        "last_name": "Clark",
        "email": "danielle.clark@bgbc.edu.au",
        "phone": "0416393531",
        "dob": "1987-12-07",
        "gender": "female",
        "type": "Employee"
    },
    "hired_date": "2019-01-01",
    "job_title": "Teacher",
    "department": "Business",
    "is_admin": false,
    "subject_classes": [
        {
            "id": "09EE01-2023",
            "subject": {
                "name": "Enterprise Education"
            }
        },
        {
            "id": "09EE02-2023",
            "subject": {
                "name": "Enterprise Education"
            }
        }
    ]
    },...]
```

If not authorised:  

```JSON
{
    "error": "You are not authorized to perform this action"
}
```

### /employees/\<int:id\>  

- Methods: GET  
- Arguments: id (an integer of the employee ID whose record is to be  returned)
- Description: Returns the employee instance of the user with the id number provided in the URI parameter. A nested list of the classes they currently teach with just the subject_id and subject_name are also include.
- Authentication: @jwt_required()  
- Headers-Authorization: Bearer {Token}-only employees with admin access or the employee with the id in the restful URI parameter provided.
- Request Body: None
- Request Response:

```JSON
{
    "id": 2,
    "user": {
        "id": 2,
        "title": "Mr",
        "first_name": "Damion",
        "middle_name": "George",
        "last_name": "Burns",
        "email": "damion.burns@bgbc.edu.au",
        "phone": "0405301451",
        "dob": "1985-04-07",
        "gender": "male",
        "type": "Employee"
    },
    "hired_date": "2010-01-01",
    "job_title": "Teacher",
    "department": "Maths",
    "is_admin": true,
    "subject_classes": [
        {
            "id": "09ENG05-2023",
            "subject": {
                "name": "Junior English"
            }
        }
    ]
}
```

#### Methods:  ['PUT', 'PATCH']

- Arguments: id (an integer of the employee ID to identify the employee object to update)
- Description: Allows an authorised employee or the employee themselves to update one employee instance. NOTE admin access can't be set through this route. Updating admin access must be done through (/auth/make_admin/<int:employee_id>/)
- Authentication: @jwt_required()  
- Headers-Authorization: Bearer {Token}-only employees with admin access or the employee with the id in the restful URI parameter provided.
- Request Body: Include any fields you wish to update:

```JSON
{
        "hired_date": "2017-01-01",
        "job_title": "Secondary Teacher",
        "department": "English"
}
```

- Request Response: (all fields are returned)

```JSON
{
    "id": 1,
    "user": {
        "id": 1,
        "title": "Miss",
        "first_name": "Danielle",
        "middle_name": "Jane",
        "last_name": "Clark",
        "email": "danielle.clark@bgbc.edu.au",
        "phone": "0416393531",
        "dob": "1987-12-07",
        "gender": "female",
        "type": "Employee"
    },
    "hired_date": "2017-01-01",
    "job_title": "Secondary Teacher",
    "department": "English",
    "is_admin": false
}

```

If not authorised:  

```JSON
{
    "error": "You are not authorized to perform this action"
}
```

#### Methods:  ['Delete']

- Arguments: id (an integer of the employee ID of the employee to delete)
- Description: Allows an authorised user to delete one employee instance.
- Authentication: @jwt_required()  
- Headers-Authorization: Bearer {Token}- only employees with admin access
- Request Body: None

```JSON
{
    "message": "The records for the employee with Employee ID 1 were deleted successfully"
}
```

If not authorised:  

```JSON
{
    "error": "You are not authorized to perform this action"
}
```
## Student Routes

### /students/

#### Methods: POST  

- Arguments: None  
- Description: Creates a new user and student instance in the database  
- Authentication: @jwt_required()  
- Headers-Authorization: Bearer {Token} - only admin can create a new student instance.  
- Request Body:

```JSON
{   "title": "Ms",
    "first_name": "Sophie",
    "middle_name": "Anne",
    "last_name": "Long",
    "password": "hamAnd335*",
    "email": "sophie.long@bgbc.edu.au",
    "phone": "0414563531",
    "dob": "2008-09-02",
    "gender": "female",
    "type": "Student",
    "student": {
            "homegroup": "WH01",
            "enrollment_date": "2022-01-01",
            "year_level": 9,
            "birth_country": "Australia"
        }
}

```

- Request response:

 ```JSON
{
    "id": 8,
    "user": {
        "title": "Ms",
        "first_name": "Sophie",
        "middle_name": "Anne",
        "last_name": "Long",
        "email": "sophie.long4@bgbc.edu.au",
        "phone": "0414563531",
        "dob": "2008-09-02",
        "gender": "female",
        "type": "Student",
    },
    "homegroup": "WH01",
    "enrollment_date": "2022-01-01",
    "year_level": 9,
    "birth_country": "Australia"
}
```

If not authorised:  

```JSON
{
    "error": "You are not authorized to perform this action"
}
```
If username already taken:

```JSON
{
    "error": "Email address already in use"
}


```
#### Methods: GET  

- Arguments: None  
- Description: Returns a JSON list of all the students stored in the database. There will also be a nested object containing their user information.
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token} - employees only (both admin and non admin).  
- Request Body: None
- Request Response:  

```JSON
[
    {
        "id": 1,
        "user": {
            "title": "Miss",
            "first_name": "Isabelle",
            "middle_name": "Margaret",
            "last_name": "Smith",
            "email": "Isabelle.Smith@bgbc.edu.au",
            "phone": "0405301444",
            "dob": "2004-04-07",
            "gender": "female",
            "type": "Student",
        },
        "homegroup": "WH01",
        "enrollment_date": "2020-01-01",
        "year_level": 9,
        "birth_country": "Australia"
    },
    },...]
```

If not authorised:  

```JSON
{
    "error": "You are not authorized to perform this action"
}
```

### /students/\<int:student_id\>  

- Methods: GET  
- Arguments: id (an integer of the student_id whose record is to be returned)
- Description: Returns the student instance of the student with the id number provided in the URI parameter. A nested user object from the parent table “user” is also included and the child table “student_relations”.  This route makes it efficient for a teacher to query a student and find relevant information about the student.  This includes their caregiver’s information because this is frequently needed by teachers when contacting parents for behavioural issues. A student can also look at their own information to ensure their details are correct.   
- Authentication: @jwt_required()  
- Headers-Authorization: Bearer {Token}-only employees or the student with the id in the restful URI parameter provided.
- Request Body: None
- Request Response:

```JSON
{
    "id": 1,
    "user": {
        "title": "Miss",
        "first_name": "Isabelle",
        "middle_name": "Margaret",
        "last_name": "Smith",
        "email": "Isabelle.Smith@bgbc.edu.au",
        "phone": "0405301444",
        "dob": "2004-04-07",
        "gender": "female",
        "type": "Student"
    },
    "homegroup": "WH01",
    "enrollment_date": "2020-01-01",
    "year_level": 9,
    "birth_country": "Australia",
    "student_relations": [
        {
            "user": {
                "title": "Mrs",
                "first_name": "Janet",
                "middle_name": "Jane",
                "last_name": "Stone",
                "email": "janet.stone12@gmail.com",
                "phone": "0405301554",
                "dob": "1975-12-07",
                "gender": "female",
                "type": "Caregiver",
                "address": null
            },
            "relationship_to_student": "Mother",
            "is_primary_contact": true
        }
    ]
}
```

#### Methods:  ['PUT', 'PATCH']

- Arguments: id (an integer of the student ID to identify the student object to update)
- Description: Allows an authorised employee to update one student instance. 
- Authentication: @jwt_required()  
- Headers-Authorization: Bearer {Token}-only employees with admin access. 
- Request Body: Include any fields you wish to update:

```JSON
{    "homegroup": "WH05",
    "enrollment_date": "2020-01-01",
    "year_level": 9,
    "birth_country": "Japan"
}


```

- Request Response: (all fields are returned)

```JSON
{
    "id": 1,
    "user": {
        "title": "Miss",
        "first_name": "Isabelle",
        "middle_name": "Margaret",
        "last_name": "Smith",
        "email": "Isabelle.Smith@bgbc.edu.au",
        "phone": "0405301444",
        "dob": "2004-04-07",
        "gender": "female",
        "type": "Student"
    },
    "homegroup": "WH05",
    "enrollment_date": "2020-01-01",
    "year_level": 9,
    "birth_country": "Japan"
}
```

If not authorised:  

```JSON
{
    "error": "You are not authorized to perform this action"
}
```

#### Methods:  ['Delete']

- Arguments: id (an integer of the student ID of the student to delete)
- Description: Allows an authorised user to delete one student instance.
- Authentication: @jwt_required()  
- Headers-Authorization: Bearer {Token}- only employees with admin access
- Request Body: None

```JSON
{
    "message": "The records for the student with Student ID5 were deleted successfully"
}
```

If not authorised:  

```JSON
{
    "error": "You are not authorized to perform this action"
}
```

```JSON
If a student with the ID doesn’t exist:
{
    "error": "Student not found with id 15"
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
- id (a string of the subject ID of the subject to delete)
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

### /Subjects/Classes

- Methods: GET  
- Arguments: None  
- Description: Returns a JSON list of all the subject classes stored in the database.  It also includes nested data about the parent subject.
- Authentication: @jwt_required()  
- Headers-Authorization: all authenticated users are able to access this route.
- Request Body: None
- Request Response:  

```JSON
[
    {
        "id": "09EE01-2023",
        "room": "MB2.2",
        "timetable_line": 2,
        "subject": {
            "id": "09EE",
            "name": "Enterprise Education",
            "year_level": 9,
            "max_students": 28,
            "department": "Business"
        },
        "employee_id": 1,
        "employee": {
            "user": {
                "first_name": "Danielle",
                "last_name": "Clark"
            }
        }
    },
    {
        "id": "09EE02-2023",
        "room": "MB2.4",
        "timetable_line": 1,
        "subject": {
            "id": "09EE",
            "name": "Enterprise Education",
            "year_level": 9,
            "max_students": 28,
            "department": "Business"
        },
        "employee_id": 1,
        "employee": {
            "user": {
                "first_name": "Danielle",
                "last_name": "Clark"
            }
        }
    }
]
```

### /Subjects/Classes<string:subject_class_id\>  

- Methods: GET  
- Arguments: id (a string of the subject_class ID of the subject_class to return)
- Description: Returns the subject_class instance of the class with the id number provided in the URI parameter.It also includes a nested parent subject instance and a nested list of students enrolled in the class (including all of their personal information including their nested user and address information).
- Authentication: @jwt_required()  
- Headers-Authorization: all employees are able to access this information.
- Request Body: None
- Request Response:

```JSON
{
    "id": "09EE01-2023",
    "room": "MB2.2",
    "timetable_line": 2,
    "subject": {
        "id": "09EE",
        "name": "Enterprise Education",
        "year_level": 9,
        "max_students": 28,
        "department": "Business"
    },
    "employee_id": 1,
    "employee": {
        "user": {
            "first_name": "Danielle",
            "last_name": "Clark"
        }
    },
    "enrollments": [
        {
            "student": {
                "id": 1,
                "user": {
                    "title": "Miss",
                    "first_name": "Isabelle",
                    "middle_name": "Margaret",
                    "last_name": "Smith",
                    "email": "Isabelle.Smith@bgbc.edu.au",
                    "phone": "0405301444",
                    "dob": "2004-04-07",
                    "gender": "female",
                    "type": "Student",
                    "address": {
                        "id": 3,
                        "complex_number": null,
                        "street_number": 62,
                        "street_name": "York Street",
                        "suburb": "Nundah",
                        "postcode": 4012
                    }
                },
                "homegroup": "WH01",
                "enrollment_date": "2020-01-01",
                "year_level": 9,
                "birth_country": "Australia"
            }
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
    "error": "Class not found with id 09EE06-2023."
}
```

- Methods:  ['PUT', 'PATCH']
- Arguments: id (a string of the subject_class ID of the subject to update)
- Description: Updates the subject_class instance of the subject_class with the id number provided in the URI parameter.
- Authentication: @jwt_required()  
- Headers-Authorization: Bearer {Token}- only employees with admin access.
- Request Body: Include any fields you wish to update:

```JSON
{
    "id": "09MAB01-2023",
    "room": "SA1.9",
    "timetable_line": 3,
    "employee_id": 2
}
```

- Request Response: (all fields are returned)

```JSON
{
    "id": "09MAB01-2023",
    "room": "SA1.9",
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

If not authorised:  

```JSON
{
    "error": "You are not authorized to perform this action"
}
```

If subject_class id provided in the URI parameter doesn't exist in the database:

```JSON
{
    "error": "Class not found with id 09MAB01-2024."
}
```

- Methods:  [DELETE]
- id (a string of the subject_class ID of the subject_class to delete)
- Description: Deletes the subject instance of the subject with the id number provided in the URI parameter.
- Authentication: @jwt_required()  
- Headers-Authorization: Bearer {Token}- only employees with admin access.
- Request Body: None
- Request Response:

```JSON
{
    "message": "The records for the Subject Class ID 09MAB01-2023 were deleted successfully"
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
    "error": "Class not found with id 09MAB01-2024."
}
```
## Enrollment Routes

### /enrollments/

#### Methods: POST  

- Arguments: None  
- Description: Creates a new enrollment instance in the database  
- Authentication: @jwt_required()  
- Headers-Authorization: Bearer {Token} - only admin can create a new enrollment.  
- Request Body:

```JSON
{
    "date": "2023-01-01",
    "subject_class_id": "09EE01-2023",
    "student_id": 1
}


```

- Request response:

 ```JSON
{
{
    "id": 5,
    "date": "2023-01-01",
    "subject_class_id": "09EE01-2023",
    "student_id": 1,
    "student": {
        "id": 1,
        "user": {
            "title": "Miss",
            "first_name": "Isabelle",
            "middle_name": "Margaret",
            "last_name": "Smith",
            "email": "Isabelle.Smith@bgbc.edu.au",
            "phone": "0405301444",
            "dob": "2004-04-07",
            "gender": "female",
            "type": "Student"
        },
        "homegroup": "WH05",
        "enrollment_date": "2020-01-01",
        "year_level": 9,
        "birth_country": "Japan"
    }
}
```

If not authorised:  

```JSON
{
    "error": "You are not authorized to perform this action"
}
```


```
#### Methods: GET  

- Arguments: None  
- Description: Returns a JSON list of all the enrollments stored in the database. 
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token} - employees only (both admin and non admin).  
- Request Body: None
- Request Response:  

```JSON
[
    {
        "id": 1,
        "date": "2023-01-01",
        "subject_class_id": "09EE01-2023",
        "student_id": 1
    },
    {
        "id": 2,
        "date": "2023-01-01",
        "subject_class_id": "09EE01-2023",
        "student_id": 2
    },
    {
        "id": 5,
        "date": "2023-01-01",
        "subject_class_id": "09EE01-2023",
        "student_id": 1
    },
    {
        "id": 3,
        "date": "2023-01-01",
        "subject_class_id": "09MAB01-2023",
        "student_id": 1
    },
    {
        "id": 4,
        "date": "2023-01-01",
        "subject_class_id": "09MAB01-2023",
        "student_id": 2
    }
]
```

If not authorised:  

```JSON
{
    "error": "You are not authorized to perform this action"
}
```

### /enrollments/\<int:id\>  

- Methods: GET  
- Arguments: id (an integer of the enrollment_id to be returned)
- Description: Returns the  enrolment instance of enrolment with the id number provided in the URI parameter. A nested student object has also been included with information about the student enrolled in the subject.  
- Authentication: @jwt_required()  
- Headers-Authorization: Bearer {Token}- employees only (both admin and non admin).  
- Request Body: None
- Request Response:

```JSON
{
    "id": 1,
    "date": "2023-01-01",
    "subject_class_id": "09EE01-2023",
    "student_id": 1,
    "student": {
        "id": 1,
        "user": {
            "title": "Miss",
            "first_name": "Isabelle",
            "middle_name": "Margaret",
            "last_name": "Smith",
            "email": "Isabelle.Smith@bgbc.edu.au",
            "phone": "0405301444",
            "dob": "2004-04-07",
            "gender": "female",
            "type": "Student"
        },
        "homegroup": "WH05",
        "enrollment_date": "2020-01-01",
        "year_level": 9,
        "birth_country": "Japan"
    }
}
```

#### Methods:  ['PUT', 'PATCH']

- Arguments: id (an integer of the enrollment ID to identify the enrollment object to update)
- Description: Allows an authorised employee to update one enrollment instance. 
- Authentication: @jwt_required()  
- Headers-Authorization: Bearer {Token}-only employees with admin access. 
- Request Body: Include any fields you wish to update:

```JSON
{
    "date": "2023-01-01",
    "subject_class_id": "09EE02-2023",
    "student_id": 1
}


```

- Request Response: (all fields are returned)

```JSON
{
    "id": 1,
    "date": "2023-01-01",
    "subject_class_id": "09EE02-2023",
    "student_id": 1,
    "student": {
        "id": 1,
        "user": {
            "title": "Miss",
            "first_name": "Isabelle",
            "middle_name": "Margaret",
            "last_name": "Smith",
            "email": "Isabelle.Smith@bgbc.edu.au",
            "phone": "0405301444",
            "dob": "2004-04-07",
            "gender": "female",
            "type": "Student"
        },
        "homegroup": "WH05",
        "enrollment_date": "2020-01-01",
        "year_level": 9,
        "birth_country": "Japan"
    }
}
```

If not authorised:  

```JSON
{
    "error": "You are not authorized to perform this action"
}
```

#### Methods:  ['Delete']

- Arguments: id (an integer of the enrollment ID of the enrolment instance to delete)
- Description: Allows an authorised user to delete one enrolment.
- Authentication: @jwt_required()  
- Headers-Authorization: Bearer {Token}- only employees with admin access
- Request Body: None

```JSON
{
    "message": "The student with student_id 1 was unenrolled from 09EE02-2023 successfully."
}
```

If not authorised:  

```JSON
{
    "error": "You are not authorized to perform this action"
}
```

If an enrolment with the ID doesn’t exist:

```JSON
{
    "error": "Enrollment not found with enrollment_id 10."
}
```
