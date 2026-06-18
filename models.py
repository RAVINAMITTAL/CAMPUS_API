from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    students = db.relationship('Student', backref='department', lazy=True)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    # phone = db.Column(db.String(20))
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False,
        default="student"
    )
class TokenBlocklist(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    jti = db.Column(db.String(255), nullable=False, unique=True)

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )    