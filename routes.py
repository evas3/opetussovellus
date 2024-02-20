from app import app
import sql_queries
import sql_modify_tables
from flask import render_template, request, redirect, session, flash
from werkzeug.security import check_password_hash, generate_password_hash

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user", methods=["POST"])
def user():
    usersname = request.form["name"]
    keyword = request.form["keyw"]
    matches = sql_queries.fetch_users(usersname)
    for user in matches:
        if check_password_hash(user[0], keyword):
            session["usersname"] = usersname
            if user[1] == True:
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
        teacher_courses = sql_queries.teachers_courses(session["usersname"])
        return render_template("courses.html", courses=teacher_courses)
    else:
        courses_all = sql_queries.all_courses()
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
    sql_modify_tables.new_course(course_name, teacher)
    return render_template("course_added.html", course_name=course_name)

@app.route("/user_created", methods=["POST"])
def user_created():
    keyword = request.form["keyw"]
    keyword2 = request.form["keyw_redone"]
    direct = "/create_user"
    if keyword == keyword2:
        usersname = request.form["name"]
        users = sql_queries.check_username(usersname)
        if users == None:
            student = request.form["role"]
            hashed = generate_password_hash(keyword)
            role_boolean = True if student == "1" else False
            sql_modify_tables.new_user(usersname, hashed, role_boolean)
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
    tests = sql_queries.tests(id)
    multiplechoice = sql_queries.multiplechoice_tests(id)
    course = sql_queries.spesific_course(id)
    amount = True if (len(tests) + len(multiplechoice)) > 0 else False
    return render_template("course.html", course=course, tests=tests, multiplechoice=multiplechoice, amount=amount)

@app.route("/delete/<int:id>")
def delete(id):
    if session["teacher"]:
        teacher = sql_queries.check_teacher(id)
        if teacher == session["usersname"]:
            sql_modify_tables.delete_course(id)
            return redirect("/courses")
    message = "Sinun täytyy olla tämän kurssin opettaja poistaaksesi kurssin"
    direct = "/courses"+str(id)
    return render_template("error.html", message=message, direct=direct)

@app.route("/edit/<int:id>")
def edit(id):
    if session["teacher"]:
        teacher = sql_queries.check_teacher(id)
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
        teacher = sql_queries.check_teacher(id)
        if teacher == session["usersname"]:
            question = request.form["question"]
            answer = request.form["answer"]
            sql_modify_tables.new_question(id, question, answer)
            return redirect("/courses/"+str(id))
    message = "Sinun täytyy olla tämän kurssin opettaja lisätäksesi kurssille tehtäviä"
    direct = "/courses"+str(id)
    return render_template("error.html", message=message, direct=direct)

@app.route("/add/multiple_choice/<int:id>", methods=["POST"])
def add_multiple_choice(id):
    if session["teacher"]:
        teacher = sql_queries.check_teacher(id)
        if teacher == session["usersname"]:
            question = request.form["question"]
            choice1 = request.form["choice1"]
            choice2 = request.form["choice2"]
            choice3 = request.form["choice3"]
            answer = request.form["choice"]
            sql_modify_tables.new_choice(id, question, choice1, choice2, choice3, answer)
            return redirect("/courses/"+str(id))
    message = "Sinun täytyy olla tämän kurssin opettaja lisätäksesi kurssille tehtäviä"
    direct = "/courses"+str(id)
    return render_template("error.html", message=message, direct=direct)

@app.route("/submit_exercises/<int:id>", methods=["POST"])
def submit_exercises(id):
    return redirect("/courses")