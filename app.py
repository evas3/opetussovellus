from flask import Flask
from flask import render_template, request, redirect, session, flash
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
    sql_users = "SELECT passkey, student FROM Users WHERE username=:usersname"
    executed = db.session.execute(text(sql_users), {"usersname":usersname})
    matches = executed.fetchall()
    for i in matches:
        if check_password_hash(i[0], keyword):
            session["usersname"] = usersname
            if i[1] == True:
                session["teacher"] = False
            else:
                session["teacher"] = True
            return redirect("/courses")
    message = "Käyttäjätunnus tai salasana on väärä"
    direct = "/"
    return render_template("error.html", message=message, direct=direct)

@app.route("/courses")
def courses():
    if session["teacher"]:
        sql_teacher_courses = "SELECT coursename, id FROM Courses WHERE teacher=:teacher"
        execute = db.session.execute(text(sql_teacher_courses), {"teacher":session["usersname"]})
        teacher_courses = execute.fetchall()
        return render_template("courses.html", courses=teacher_courses)
    else:
        sql_courses = "SELECT coursename, id FROM Courses"
        execute = db.session.execute(text(sql_courses))
        courses_all = execute.fetchall()
        return render_template("courses.html", courses=courses_all)

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
    keyword = request.form["keyw"]
    keyword2 = request.form["keyw_redone"]
    direct = "/create_user"
    if keyword == keyword2:
        usersname = request.form["name"]
        sql = "SELECT username FROM Users WHERE username=:usersname"
        execute = db.session.execute(text(sql), {"usersname":usersname})
        users = execute.fetchone()
        if users == None:
            student = request.form["role"]
            hashed = generate_password_hash(keyword)
            role_boolean = True if student == "1" else False
            sql = "INSERT INTO Users (username, passkey, student) VALUES (:usersname, :keyword, :role_boolean)"
            db.session.execute(text(sql), {"usersname":usersname, "keyword":hashed, "role_boolean":role_boolean})
            db.session.commit()
            return render_template("user_created.html")
        message = "Käyttäjätunnus on jo käytössä"
        return render_template("error.html", message=message, direct=direct)
    message = "Kenttiin annetut salasanat eroavat toisistaan"
    return render_template("error.html", message=message, direct=direct)

@app.route("/logout")
def logout():
    del session["usersname"]
    session["teacher"] = False
    return redirect("/")

@app.route("/courses/<int:id>")
def course(id):
    sql_tests = "SELECT ROW_NUMBER() OVER(ORDER BY id) AS num_row, question FROM Questions WHERE course_id=:id"
    execute_tests = db.session.execute(text(sql_tests), {"id":id})
    tests = execute_tests.fetchall()
    sql_multiplechoice_tests = "SELECT ROW_NUMBER() OVER(ORDER BY id) AS num_row, question, choice1, choice2, choice3 FROM Multiple_choice WHERE course_id=:id"
    execute_multiplechoice = db.session.execute(text(sql_multiplechoice_tests), {"id":id})
    multiplechoice = execute_multiplechoice.fetchall()
    sql = "SELECT coursename, id FROM Courses WHERE id=:id"
    execute = db.session.execute(text(sql), {"id":id})
    course = execute.fetchone()
    amount = True if (len(tests) + len(multiplechoice)) > 0 else False
    sql_done = "SELECT "
    return render_template("course.html", course=course, tests=tests, multiplechoice=multiplechoice, amount=amount)

@app.route("/delete/<int:id>")
def delete(id):
    if session["teacher"]:
        sql = "SELECT teacher FROM Courses WHERE id=:id"
        execute = db.session.execute(text(sql), {"id":id})
        teacher = execute.fetchone()[0]
        if teacher == session["usersname"]:
            sql = "DELETE FROM Courses WHERE id=:id"
            db.session.execute(text(sql), {"id":id})
            db.session.commit()
            return redirect("/courses")
    message = "Sinun täytyy olla tämän kurssin opettaja poistaaksesi kurssin"
    direct = "/courses"+str(id)
    return render_template("error.html", message=message, direct=direct)

@app.route("/edit/<int:id>")
def edit(id):
    if session["teacher"]:
        sql = "SELECT teacher FROM Courses WHERE id=:id"
        execute = db.session.execute(text(sql), {"id":id})
        teacher = execute.fetchone()[0]
        if teacher == session["usersname"]:
            return redirect("/courses/"+str(id))
    message = "Sinun täytyy olla tämän kurssin opettaja muokataksesi kurssia"
    direct = "/courses"+str(id)
    return render_template("error.html", message=message, direct=direct)

@app.route("/create/question/<int:id>")
def create_question(id):
    return render_template("create_question.html", id=id)

@app.route("/create/multiple_choice/<int:id>")
def create_multiple_choice(id):
    return render_template("create_multiple_choice.html", id=id)

@app.route("/add/question/<int:id>", methods=["POST"])
def add_question(id):
    if session["teacher"]:
        sql = "SELECT teacher FROM Courses WHERE id=:id"
        execute = db.session.execute(text(sql), {"id":id})
        teacher = execute.fetchone()[0]
        if teacher == session["usersname"]:
            question = request.form["question"]
            answer = request.form["answer"]
            sql = "INSERT INTO Questions (course_id, question, answer) VALUES (:course_id, :question, :answer)"
            db.session.execute(text(sql), {"course_id":id, "question":question, "answer":answer})
            db.session.commit()
            return redirect("/courses/"+str(id))
    message = "Sinun täytyy olla tämän kurssin opettaja lisätäksesi kurssille tehtäviä"
    direct = "/courses"+str(id)
    return render_template("error.html", message=message, direct=direct)

@app.route("/add/multiple_choice/<int:id>", methods=["POST"])
def add_multiple_choice(id):
    if session["teacher"]:
        sql = "SELECT teacher FROM Courses WHERE id=:id"
        execute = db.session.execute(text(sql), {"id":id})
        teacher = execute.fetchone()[0]
        if teacher == session["usersname"]:
            question = request.form["question"]
            choice1 = request.form["choice1"]
            choice2 = request.form["choice2"]
            choice3 = request.form["choice3"]
            answer = request.form["choice"]
            sql = "INSERT INTO Multiple_choice (course_id, question, choice1, choice2, choice3, answer) VALUES (:course_id, :question, :choice1, :choice2, :choice3, :answer)"
            db.session.execute(text(sql), {"course_id":id, "question":question, "choice1":choice1, "choice2":choice2, "choice3":choice3, "answer":answer})
            db.session.commit()
            return redirect("/courses/"+str(id))
    message = "Sinun täytyy olla tämän kurssin opettaja lisätäksesi kurssille tehtäviä"
    direct = "/courses"+str(id)
    return render_template("error.html", message=message, direct=direct)

@app.route("/submit_exercises/<int:id>", methods=["POST"])
def submit_exercises(id):
    return redirect("/courses")