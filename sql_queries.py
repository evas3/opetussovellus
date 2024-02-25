from sqlalchemy.sql import text
from db import db

def fetch_users(username):
    sql_users = "SELECT passkey, student FROM Users WHERE username=:usersname"
    executed = db.session.execute(text(sql_users), {"usersname":username})
    matches = executed.fetchall()
    return matches

def teachers_courses(name):
    sql_teacher_courses = "SELECT coursename, id FROM Courses WHERE teacher=:teacher"
    execute = db.session.execute(text(sql_teacher_courses), {"teacher":name})
    teacher_courses = execute.fetchall()
    return teacher_courses

def all_courses():
    sql_courses = "SELECT coursename, id FROM Courses"
    execute = db.session.execute(text(sql_courses))
    courses_all = execute.fetchall()
    return courses_all

def check_username(usersname):
    sql = "SELECT username FROM Users WHERE username=:usersname"
    execute = db.session.execute(text(sql), {"usersname":usersname})
    users = execute.fetchone()
    return users

def tests(id):
    sql_tests = """SELECT id, question FROM Questions
                   WHERE course_id=:id"""
    execute_tests = db.session.execute(text(sql_tests), {"id":id})
    tests = execute_tests.fetchall()
    return tests

def multiplechoice_tests(id):
    sql_multiplechoice = """SELECT id, question,
                            choice1, choice2, choice3 FROM Multiple_choice WHERE course_id=:id"""
    execute_multiplechoice = db.session.execute(text(sql_multiplechoice), {"id":id})
    multiplechoice = execute_multiplechoice.fetchall()
    return multiplechoice

def spesific_course(id):
    sql = "SELECT coursename, id FROM Courses WHERE id=:id"
    execute = db.session.execute(text(sql), {"id":id})
    course = execute.fetchone()
    return course

def check_teacher(id):
    sql = "SELECT teacher FROM Courses WHERE id=:id"
    execute = db.session.execute(text(sql), {"id":id})
    teacher = execute.fetchone()[0]
    return teacher

def question_answer(id):
    sql = "SELECT answer, course_id FROM Questions WHERE id=:id"
    execute = db.session.execute(text(sql), {"id":id})
    answers = execute.fetchone()
    return answers

def multiplechoice_answer(id):
    sql = "SELECT answer, course_id FROM Multiple_choice WHERE id=:id"
    execute = db.session.execute(text(sql), {"id":id})
    answers = execute.fetchone()
    return answers

def course_id(course_name, teacher):
    sql = "SELECT id FROM Courses WHERE coursename=:name AND teacher=:teacher"
    execute = db.session.execute(text(sql), {"name":course_name, "teacher":teacher})
    id = execute.fetchone()
    return id[0]

def content(id):
    sql = "SELECT text_content FROM Content WHERE course_id=:course_id"
    execute = db.session.execute(text(sql), {"course_id":id})
    content = execute.fetchall()
    return content