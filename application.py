import os, requests

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

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
		return render_template("menu.html", name=session.get('name'))
	else:
		return render_template("error.html", message="Sorry - we couldn't find you in our system. Please return to try again or register!")
	return render_template("mainpage.html")

@app.route("/view_results")
def view_results():
    return render_template("view_results.html")

@app.route("/start_assessment")
def start_assessment():
    return render_template("start_assessment.html")    
