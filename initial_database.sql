/* To run these sets of code in command line, you must have PostgreSQL installed. It is a form of SQL.
After installing, type psql DATABASE_URL in terminal to open shell for SQL commands - this allows you
to write SQL commands to directly write to our database on Heroku. 

Note: Cannot create users and students tables again - they're already created! You can use the code
below as a guideline to create more tables in our database. */


CREATE TABLE users ( /* Keeps track of healthcare professionals that register with DentAssist. */
	id SERIAL PRIMARY KEY, 
	first_name VARCHAR NOT NULL,
	last_name VARCHAR NOT NULL,
	email VARCHAR NOT NULL,
	password VARCHAR NOT NULL
);


INSERT INTO users (first_name, last_name, email, password) VALUES ('Jessica', 'Trac', 'tracj2@mcmaster.ca','testing123');


CREATE TABLE students ( /* Keeps track of detection results for students. */
	id SERIAL PRIMARY KEY,
	student_first_name VARCHAR NOT NULL,
	student_last_name VARCHAR NOT NULL,
	school VARCHAR NOT NULL,
	guardian_email VARCHAR NOT NULL,
	user_id INTEGER REFERENCES users, 
	plaque DECIMAL,
	cavities INTEGER 
);

INSERT INTO students (student_first_name, student_last_name, school, guardian_email, user_id) VALUES ('Christine', 'Trac', 'Castlemore', 'jessicamtrac@gmail.com', 1);
INSERT INTO students (student_first_name, student_last_name, school, guardian_email, user_id, plaque, cavities) VALUES ('Sarina', 'Trac', 'Castlemore', 'jessicamtrac@gmail.com', 1, 0.50, 2);