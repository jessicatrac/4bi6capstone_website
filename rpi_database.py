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


plaque_detected = 1 # yes there is plaque


if plaque_detected == 1:
	engine.execute("UPDATE students SET plaque= 't' WHERE id=(SELECT max(id) FROM students)")
	db.commit()
	print("PLAQUE")
else:
	engine.execute("UPDATE students SET plaque= 'f' WHERE id=(SELECT max(id) FROM students)")
	db.commit()
	print(" NOPLAQUE")
