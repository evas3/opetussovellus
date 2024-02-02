from flask import Flask
from flask import render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user", methods=["POST"])
def user():
    username = request.form["name"]
    keyword = request.form["keyw"]
    if "ope":
        return render_template("teacher.html", name=username)
    elif "oppilas":
        return render_template("students.html", name=username)

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
    username = request.form["name"]
    keyword = request.form["kayw"]
    return render_template("user_created.html")