import os, requests

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import datetime

app = Flask(__name__)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def mainpage():
    return render_template("mainpage.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/team")
def team():
    return render_template("team.html")

@app.route("/registration")
def registration():
    return render_template("registration.html")

@app.route("/mainpage_newregister", methods=['POST'])
def mainpage_newregister():
	firstname_new = request.form.get("firstname") # Storing the new user into our database
	lastname_new = request.form.get("lastname")
	email_new = request.form.get("email")
	pass_new = request.form.get("pass")
	try:
		db.execute("INSERT INTO users (first_name, last_name, email, password) VALUES (:first, :last, :email, :pass)",
			{"first": firstname_new, "last": lastname_new, "email": email_new, "pass": pass_new})
		db.commit()
		print("Registered %s to the database" % firstname_new)
	except ValueError:
		return render_template("error.html", message="Sorry - cannot register user.")
	return render_template("mainpage.html")

@app.route("/menu", methods=['POST'])
def menu():
	email_attempt = request.form.get("email")
	pass_attempt = request.form.get("pass")
	try:
		users_match = db.execute("SELECT * FROM users WHERE email=:email", {"email": email_attempt}).fetchone()
	except ValueError:
		return render_template("error.html", message="Sorry - we couldn't find you in our system. Please return to try again or register!")
	if users_match.password == pass_attempt:
		session['name'] = users_match.first_name
		session['id'] = users_match.id
		return render_template("menu.html", name=session.get('name'))
	else:
		return render_template("error.html", message="Sorry - we couldn't find you in our system. Please return to try again or register!")
	return render_template("mainpage.html")

@app.route("/menu_return")
def menu_return():
    print("%s is returning to menu" % session['name'])
    return render_template("menu.html", name=session.get('name'))


@app.route("/view_results", methods=['POST'])
def view_results():
	user_id = session.get('id')
	student_list = db.execute("SELECT MIN(id) as id, student_first_name, student_last_name FROM students WHERE user_id = :user_id GROUP BY student_first_name, student_last_name",
		{"user_id":user_id}).fetchall()
	for student in student_list:
		print("Search result: %s" % student.student_first_name)
	if student_list is None:
		return render_template("error.html", message = "Sorry - no students found.")
	else:
		return render_template("view_results.html",student_list=student_list)

@app.route("/assessment/<string:student_id>")
def assessment(student_id):
    student_prelim = db.execute("SELECT * FROM students WHERE id =:student_id", {"student_id": student_id}).fetchone()
    if student_prelim is None:
        return render_template("error.html", message = "Sorry - this student does not exist.")
    first_name = student_prelim.student_first_name
    last_name = student_prelim.student_last_name
    student_search = db.execute("SELECT * FROM students WHERE student_first_name =:first_name AND student_last_name =:last_name", {"first_name": first_name, "last_name": last_name}).fetchall()
    if student_search is None:
        return render_template("error.html", message = "Sorry - this student does not exist.")
    return render_template("assessment_details.html", student = student_prelim,student_per_year = student_search)

@app.route("/assessment_start", methods=['POST'])
def assessment_start():
    return render_template("assessment_start.html")

@app.route("/assessment_front", methods=['POST'])
def assessment_front():
    firstname_new = request.form.get("firstname") # Storing the new user into our database
    lastname_new = request.form.get("lastname")
    school_new = request.form.get("school")
    email_new = request.form.get("email")
    session_id = session['id']
    now = datetime.datetime.now() # get current year to store as assessment year
    year = now.year
    try:
    	db.execute("INSERT INTO students (student_first_name, student_last_name, school, guardian_email, user_id, year_assessment) VALUES (:first, :last, :school, :email, :nurse_id, :year)",
    		{"first": firstname_new, "last": lastname_new, "school": school_new, "email": email_new, "nurse_id": session_id, "year": year})
    	db.commit()
    	print("Added %s to the student database" % firstname_new)
    except ValueError:
    	return render_template("error.html", message="Sorry - cannot add student.")
    return render_template("assessment_front.html")

@app.route("/assessment_back", methods=['POST'])
def assessment_back():
    return render_template("assessment_back.html")

@app.route("/assessment_complete", methods=['POST'])
def assessment_complete():
    return render_template("assessment_complete.html")
