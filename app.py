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
    sql_users = "SELECT passkey, student FROM Users where username=:usersname"
    executed = db.session.execute(text(sql_users), {"usersname":usersname})
    matches = executed.fetchall()
    for i in matches:
        if check_password_hash(i[0], keyword):
            sql_courses = "SELECT coursename FROM Courses"
            execute2 = db.session.execute(text(sql_courses))
            courses = execute2.fetchall()
            if i[1] == True:
                session["usersname"] = usersname
                return render_template("student.html", courses=courses)
            else:
                session["usersname"] = usersname
                return render_template("teacher.html", courses=courses)
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
    teacher = session["usersname"]
    sql = "INSERT INTO Courses (coursename, teacher, students) VALUES (:course_name, :teacher, NULL)"
    db.session.execute(text(sql), {"course_name":course_name, "teacher":teacher})
    db.session.commit()
    return render_template("course_added.html", course_name=course_name)

@app.route("/user_created", methods=["POST"])
def user_created():
    usersname = request.form["name"]
    keyword = request.form["keyw"]
    student = request.form["role"]
    hashed = generate_password_hash(keyword)
    role_boolean = True if student == "1" else False
    sql = "INSERT INTO Users (username, passkey, student) VALUES (:usersname, :keyword, :role_boolean)"
    db.session.execute(text(sql), {"usersname":usersname, "keyword":hashed, "role_boolean":role_boolean})
    db.session.commit()
    return render_template("user_created.html")

@app.route("/teacher")
def teacher():
    sql_courses = "SELECT coursename FROM Courses"
    execute2 = db.session.execute(text(sql_courses))
    courses = execute2.fetchall()
    return render_template("teacher.html", courses=courses)

@app.route("/logout")
def logout():
    del session["usersname"]
    return redirect("/")