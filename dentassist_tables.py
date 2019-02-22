from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.VARCHAR, nullable=False)
    last_name = db.Column(db.VARCHAR, nullable=False)
    email = db.Column(db.VARCHAR, nullable=False)
    password = db.Column(db.VARCHAR, nullable=False)


class students(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    student_first_name = db.Column(db.VARCHAR, nullable=False)
    student_last_name = db.Column(db.VARCHAR, nullable=False)
    school = db.Column(db.VARCHAR, nullable=False)
    guardian_email = db.Column(db.VARCHAR, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"),nullable=False)
    plaque = db.Column(db.BOOLEAN, nullable=True)
    cavities = db.Column(db.Integer, nullable=True)


