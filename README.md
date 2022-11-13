# Our_School Web Server API Documentation

## [Github Repo](https://github.com/dayleclarke/api_webserver_project-)

## [Trello Board](https://trello.com/b/SUJE83TF/ourschooldb-webserver-api)

## [ERD](https://lucid.app/lucidchart/8c7b2138-1bf4-44a4-8c3d-8cfede79fa4d/edit?viewport_loc=-2112%2C-912%2C6656%2C3012%2C0_0&invitationId=inv_55dc587a-c01f-42cf-bde6-8dc2e6272728)

Table of Contents

- [Our_School Web Server API Documentation](#our_school-web-server-api-documentation)
  - [Github Repo](#github-repo)
  - [Trello Board](#trello-board)
  - [ERD](#erd)
  - [**Installation and Setup**](#installation-and-setup)
  - [**R1 and R2 Problem Identification and Justification**](#r1-and-r2-problem-identification-and-justification)
  - [**R3 Justification of the Database System**](#r3-justification-of-the-database-system)
    - [**Relational Database Management System (RDMS)**](#relational-database-management-system-rdms)
    - [**PostgreSQL**](#postgresql)
  - [**R4 Functionalities and Benefits of an ORM**](#r4-functionalities-and-benefits-of-an-orm)
  - [**R5 API Endpoints**](#r5-api-endpoints)
  - [**R7 Third Party Services**](#r7-third-party-services)
    - [SQLAlchemy](#sqlalchemy)
    - [Psycopg2](#psycopg2)
    - [Flask-Marshmallow](#flask-marshmallow)
    - [Python-Dotenv](#python-dotenv)
    - [Pip-Review](#pip-review)
    - [Flask-Bcrypt](#flask-bcrypt)
      - [Figure 1 Rainbow Table](#figure-1-rainbow-table)
    - [Flask-JWT-Extended](#flask-jwt-extended)
      - [Figure 2 Example JWT Token](#figure-2-example-jwt-token)
  - [**R6/R9 Explanation of ERD and Database Relations Implementation**](#r6r9-explanation-of-erd-and-database-relations-implementation)
  - [Entities](#entities)
      - [One-to-Many Relatinship Between Addresses and Users](#one-to-many-relatinship-between-addresses-and-users)
      - [Many to Many Relationship between Students and Carers](#many-to-many-relationship-between-students-and-carers)
      - [One to One Relationship between Users and Employees](#one-to-one-relationship-between-users-and-employees)
      - [Many to Many Relationship between Students and Subject Classes](#many-to-many-relationship-between-students-and-subject-classes)
      - [One to Many Relationship between Subjects and Subject Classes](#one-to-many-relationship-between-subjects-and-subject-classes)
      - [One to Many Relationship between Employees and Subject Classes](#one-to-many-relationship-between-employees-and-subject-classes)
  - [**R8 Project Models and their Relationships with Each Other**](#r8-project-models-and-their-relationships-with-each-other)
    - [Users Live at an Address](#users-live-at-an-address)
    - [Users can also be Employees or Students](#users-can-also-be-employees-or-students)
    - [Users (of the Caregiver type) care for Students](#users-of-the-caregiver-type-care-for-students)
    - [Students are Enrolled in SubjectClasses](#students-are-enrolled-in-subjectclasses)
    - [Teachers Teach SubjectClasses](#teachers-teach-subjectclasses)
    - [Subjects Have SubjectClasses](#subjects-have-subjectclasses)
  - [**R10 Planning and Tracking Tasks**](#r10-planning-and-tracking-tasks)
    - [Creating a Kanban Trello Board](#creating-a-kanban-trello-board)
    - [Writing User Stories](#writing-user-stories)
    - [Adding Prioritisation, Timeframes and Labels](#adding-prioritisation-timeframes-and-labels)
    - [Adding Assessable Elements](#adding-assessable-elements)
    - [Writing Daily Stand-Ups](#writing-daily-stand-ups)
  - [Reference List](#reference-list)

<br>

## **Installation and Setup**

Locate the folder where you would like to save the API. Then when you are inside the folder Clone the repository from Github.

Connect to a PostgreSQL database from the Flask application. Run the PostgreSQL prompt in the terminal:

```SQL
psql 
```

Create the database:

```bash
CREATE DATABASE our_school_db;
```

Connect to the database:

```bash
\c our_school_db;
```

Create user and set a temporary password such as:

```bash
CREATE USER api_dev WITH PASSWORD 'password123';
```

Grant this user priviliges:

```bash
GRANT ALL PRIVILEGES ON DATABASE our_school_db TO api_dev;
```

Open another WSL command line and run the following commands:

To create and activate a virtual environment:

```bash

python3 -m venv .venv

source .venv/bin/activate

```

Install dependant packages:

```bash
pip install -r requirements.txt
```

Rename the .env.sample to .env and set the database connection stream and the JWT secret key. For example:

```
DATABASE_URL=postgresql+psycopg2://api_dev:password123@127.0.0.1:5432/our_school_db
JWT_SECRET_KEY=Example Key
```

Create and seed the database then run the Flask application with the following cli commands:

```bash
flask db create
flask db seed
flask run
```

This should allow you to open 127.0.0.1:8080/ on your browser or through [Postman](https://www.postman.com/). See possible routes and end points available here [API End Points](end_points.md)

## **R1 and R2 Problem Identification and Justification**

The problem being solved by this application is the need for a secure way of storing reliable, up-to-date personal information (including contact information) about school community members. This information needs to be readily available and accessible to those who need it quickly and easily. This is required to establish and maintain effective communication among the key stakeholders in the school community including teachers, support staff, caregivers, and students.  While many schools have sophisticated database management systems implemented already to store this information, some schools (particularly small schools in regional areas) do not.

Teachers, for example, need a way to locate caregiver contact information quickly and easily.  This allows them to establish and build effective communication, understanding and trust with a child’s support network.  They can then work in partnership towards improving the academic success and holistic wellbeing of each student (Seitsinger, Felner, Brand, & Burns, 2018). Kraft and Dougery (2013) found that frequent teacher-family communication increased student classroom engagement, organisation, and homework completion by 15%, 35% and 40% respectively.  Teacher-family communication also promotes a students’ sense of competence and enhances their feelings of relatedness to the teacher and school.

Teachers juggle an ever-expanding workload, with high rates of burnout.  Visentin (2022) stated that  92% of teachers across Australia felt they did not have enough time to prepare for their core teaching duties. An application is required to make caregiver contact information quickly accessibly by teachers. This will reduce the activation energy required to reach out to parents. If contact information is not up-to-date, accurate and readily available, it is likely that this communication will not occur as other pressing matters arise. Teachers also frequently work from home, outside of school hours so having this information available online is important.

This application makes it easy for teachers to see the contact information of caregivers so they can reach out to parents via the communication means that suits the purpose and individual.  For example, an email address is included so that commendations can quickly sent home to reinforce and encourage positive behaviours. The email address can also be used to send missed assessment notices home to inform parents when their child has missed an exam or draft/assignment deadline. Phone numbers are also included allowing teachers the option of calling parents in real time to discuss behavioural or other concerns.

School administrative officers also need to be able to store and retrieve accurate and up to date student and caregiver contact information.  This application makes it easy for them to quickly access this information to send school correspondence (such as report cards, excursion permission slips and school calendars) to students and/or parents. Students and parents also need a way to ensure that the information in the system is accurate and up to date.
Furthermore, this application allows staff to quickly see which teachers a student currently has and how to contact them. This allows learning support staff, guidance officers or heads of house to reach out with information teachers need to know about the students in their classroom.  For example, if a student was currently facing a significant loss that would impact their behaviour and engagement.

Teachers also require information to be stored about the students they teach.  This allows them to establish rapport and better meet the learning needs of individual students in the classroom. Future iterations of this application will include additional information about students such medical conditions, allergies, assessment results, grade point averages, preferred learning styles, learning needs, classroom seating requirements, leadership capabilities, character strengths and behaviour/attendance records. While important these are outside the scope of this project.

The problem with storing information of such a private and sensitive nature is that there is a risk of unauthorised access, modification, or disclosure of information. This application is needed to store this information in a secure way to maintain confidentiality. Information should only be accessible to those who own the information or individuals who require access to perform their duties. This application solves the problem of maintaining confidentiality and integrity through authentication and authorisation. Authentication was achieved through implementing JSON Web Tokens and verifying the user's credentials in the form of a username and password. JWT is open standard, self-contained, compact, secure, and scalable (Okta, 2022). Information can be verified and trusted due to the use of digital signatures using a secret key. This helps ensure the person accessing the information is who they present themselves to be. Each individual user’s identity can be accessed via the JWT token which allows the application to serve resources to specific users.  This allows users to access their own information and the information they require to perform their duties. There is also information that is only accessible to employees with admin rights.  This improves security, scalability and allowin schools to meet their legal oblgatations as per the The Privacy Act 1988 (Cth) (Andress, 2019).

## **R3 Justification of the Database System**

There are many different database management systems available to chose from each with distinct advantages and disadvantages and suitable for different situations.  To ensure the most appropriate database management system was selected an analysis was conducted into alternative options.  A comprehensive analysis of the chosen system was developed as shown in table 1 and 2 below.

### **Relational Database Management System (RDMS)**

A Relational Database Management System (RDMS) was chosen as they make it easy to group data into clearly defined categories (entities) and efficiently establish relationships between those entities (Microsoft, 2022).  Data can be stored in a structured organised manner and users can quickly and easily complete complex queries on the database (Dolphin, 2022).  This is a key advantage as the data stored in Our_School_db has a consistent structure and has clear relationships (such as the relationship between student, parent, and teacher) Entity, referential and domain integrity is also easily achieved through primary and foreign keys, normalisation, and data validation rules.

While RDMS doesn’t provide as much flexibility as non-relational databases the data being stored in this application has consistent attributes and benefit from the domain integrity achieved by a more rigid schema.  This disadvantage is also less of a concern as the overall structure of the data across all tables in this database is unlikely to change over time  (Dolphin, 2022).

Another drawback of this system is that objects in a programming language must be converted to and from the database storage format, but this can be achieved with the use of an object relational mapper. Finally, while alternatives such as NoSQL are better at scaling horizontally and partition tolerance this is achieved by compromising consistency and referential integrity (which are both important for this application)  (Hevo Data Inc, 2022).

![Table 1: Analyis of RDMS](./docs/analysis_of_rdms.jpg)

### **PostgreSQL**

PostgreSQL was chosen as the specific database system for this application because it is a robust and powerful, enterprise class, object-relational database system commonly used as a back-end database for web applications.  It has many significant advantages that make it highly suitable for this application (see table 2 below). A key deciding factor was that it is free to use and open source. This makes the app more affordable which is important for schools as they typically have strict budgeting requirements.  Furthermore, it has a 30-year development history with a reputation for reliability, robustness, extensibility, and data integrity (The PostgreSQL Global Development Group, 2022).

It is also popular with 44% of professional developers using the system in 2021 (StackOverflow, 2021). Because of this the software is well maintained, documented, and supported with a dedicated community consistently delivering performance and innovative solutions. The system is also scalable and highly suitable for large databases (Peterson, 2022).  This is an important factor for this application as schools can vary significantly in size and grow over time. For example Queensland has more than 100 schools with fewer than 20 students but Brisbane State High School  (BSHS) is Queensland's, and Australia's, largest state secondary school with over 3,000 students  (The State of Queensland- Department of Education, 2022).  PostgreSQL can manage thousands of terabytes of data and process 100 thousand queries per second which is well above the capabilities of what is required for this application. Additionally, it offers multi-version concurrency control allowing multiple teachers and school administrators to access the database simultaneously.  Furthermore, it allows complex queries which can be a significant advantage when gathering assessment results data to analyse student, subject, and class performance over time (Peterson, 2022).

While the speed and performance of PostgreSQL is not as high as competitors such as MySQL this is not as important for the application as other factors such as cost, reliability, robustness, and data integrity. Another drawback is that PostgreSQL’s expandable documentation is typically only available in English.  This is not as impactful on this application as it is targeted towards Queensland schools and the 2021 Census revealed the 91.1% of Australians considered themselves to be proficient in English.  Any users needing to review this documentation would likely be able to read English.   Finally, the installation and configuration processes are often considered more complex compared with MySQL and with other systems.  These processes however are still very achievable, well documented, and only a short-term drawback (Ionos, 2022) (Peterson, 2022).

![Table 1: Analyis of PostgreSQL](./docs/analysis_of_postgresql.jpg)

## **R4 Functionalities and Benefits of an ORM**

An  Object Relational Mapper (ORM) can be used to provide a layer that connects object oriented programming (OOP) to relational databases without having to write Structured Query Language (SQL) queries. SQL is a standard language for accessing and manipulating databases. An ORM allows data to be converted between the storage format used in the program (in this case Python objects) and the relational schema of the database (tables with columns and rows). This allows developers to interact with the database using their programming language of choice instead of SQL.

This application has used the SQLAlchemy as an ORM.  This is a well-regarded database toolkit and ORM written in Python. It provides a generalized interface for creating and executing code that is database-agnostic without writing SQL statements.

ORMs generate objects which map to tables in the database virtually. In this application a model has been created for each entity in the database.  This provides an abstract representation each table. A model is a class that represents a table where each class attribute is a field (column) of the table. Additionally, ORMs track object changes and synchronize those changes back to the database. ORMs generate the SQL code for a relational database to insert, update, create and delete data in response to changes the application makes to the model (Liang, 2021).

The ORM encapsulates the code needed to query and manipulate the data, removing the need to write SQL queries and type converting data to and from the database. Queries are instead written in Python (by calling methods on a class), and then the ORM can sanitise the incoming data to ensure it doesn’t contain anything malicious.  It translates the query to SQL and retrieves the result as an object  (Liang, 2021).

Another key functionality of SQLAlchemy is that it can be used to map relationships between classes to relationships between tables using foreign key constructs. SQLAlchemy supports four types of relationships: One To Many, Many To One, One To One, and Many To Many. ORM enables cascade behaviour to be mapped when using relationship() constructs. When operations are performed on parent objects, child objects get updated or deleted as well depending on the behaviour chosen.

Sessions provide consistency and are another key functionality of an ORM. A session acts as a “holding zone” for all conversations with the database. The ORM objects themselves that are affected by the transaction are maintained inside the session. These will be committed to the underlying database together, or none of them will.

Even when using an ORM knowing SQL is important. A database may need to be queried directly while in development and when debugging and testing. SQL provides more control over the application and SQL queries may need to be fine-tuned to optimise performance. Additionally complex queries may not be solved with ORMs, requiring embedded SQL.

An alternative to using an ORM tool is that raw SQL code could be written to provide a direct interface between the application and the database. This provides more detail and flexibility than an ORM abstraction. However, is requires in-depth database knowledge and the ability to code in SQL. Furthermore, writing data-access code is time-consuming and misses out on many of the advantages an ORM provides.

Benefits of an ORM

- Security is improved. ORM tools can be used to sanitise the incoming data improving data integrity and preventing SQL injection attacks.
- Less and cleaner code compared to embedded SQL (using SQL directly would result in more grunt work and boiler plate code).  
- Speeds up development time and costs.
- Can be used to track database changes making it easier to debug and change the application in the future.
- High level implementation with excellent support for tasks like transactions, connections, migrations, seeds, streams and many more.
- Simpler implementation (than embedded SQL) as there is no need to convert from the table to the object and vice versa.
- ORM’s abstracts away the database system making it easier to migrate to another database (PostgreSQL could be later changed to MySQL)  It also supports multiple database platforms which is beneficial if the API was sold for distribution in on-premises solutions
- ORMs promote code maintainability and reuse, as they enable developers to think in terms of objects instead of atomized pieces of data.
(Abba, 2022) (Hoyos, 2018) (Liang, 2021)

## **R5 API Endpoints**

The endpoints of this API are documented here [API End Points](end_points.md)

## **R7 Third Party Services**

Flask is the web application framework used to build this RESTful API. Flask provides basic routing with requests, responses, and a development server. There are numerous high-level components which work together to produce a fast, performant, and scalable API.  It is a micro framework and additional functionality can be added with packages. It is agnostic in that the framework’s major components can be swapped out for alternatives which provides flexibility and choice in terms of how the server is designed (Pallets, 2010).  The following third party PyPi packages have been used in this project. A full list of dependancies and requirements can be found here: [Requirements.txt](src/requirements.txt)

### SQLAlchemy

This application has used SQLAlchemy as an ORM.  This is a well-regarded database toolkit and ORM written in Python. It allows the app to connect to PostgreSQL.  It encapsulates the code needed to query and manipulate the data, removing the need to write SQL queries and type converting data to and from the database. Queries are instead written in Python (by calling methods on a class), and then the ORM can sanitise the incoming data.  It translates the query to SQL and retrieves the result as an object.

### Psycopg2

Psycopg2 was used as an adaptor between the PostgreSQL database and the flask application. SQL Alchemy is database agnostic, so it requires another package (specific to the database style used) to interact with the database which acts as a driver/adaptor (SQLAlchemy, 2022).

### Flask-Marshmallow

Used to convert complex datatypes, such as objects, to and from native Python datatypes. Marshmallow schemas have been used to:

- Validate input data.
- Deserialize input data to app-level objects.
- Serialize app-level objects to primitive Python types. The serialized objects can then be rendered to JSON for use in the HTTP API. (Pallets, 2010).

### Python-Dotenv

Python-Dotenv is used to set environment variables defined in the files “.env” and “.flaskenv” files. The .flaskenv file contains information about how to run the project such as where to run the application from, the port number and whether to run the application in debug mode. The .env file is used to contain configuration information that is sensitive such as the database connection stream as this contains a password and the JWT secret key (Pallets, 2010). This is more secure that hard coding them into the application.  

### Pip-Review

Pip-review (a standalone convenience wrapper around pip)was used to automate the process of updating packages using pip. The command pip-review can be used to list available updates on the Python Packages Index. Pip-review -aC can be used to check if a newer version is available and install it in the current python environment.

### Flask-Bcrypt

Flask bcrypt is a flask extension used to protect passwords using bcrypt hashing based on the Blowfish cipher. This involves transforming a string of characters (of any length) into a fixed-length value. The hashing function will always produce the same output given the same input. Changing even one character in the original string will significantly change the resulting hash. It also incorporates salt for protecting the application against any rainbow table attacks. A rainbow table contains a series of precomputed hash values which could be used to find commonly used passwords (as shown in figure 1 below).  To overcome this issue a “salt” (a random value) is added to the original message before it's hashed (Okta, 2022).  Bcrypt hashing functions can be deliberately made slower to prevent brute force attacks.

```py
password = bcrypt.generate_password_hash(request.json['password']).decode('utf8')
```

![Figure 1 Rainbow Table](docs/rainbow_table.png)

#### Figure 1 Rainbow Table

### Flask-JWT-Extended

The JWT Extended library has been used to implement JSON Web Tokens (JWT) authentication in the API. JWT involves the server verifying the user's credentials and sending back an encrypted token to the client. The token is stored (ideally in session storage) and added as an authorization header for  subsequent requests.  This is critical to protect personal information from unauthorised access. JWT is suitable because it is open standard, self-contained, compact, secure, and scalable (Okta, 2022). Information can be verified and trusted due to the use of digital signature using a secret key. (Andress, 2019). This helps ensure the person accessing the information is who they present themselves to be. Each individual user’s identity can be accessed via the JWT token which allows the application to serve resources to specific users.

It can be used to prevent a user from needing to login at each request.  Create_access_token() can be used to make JSON Web Tokens, jwt_required() to protect routes, and get_jwt_identity() to get the identity of a JWT in a protected route

![Figure 2 Example JWT Token](docs/example_jwt_token.jpg)

#### Figure 2 Example JWT Token

## **R6/R9 Explanation of ERD and Database Relations Implementation**

The following ERD was created to better understand the foundations of the data and information that to be stored within the database including the entities, attributes and relations required.
![ERD](docs/ERD.jpg)

## Entities

The following provides a list of entities tracked by the application.  Note that each table also has a primary key called id which is used to uniquely identify that table in addition to the attributes described below.

**Users:**  to store information about all key stakeholders in the system. This will have attributes about the user (such as their name, gender, date of birth) and the type of user that they are (either caregiver, student, employee or other). Contact information will also be tracked  such as their phone number, email, and an address id (which is a foreign key linking to the addresses table).  It will also contain a password which along with their unique user id allows them to access the system.

**Addresses-** To achieve the second form of normalisation all columns in a table must depend on the table's primary key. For this reason, the user’s address information was taken out of the user’s table and stored in a separate addresses table. Each column represents a single piece of address information (such as a complex number, street number, street name, suburb, and postcode).

Each user can have zero to one address stored in the database. Each address however can belong to many users.  This is common in schools as parents and students (including student siblings) will often live at the same address.  While users may live at multiple addresses (such as students with separated parents) the decision was made to store only one address to streamline communication and make it clear where physical mail should be sent. This means a one-to-many relationship needs to be established as shown below:

![One-to-Many Relatinship Between Addresses and Users](docs/users_addresses.jpg)

#### One-to-Many Relatinship Between Addresses and Users

**Students-** to track extra personal information specific to students.  This will store information such as their id, homegroup, enrolment date, year level and birth country. This will provide extra information about them in addition to the details tracked in the user’s table. A foreign key of user id is also required to relate this table to their other information stored in the user table.  This will require a one-to-one relationship to be established.  One user can have zero to one student information stored about them and each student will have exactly one entry in the user’s table to store their personal information (as shown in green in the image below).

**Student_relations-** to track the relationships between students and their family members or caregivers. This will have a foreign key linking to the information about the student and another foreign key linking to details about the relative or caregiver. An attribute is added to track the relationship the carer has to the student such as parent, sibling, stepparent, temporary carer etc. A Boolean is_primary_contact is also included so that stakeholders know who to contact in the first instance. For example, if an excursion letter needed to be sent home it would be sent to the primary contact, this would also be the first person contacted in an emergency. The student_relations table is an intermediary table connecting students and their carers. This is required because one user can care for zero-to-many students and each student can have one-to many-caregivers.

Using this join table means that instead of a many-to-many relationship there will be two separate one-to-many relationships established. Each student_relations record will relate to exactly one student and each student can have one to many career relationships recorded (as shown in yellow below). At least one career is required so that the school knows who to contact in an emergency or to discuss the student’s learning needs etc. Additionally, each student_relations record will relate to exactly one career (stored as a user) and each user can be a career to zero or many students (shown in blue below). Zero because not all users are carers and many because siblings will typically attend the same school leading to one carer caring for multiple students at the school.

![Many to Many Relationship between Students and Carers](docs/students_caregivers.png)

#### Many to Many Relationship between Students and Carers

**Employees-** to track extra information specific to employees.  This will store information such as their id, hired_date, job_title, department and a Booleon attribute to indicate if they have administrative access to the database. This will provide extra information about them in addition to the details tracked about them in the user’s table. A foreign key of user_id is also required to relate this table to their other information stored in the user’s table.   This will require a one-to-one relationship (as shown in blue below).  One user can have zero to one employee information stored about them (not all users are employees) and each employee will have exactly one entry in the user’s table to store their personal information (each employee must also have information about them stored in the users table).

![One to One Relationship between Users and Employees](docs/users_employees.png)

#### One to One Relationship between Users and Employees

**Subjects-** to track each of the subjects offered at the school .  This will include details about the name of the subject, the year level, department and the maximum number of students permitted in each class. This is required as some subjects such as year 12 classes require smaller class sizes.  A semantic string for subject id was used instead of an automatically generate series to uniquely identify each subject.  This is comprised of two numbers to indicate the year level and three letters to indicate the subject code.  This is a typical identification system used in schools across Queensland.

**Subject_Classes-** to track each individual school class. Because there is a maximum class size several different classes are typically offered for each subject depending on the number of students wishing to study that course. This entity will track attributes such as the room and timetable line. Again, a semantic string for class id was used instead of an automatically generated series to unique identify each class.  This is comprised of the subject id followed by a 1–2-digit number and the school year the class is occurring in.  There will also be a foreign key teacher id linking to the information about the teacher of that class.  

This involves a one-to-many relationship (shown in blue below), as each class is taught by exactly one teacher, but each teacher can teach zero to many classes.  In this version of the application team teaching is not permitted (this may be added in future iterations and would involve adding a join table to handle the many-to-many relationship).

This table also has a foreign key subject id. This provides a link to the subject table with a one-to-many relationship (shown in pink below). Each subject can have zero to many classes, but each class covers exactly one subject.

**Enrolments-** to track which students are enrolled in which classes. This is an intermediary table between students and classes. It is required because one class can be taken by zero to many students and each student can take zero to many classes which is a many-to-many relationship. The Enrolments entity has a foreign key student id to track information about the student.  This is now a one-to-many relationship as each enrolment relates to exactly one student and each student can have zero to one enrolment.  There is also a foreign key class id which provides information about the class they are enrolling in.  This is a one-to-many relationship as each enrolment relates to exactly one class, but each class can have zero to many enrolments.

![Student, Enrollment, Class, Subject and Employee Relatinships](docs/subjects_classes_students_employees.jpg)

#### Many to Many Relationship between Students and Subject Classes

#### One to Many Relationship between Subjects and Subject Classes

#### One to Many Relationship between Employees and Subject Classes

## **R8 Project Models and their Relationships with Each Other**

This application follows the MVC architectural pattern as it is split into specific sections that all have their own purpose. All models are stored in a separate model’s folder. Models store data (and its related logic) and are the only object that interact directly with the database (Pallets, 2010). Models help the controller retrieve all the information it needs from the database. The controller then interacts with the view to render the information back to the user. (Real Python, 2014).  

A model was created for each entity in the database to provide an abstract representation each table. A model is a python class that represents a table where each class attribute is a field (column) of the table.  This class inherits from the db.Model. Columns contain information such as a name, datatype, constraints, primary key and foreign key. When the cli command db create is run, for example it will execute all the methods in the model.  This will result in an SQL create query which it then executes against the database.

### Users Live at an Address

The first model created was the User model as explained below:

```py
class User(db.Model):
    __tablename__ = 'users' # This names the table (otherwise SQLAlchemy will name it after the class which is singular: User). Tables names should be plural as they store data on multiple users. 

    # The following class attributes are defined to represent a field (column) of the table.   Here we include information such as a name, datatype, and constraints.  

    id = db.Column(db.Integer, primary_key=True) # This is the primary key which is a required unique identifier allowing row differentiation.
    title = db.Column(db.String(50)) # to store honorific titles
    first_name = db.Column(db.String(50), nullable= False) # Nullable = False means that the attribute cannot be left null. Each user must have a first name listed.
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable= False)
    password = db.Column(db.String, nullable= False)
    email = db.Column(db.String(100), unique=True, nullable= False) # Unique = True means no two users are permitted to have the same email address. Each instance of the user model must have a unique email attribute. 
    phone = db.Column(db.String(20), nullable= False)
    dob = db.Column(db.Date) 
    gender = db.Column(db.String(50))
    type = db.Column(db.String(9), nullable= False)
    
```

The user class is linked to the addresses table by the foreign key addresses id. User represents the child side of the one-to-many relationship as each user has only one address, but each address can belong to multiple users.  The following code was added to the user’s model to link to the id of the addresses model (which is that model’s primary key).  Relationship() takes numerous parameters. The first parameter indicates which other model (class name) it relates to as a string. 'Address' will encapsulate data from the Address model.  This allows an address object to be provided for each user. The second parameter back_populates is used to specify the other side of the relationship. It adds a field to each address called 'user' that will return the entire user object for an address.

```py
address_id = db.Column(db.Integer, db. ForeignKey ('addresses.id')) 
address = db.relationship('Address', back_populates='user')
```

As previously stated, this app utilises Marshmallow to allow SQLAlchemy models (returned when querying the database) to be converted into JSON. An instance of the Marshmallow object that runs with the Flask app is required along with schemas to define which model fields are to be converted (Pallets, 2010). An address object cannot be JSON serialized directly. Marshmallow needs to be told what schema to use to process the address attribute so that it can be represented as a nested field.

```py

class UserSchema(ma.Schema):
address = fields.Nested('AddressSchema') # When it needs to process address it should process it as a nested field using the Address Schema.  

    class Meta:
        fields = ('id', 'title', 'first_name', 'middle_name', 'last_name', 'password', 'email', 'phone', 'dob', 'gender', 'type', 'address')
        ordered = True # puts the keys in the same order as the fields lists above otherwise it will be alphabetical order. 
```

An addresses model and schema are also required. While there is no foreign key in the addresses table, relationship() is specified on the address as shown below. The first parameter ‘User’ indicates which model it relates to.  This allows a list to be provided of all the users who live at each address. Each element in the list will be a user object (an instance of the user model).Back_populates is again used to specify the other side of the relationship. It will add a property to User called address that will return the entire address object for a user.  

Here cascade delete was not set because if an address is deleted, any users who have that address listed should NOT be deleted. By leaving this parameter out  if the address is deleted it will de-associate each user from the address by setting their foreign key reference to NULL.

```py
user = db.relationship('User', back_populates='address')     
 ```

### Users can also be Employees or Students

As previously stated, there are separate tables to store additional information about employees and students. This requires a one-to-one relationship between user and student and user and employee.   One user can have zero to one employee (or student) information stored about them (not all users are employees/students) and each employee (or student) will have exactly one entry in the user’s table to store their personal information (each employee/student must also have information about them stored in the users table).

Relationship() is specified on the user to link the user to the employee model (and another to link to the student model) as shown in the code snippet below. Again the first parameter indicates which model it relates to.  This allows an employee object (or student object) to be provided for a user.

Back_populates is again used to specify the other side of the relationship. It will add a property to employee called user that will return the entire address object for a user.  Cascade all delete was added which means that if a user is deleted their related resource in the employee or student table will also be deleted.  Uselist=False was added here because this is a one-to-one relationship, and this indicates the result is a single object (rather than a list).  

```py
employee = db.relationship('Employee', back_populates='user', cascade='all, delete', uselist=False)
student = db.relationship('Student', cascade='all, delete', uselist=False)
```

Both employee and student fields are then added to the users schema. Again because these student and employee objects cannot be JSON serialized directly  Marshmallow needs to be told what schema to use to process each of these attributes so that it can be represented as a nested field. Note that the user details need to be excluded to avoid a RecursionError.

```py
class UserSchema(ma.Schema):
address = fields.Nested('AddressSchema') 
student = fields.Nested('StudentSchema', exclude=['user']) # When it needs to process student it should process it as a nested field using the student Schema.  
employee = fields.Nested('EmployeeSchema', exclude=['user'])

    class Meta:
        fields = ('id', 'title', 'first_name', 'middle_name', 'last_name', 'password', 'email', 'phone', 'dob', 'gender', 'type', 'address')
        ordered = True 
```

The other side of the relationship also needs to be established in the employees model by adding a foreign key user_id linking to the user’s table and specifying the relationship(). Foreign key constraints were added to prevent it from being null and requiring a unique entry. This means that each employee must have a related user and each user can relate to zero or one employee.  

```py
user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True) 
user = db.relationship('User', back_populates='employee')
```

This was also done in the students model:

```py
user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True) 
user = db.relationship('User', back_populates='student')
```

Again the schemas for both models need to be updated to include a user. This time password should be excluded for security reasons (even though it is hashed) and the other table because if they are a student, they will not have details in the employee able and this would be null.

This is how it would appear in the StudentSchema (employee would be the same):

```py

 user = fields.Nested(UserSchema, exclude= ['password', 'employee', ‘student’]) # When it needs to process user it should process it as a nested field using the UserSchema.  
```

### Users (of the Caregiver type) care for Students

As previously stated, the StudentRelations model will act as a join table between Students and their Caregivers (a type of User). To represent the one-to-many relationship between students and student_relations a foreign key of students.id is set up in the StudentRelations model. In a similar way a foreign key is set up for user.id (linking the Users and StudentRelations). As shown below the student_id and user_id cannot be null because each student_relationship must relate to a specific student and caregiver. The relationship() is also specified to define each relationship. This allows a student object to be provided for each student_relation.  

As you can see student and user are singular as each student_relation only relates to one student and caregiver. Student_relations however is plural as both students and caregivers can have multiple student_relations.

```py

class StudentRelation(db.Model):
    __tablename__ = 'student_relations' # Renames the table to be plural

    id = db.Column(db.Integer, primary_key=True) 
    relationship_to_student = db.Column(db.String(50))
    is_primary_contact = db.Column(db.Boolean)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    
    user = db.relationship('User', back_populates='student_relations')
    
    student = db.relationship('Student', back_populates='student_relations')
```

Both user and student fields are then added to the StudentRelationsSchema. Again because these student and employee objects cannot be JSON serialized directly Marshmallow needs to be told what schema to use to process each of these attributes so that it can be represented as a nested field.  Note specific fields are excluded to avoid a RecursionError and the duplication of data.  This can be either achieved by specifying the fields to exclude or which ones to include.

```py
class StudentRelationSchema(ma.Schema):
    user = fields.Nested('UserSchema', exclude= ['password', 'employee', 'student'])
    student = fields.Nested('StudentSchema', only = ['user.first_name', 'user.last_name'])
    
    class Meta:
        fields = ('student', 'user', 'relationship_to_student', 'is_primary_contact')
        ordered = True 

```

The other side of the student/student_relations relationship is the defined in the Student model:

```py
student_relations = db.relationship('StudentRelation', back_populates='student', cascade= 'all, delete') # If a subject is deleted all the subject_classes of that subject will also be deleted. 
```

The StudentSchema is then updated to allow the student_relations object to be JSON serialized.  Marshmallow needs to be told to use the StudentRelation schema to use to process the student_relations attribute so that it can be represented as a nested list of all the student’s relations. Each element in the list is a student_relations object.  Again student and the user’s student relations are excluded to avoid duplication of data.

```py
student_relations = fields.List(fields.Nested('StudentRelationSchema', exclude = ['student', 'user.student_relations']))
The other side of the user/student_relations relationship is the defined in the User model:
student_relations = db.relationship('StudentRelation', back_populates='user', cascade= 'all, delete')
# If a subject is deleted all the subject_classes of that subject will also be deleted. 
```

The UserSchema is then updated to allow the student_relations object to be JSON serialized.  Marshmallow needs to be told to use the StudentRelation schema to use to process the student_relations attribute so that it can be represented as a nested list of all the users student relations. Each element in the list is a student_relations object.  User is excluded to avoid duplication of data.

```py

student_relations = fields.List(fields.Nested('StudentRelationSchema', exclude = ['user']))
```

### Students are Enrolled in SubjectClasses

As previously stated, the enrolments model will act as a join table between students and subject classes. To represent the one-to-many relationship between students and enrolments a foreign key of students.id is set up in the enrolments model. In a similar way a foreign key is set up for subject_class.id (linking enrolments and subjects). As shown below the student_id and subject_class_id cannot be null because each enrolment must relate to a specific student and subject_class.

The relationship() is also specified to define each relationship. This allows a student object (and a subject_class object) to be provided for each enrolment.  As you can see student and subject class are singular as each enrolment only relates to one student and subject_class. Enrolments however is plural as both students and subject_classes can have multiple enrolments.

```py

subject_class_id = db.Column(db.String(15), db.ForeignKey('subject_classes.id'), nullable=False)
student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)

subject_class = db.relationship('SubjectClass', back_populates='enrolments')
student = db.relationship('Student', back_populates='enrolments')
```

Again the EnrolmentsSchema is updated to include a student and a subject field. This tells Marshmallow to process student as a nested field using the StudentSchema and subject_class as a nest field using the SubjectClassSchema.

```py
subject_class = fields.Nested('SubjectClassSchema')
student = fields.Nested('StudentSchema', only = ['user.first_name', 'user.last_name'])
```

The other side of the relationship is the defined in the Student model:

```py
enrollments = db.relationship('Enrolment', back_populates='student', cascade= 'all, delete') # If a student is deleted all their enrolments need to be deleted too. 
```

And also in the SubjectClassModel:

```py
enrollments = db.relationship('Enrollment', back_populates='subject_class', cascade= 'all, delete') # If a subject_class is deleted all the enrolments in the class will also be deleted. 

```

The SubjectClassSchema was then updated to include a nested list of enrolments using the EnrolmentSchema. This will allow a nested list of enrolments to be displayed. The list will only include the student details from the enrolment schema as this is the only information the app needs to access about the enrolments in each subject.  

```py
    enrolments = fields.List(fields.Nested('EnrolmentSchema', only = ['student'])
```

### Teachers Teach SubjectClasses

To represent the one-to-many relationship between the Employees and SubjectClass models a foreign key of employee.id is set up in the SubjectClass model. The relationship() is also specified to allow an employee object to be provided for each SubjectClass.  As you can see employee is singular as each class only has one teacher. Subject_classes however is plural as each employee can teach multiple classes.

```py
employee_id = db.Column(db.Integer, db.ForeignKey('employees.id') ) 
employee = db.relationship('Employee', back_populates='subject_classes')
```

The SubjectClassesSchema is updated to include an employee field. This tells Marshmellow to process employee as a nested field using the EmployeeSchema. Only the user’s first and last name is included to reduce unnecessary and duplicate data. Employee is also then added as a field with the list of fields.

```py
employee = fields.Nested('EmployeeSchema', only=['user.first_name', 'user.last_name'])
```

The other side of the relationship is the defined in the Employees model:

```py
subject_classes = db.relationship('SubjectClass', back_populates='employee', cascade='all, delete') 
```

A subject_class field is then added to the EmployeeSchema. This will allow a nested list of SubjectClass objects to be displayed, although only the subject_id and subject name will be included to reduce data duplication.

```py
subject_classes = fields.List(fields.Nested('SubjectClassSchema', only=['id','subject.name']))
```

### Subjects Have SubjectClasses

To represent the one-to-many relationship between the Subject and SubjectClass models a foreign key of subject.id was set up in the SubjectClass model. Note that nullable is set to False because each class must relate to a subject.  The relationship() is also specified to allow a subject object to be provided for each SubjectClass.  As you can see subject is singular as each class only relates to one subject. Subject_classes however is plural has each subject can have multiple classes.

```py
subject_id = db.Column(db.String(15), db.ForeignKey('subjects.id'), nullable=False)
subject = db.relationship('Subject', back_populates='subject_classes')
```

Again the SubjectClassesSchema is updated to include a subject field. This tells Marshmellow to process subject as a nested field using the SubjectSchema. Subject is also then added as a field with the list of fields.

```py
subject = fields.Nested('SubjectSchema', exclude=['subject_classes'])
```

The other side of the relationship is the defined in the Subject model:

```py
subject_classes = db.relationship('SubjectClass', back_populates='subject', cascade='all, delete') # If a subject is deleted all the subject_classes of that subject will also be deleted. 
```

And added to the SubjectSchema. This will allow a nested list of SubjectClass objects to be displayed.

```py
subject_classes = fields.List(fields.Nested('SubjectClassSchema', exclude=['subject']))
```

## **R10 Planning and Tracking Tasks**

### Creating a Kanban Trello Board

Trello was used to plan and track tasks for this project.  This allowed work streams to be defined in lists, and user stories and Kanban methodology were implemented.  The Trello workspace was divided into 5 lists:

- **Backlog:** A prioritised list of unplanned tasks that I intended to spend time on but hadn't started yet. This was the staging area where specs got fleshed out. They are not in the current implementation plan. My project got out of scope quickly so tasks that were out of the scope of this implementation went here.  Future iterations of this application will include additional information about student such medical conditions, allergies, assessment results, grade point averages, preferred learning styles, learning needs, classroom seating requirements, leadership capabilities, character strengths and behaviour/attendance records.
- **To-do-** A prioritised lists of planned work that is ready to be done.
- **Doing-** A task currently being worked on. This would have been more beneficial when working in a team as the entire team can immediately see who is working on what. It was still useful for me to ensure I didn’t have too many ongoing tasks at the one time. I also stored tasks here that needed to be completed on an ongoing bases such as commenting source code.
- **Testing-** Tasks that have been completed but require testing/review.
- **Done-** All completed tasks

I began the project by creating the Trello board workspace using the Kanban template. I added the first three introductory tasks.

![Introductory Trello Tasks](docs/Trello1.png)

### Writing User Stories

After these three tasks were completed user stories were written. This allowed me to determine the key tasks that needed to be performed to create this application. Each of these short, written explanations outlined a particular user’s need outlining what their role is, the action they need to perform and why. As per Agile methodology they were expressed from the user’s perspective and were used to help establish small units of work to be performed. These user stories informed what data and information would need to be stored in the database and the routes/end points that would be required (Agile Alliance, 2022). This helped to ensure the application delivered the highest value for the end user by ensuring their core needs we met and kept the end user/customer top of mind. In the future I would write these before documenting the problem and writing the ERD.

### Adding Prioritisation, Timeframes and Labels

After writing these user stories I wrote a checklist of tasks that needed to be completed for each user story. I ensured that each task was specific, actionable, and achievable. I assigned dates to tasks and put them in order of priority. I also added labels to document categories like userstory, planning, README and coding.

![Teacher User Stories](docs/teacher_user_stories.png)
![Other Staff User Stories](docs/other_staff_user_stories.jpg)
![Student User Stories](docs/student_user_stories.png)
![Other User Stories](docs/other_user_stories.png)

### Adding Assessable Elements

Because this is an assessment task, I also added tasks that needed to be completed to meet assessment requirements outlined in the rubric. This allowed me to mark tasks as complete as I progressed throughout the assignment and know at any point what work needed to be completed by the final due date.

![Trello Board Tracking](docs/trello_board_tracking.jpg)
![Trello Board Tracking](docs/trello_board_checklists.jpg)

### Writing Daily Stand-Ups

Another way I tracked my progress was through daily stand ups with my peers on Discord. This involved briefly explaining what work was completed in the last 24 hours, tasks that are upcoming, any blockers/issues I faced and what I had learnt.  It was rewarding to look at how much I had achieved in the 24 hour time frame and I found it useful to set a goal for what I wanted to achieve for day. This motivated me to stay on task to achieve the tight deadline. I also found it beneficial to reflect on what I had learnt that day that I could apply to improve my performance in the future.  

![Stand Up Example](docs/standup_example.png)

## Reference List

Abba, I. V. (2022, October 21). What is an ORM – The Meaning of Object Relational Mapping Database Tools. Retrieved from https://www.freecodecamp.org/news/what-is-an-orm-the-meaning-of-object-relational-mapping-database-tools/

Agile Alliance. (2022). Agile 101 What is Agile? Retrieved October 2, 2022, from https://www.agilealliance.org/agile101/

Andress, J. (2019). Foundations of Information Security: A Straightforward Introduction. San Fransisco : No Starch Press.

Bourgeois , D., & Bourgeois, D. (2014). Information Systems for Business and Beyond. Saylor Academy Press Books.

Chavan, H., & Shaikh, S. (2022). Introduction to DBMS: Designing and Implementing Databases from Scratch for Absolute Beginners (English Edition) Paperback. BPB Publications.

Dolphin, R. (2022, Feb 23). SQL vs NoSQL | Comparing Relational and Non-Relational Database Management. Retrieved October 29, 2022, from Towards Data Science: https://towardsdatascience.com/comparing-relational-and-non-relational-database-management-systems-sql-vs-nosql-f4c8f5988365

Hevo Data Inc. (2022, May 6). Relational Database Vs NoSQL: 7 Critical Aspects. Retrieved October 29, 2022, from Hevo Data: https://hevodata.com/learn/relational-database-vs-nosql/

Hoyos, M. (2018, December 25). What is an ORM and Why You Should Use it. Retrieved October 29, 2022, from https://blog.bitsrc.io/what-is-an-orm-and-why-you-should-use-it-b2b6f75f5e2a

Ionos. (2022, September 22). PostgreSQL: a closer look at the object-relational database management system. Retrieved October 12, 2022, from Ionos: https://www.ionos.com/digitalguide/server/know-how/postgresql/

Kraft, M., & Dougherty, S. (2013). The effect of teacher–family communication on. Journal of Research on Educational Effectiveness, 6(3), 199-222.

Liang, M. (2021, March 11). Understanding Object-Relational Mapping: Pros, Cons, and Types. Retrieved October 29, 2022, from Altexsoft: https://www.altexsoft.com/blog/object-relational-mapping/

Microsoft. (2022, July 4). Relational vs. NoSQL data. Retrieved October 29, 2022, from https://learn.microsoft.com/en-us/dotnet/architecture/cloud-native/relational-vs-nosql-data

Okta. (2022). Introduction to JSON Web Tokens. Retrieved October 12, 2022, from https://jwt.io/

Pallets. (2010). Flask Web development one drop at a time. Retrieved October 20, 2022, from Flask’s Documentation: https://flask.palletsprojects.com/en/2.2.x/
Peterson, R. (2022, October 15). What is PostgreSQL? Introduction, Advantages & Disadvantages. Retrieved October 20, 2022, from Guru99: https://www.guru99.com/introduction-postgresql.html

PostgreSQL Tutorial Website. (2022). Retrieved October 14, 2022, from What is PostgreSQL?: https://www.postgresqltutorial.com/postgresql-getting-started/what-is-postgresql/

Real Python. (2014). Model-View-Controller (MVC) Explained – With Legos. Retrieved October 20, 2022, from https://realpython.com/
the-model-view-controller-mvc-paradigm-summarized-with-legos/

Seitsinger, A., Felner, R., Brand, S., & Burns, A. (2018). A large-scale examination of the nature and efficacy of teachers' practices to engage parents: Assessment, parental contact, and student-level impact. Journal of School Psychology, 46(4), 477-505.

Shields, W. (2019). SQL QuickStart Guide: The Simplified Beginner's Guide to Managing, Analyzing, and Manipulating Data With SQL. ClydeBank Media LLC.
SQLAlchemy. (2022). SQLAlchemy 1.4 Documentation. Retrieved October 15, 2022, from https://docs.sqlalchemy.org/en/14/

StackOverflow. (2021, June). 2021 Developer Survey. Retrieved from Stack Overflow: https://insights.stackoverflow.com/survey/2021#most-popular-technologies-platform

Sutherland , J., & Sutherland , J. (2014). Scrum: The Art of Doing Twice the Work in Half the Time. New York: Crown Business.

The PostgreSQL Global Development Group. (2022). PostgreSQL: The World's Most Advanced Open Source Relational Database. Retrieved October 2, 2022, from https://www.postgresql.org/

The State of Queensland- Department of Education. (2022). Brisbane State High School. Retrieved October 27, 2022, from School Enrolment Management Plan: https://education.qld.gov.au/parents-and-carers/enrolment/management-plans/brisbane-state-high-school

