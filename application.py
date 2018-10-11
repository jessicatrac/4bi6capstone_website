import os, requests

from flask import Flask, session, render_template, request
# from flask_session import Session
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# # Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")

# # Configure session to use filesystem
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# # Set up database
# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def mainpage():
    return render_template("mainpage.html")

@app.route("/registration")
def registration():
    return render_template("registration.html")

@app.route("/mainpage_newregister", methods=['POST'])
def mainpage_newregister():
	firstname_new = request.form.get("firstname") # Storing the new user into our database with the relevant information
	lastname_new = request.form.get("lastname")
	email_new = request.form.get("email")
	username_new = request.form.get("username")
	password_new = request.form.get("password")
	# try:
	# 	db.execute("INSERT INTO users (username, password) VALUES (:user, :pass)",
	# 		{"user": username_new, "pass": password_new})
	# 	db.commit()
	# 	print("Registered %s to the database" % username_new)
	# except ValueError:
	# 	return render_template("error.html", message="Sorry - cannot register user.")
	return render_template("mainpage.html")

@app.route("/useraccess", methods=['POST'])
def useraccess():
	username_attempt = request.form.get("username")
	password_attempt = request.form.get("password")
	# try:
	# 	user_match = db.execute("SELECT * FROM users WHERE username=:username", {"username": username_attempt}).fetchone()
	# except ValueError:
	# 	return render_template("error.html", message="Sorry - we couldn't find you in our system. Please return to try again or register!")
	# if user_match.password == password_attempt:
	# 	session['user'] = user_match.username
	# 	return render_template("search.html", name=session.get('user'))
	# else:
	# 	return render_template("error.html", message="Sorry - we couldn't find you in our system. Please return to try again or register!")
	return render_template("mainpage.html")

