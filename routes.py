from flask import render_template, request, redirect, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from app import app
import sql_queries
import sql_modify_tables

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
            if user[1]:
                session["teacher"] = False
            else:
                session["teacher"] = True
            return redirect("/courses")
    flash("Käyttäjätunnus tai salasana on väärä")
    return redirect("/")

@app.route("/courses")
def courses():
    if session["teacher"]:
        teacher_courses = sql_queries.teachers_courses(session["usersname"])
        return render_template("courses.html", courses=teacher_courses)
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
    if session["teacher"]:
        course_name = request.form["course_name"]
        ids = sql_queries.check_coursename(course_name)
        if ids is None:
            content = request.form["content"]
            teacher = session["usersname"]
            sql_modify_tables.new_course(course_name, teacher)
            course_id = sql_queries.course_id(course_name, teacher)
            sql_modify_tables.add_content(course_id, content)
            flash("Kurssi "+course_name+" lisätty")
            return redirect("\courses")
        flash("Kurssinimi on jo käytössä")
        return redirect("/create_course")
    flash("Sinun tulee ensin kirjautua sisään opettajana lisätäksesi kurssin")
    return redirect("/")

@app.route("/user_created", methods=["POST"])
def user_created():
    keyword = request.form["keyw"]
    keyword2 = request.form["keyw_redone"]
    if keyword == keyword2:
        usersname = request.form["name"]
        users = sql_queries.check_username(usersname)
        if users is None:
            student = request.form["role"]
            hashed = generate_password_hash(keyword)
            role_boolean = True if student == "1" else False
            sql_modify_tables.new_user(usersname, hashed, role_boolean)
            flash("Uusi käyttäjä luotu")
            return redirect("/")
        flash("Käyttäjätunnus on jo käytössä")
        return redirect("/create_user")
    flash("Kenttiin annetut salasanat eroavat toisistaan")
    return redirect("/create_user")

@app.route("/logout")
def logout():
    del session["usersname"]
    session["teacher"] = False
    flash("Sinut on kirjattu ulos")
    return redirect("/")

@app.route("/courses/<int:id>")
def course(id):
    tests = sql_queries.tests(id)
    multiplechoice = sql_queries.multiplechoice_tests(id)
    course = sql_queries.spesific_course(id)
    content = sql_queries.content(id)                                                                                                                      
    amount = (True if (len(tests) + len(multiplechoice)) > 0 else False, True if len(content)>0 else False)
    return render_template("course.html", course=course, amount=amount, content=content)

@app.route("/delete/<int:id>")
def delete(id):
    if session["teacher"]:
        teacher = sql_queries.check_teacher(id)
        if teacher == session["usersname"]:
            sql_modify_tables.delete_multiplechoices(id)
            sql_modify_tables.delete_questions(id)
            sql_modify_tables.delete_course(id)
            flash("Kurssi poistettu")
            return redirect("/courses")
    flash("Sinun täytyy olla tämän kurssin opettaja poistaaksesi kurssin")
    return redirect("/courses/"+str(id))

@app.route("/edit/<int:id>")
def edit(id):
    if session["teacher"]:
        teacher = sql_queries.check_teacher(id)
        if teacher == session["usersname"]:
            flash("Kurssia muokattu")
            return redirect("/courses/"+str(id))
    flash("Sinun täytyy olla tämän kurssin opettaja muokataksesi kurssia")
    return redirect("/courses/"+str(id))

@app.route("/courses/<int:course_id>/exercises")
def exercises(course_id):
    tests = sql_queries.tests(course_id)
    multiplechoice = sql_queries.multiplechoice_tests(course_id)
    course = sql_queries.spesific_course(course_id)
    return render_template("exercises.html", course=course, tests=tests, multiplechoice=multiplechoice)

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
            flash("Tehtävä lisätty")
            return redirect("/courses/"+str(id))
    flash("Sinun täytyy olla tämän kurssin opettaja lisätäksesi kurssille tehtäviä")
    return redirect("/courses/"+str(id))

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
            flash("Monivalintatehtävä lisätty")
            return redirect("/courses/"+str(id))
    flash("Sinun täytyy olla tämän kurssin opettaja lisätäksesi kurssille tehtäviä")
    return redirect("/courses/"+str(id))

@app.route("/submit/question/<int:id>/<int:exercise_id>", methods=["POST"])
def submit_question(id, exercise_id):
    answer = sql_queries.question_answer(exercise_id)
    input = request.form["answer"]
    if answer[0] == input:
        sql_modify_tables.correct_question(id, exercise_id, session["usersname"])
        flash("Vastasit oikein tehtävään "+str(exercise_id))
        return redirect("/courses/"+str(id)+"/exercises")
    flash("Vastasit väärin tehtävään "+str(exercise_id))
    return redirect("/courses/"+str(id)+"/exercises")

@app.route("/submit/multiple_choice/<int:id>/<int:exercise_id>", methods=["POST"])
def submit_multiple_choice(id, exercise_id):
    answer = sql_queries.multiplechoice_answer(exercise_id)
    input = request.form["m_answer"]
    if str(answer[0]) == str(input):
        sql_modify_tables.correct_multiple_choice(id, exercise_id, session["usersname"])
        flash("Vastasit oikein monivalintatehtävään "+str(exercise_id))
        return redirect("/courses/"+str(id)+"/exercises")
    flash("Vastasit väärin monivalintatehtävään "+str(exercise_id))
    return redirect("/courses/"+str(id)+"/exercises")

@app.route("/delete/question/<int:id>/<int:exercise_id>")
def delete_question(id, exercise_id):
    if session["teacher"]:
        teacher = sql_queries.check_teacher(id)
        if teacher == session["usersname"]:
            sql_modify_tables.delete_question(exercise_id)
            flash("Tehtävä poistettu")
            return redirect("/courses/"+str(id)+"/exercises")
    flash("Sinun täytyy olla tämän kurssin opettaja poistaaksesi kurssin tehtäviä")
    return redirect("/courses/"+str(id)+"/exercises")

@app.route("/delete/multiple_choice/<int:id>/<int:exercise_id>")
def delete_multiple_choice(id, exercise_id):
    if session["teacher"]:
        teacher = sql_queries.check_teacher(id)
        if teacher == session["usersname"]:
            sql_modify_tables.delete_multiplechoice(exercise_id)
            flash("Tehtävä poistettu")
            return redirect("/courses/"+str(id)+"/exercises")
    flash("Sinun täytyy olla tämän kurssin opettaja poistaaksesi kurssin tehtäviä")
    return redirect("/courses/"+str(id)+"/exercises")
