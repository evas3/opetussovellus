from db import db
from sqlalchemy.sql import text

def new_user(username, password, role):
    sql = "INSERT INTO Users (username, passkey, student) VALUES (:usersname, :keyword, :role_boolean)"
    db.session.execute(text(sql), {"usersname":username, "keyword":password, "role_boolean":role})
    db.session.commit()

def new_course(name, teacher):
    sql = "INSERT INTO Courses (coursename, teacher, students) VALUES (:course_name, :teacher, NULL)"
    db.session.execute(text(sql), {"course_name":name, "teacher":teacher})
    db.session.commit()

def delete_course(id):
    sql = "DELETE FROM Courses WHERE id=:id"
    db.session.execute(text(sql), {"id":id})
    db.session.commit()

def new_question(id, question, answer):
    sql = "INSERT INTO Questions (course_id, question, answer) VALUES (:course_id, :question, :answer)"
    db.session.execute(text(sql), {"course_id":id, "question":question, "answer":answer})
    db.session.commit()

def new_choice(id, question, choice1, choice2, choice3, answer):
    sql = "INSERT INTO Multiple_choice (course_id, question, choice1, choice2, choice3, answer) VALUES (:course_id, :question, :choice1, :choice2, :choice3, :answer)"
    db.session.execute(text(sql), {"course_id":id, "question":question, "choice1":choice1, "choice2":choice2, "choice3":choice3, "answer":answer})
    db.session.commit()