from flask import Flask
from flask import render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SEC_KEY")
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user", methods=["POST"])
def user():
    usersname = request.form["name"]
    keyword = request.form["keyw"]
    sql = "SELECT passkey, student FROM Users where username=:usersname"
    executed = db.session.execute(text(sql), {"usersname":usersname})
    matches = executed.fetchall()
    for i in matches:
        if check_password_hash(i[0], keyword):
            if i[1] == "Oppilas":
                session["usersname"] = usersname
                return render_template("students.html", name=usersname)
            else:
                session["usersname"] = usersname
                return render_template("teacher.html", name=usersname)
    return redirect("/")

@app.route("/create_user")
def create_user():
    return render_template("new_user.html")

@app.route("/create_course")
def create_course():
    return render_template("new_course.html")

@app.route("/course_added", methods=["POST"])
def course_added():
    course_name = request.form["course_name"]
    return render_template("course_added.html", course_name=course_name)

@app.route("/user_created", methods=["POST"])
def user_created():
    usersname = request.form["name"]
    keyword = request.form["keyw"]
    student = request.form["role"]
    hashed = generate_password_hash(keyword)
    role_boolean = True if student == "Oppilas" else False
    sql = "INSERT INTO Users (username, passkey, student) VALUES (:usersname, :keyword, :role_boolean)"
    db.session.execute(text(sql), {"usersname":usersname, "keyword":hashed, "role_boolean":role_boolean})
    db.session.commit()
    return render_template("user_created.html")

@app.route("/teacher")
def teacher():
    return render_template("teacher.html")

@app.route("/logout")
def logout():
    del session["usersname"]
    return redirect("/")