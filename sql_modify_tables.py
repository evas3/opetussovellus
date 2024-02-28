from sqlalchemy.sql import text
from db import db

def new_user(username, password, role):
    sql = "INSERT INTO Users (username, passkey, student) VALUES (:usersname, :keyword, :role_boolean)"
    db.session.execute(text(sql), {"usersname":username, "keyword":password, "role_boolean":role})
    db.session.commit()

def new_course(course_name, teacher):
    sql = "INSERT INTO Courses (coursename, teacher) VALUES (:course_name, :teacher)"
    db.session.execute(text(sql), {"course_name":course_name, "teacher":teacher})
    db.session.commit()

def delete_course(course_id):
    sql = "DELETE FROM Content WHERE course_id=:id"
    db.session.execute(text(sql), {"id":course_id})
    sql = "DELETE FROM Courses WHERE Courses.id=:id"
    db.session.execute(text(sql), {"id":course_id})
    db.session.commit()

def delete_multiplechoices(course_id):
    sql = "DELETE FROM AnsweredMultiple_choice WHERE course_id=:course_id"
    db.session.execute(text(sql), {"course_id":course_id})
    sql = "DELETE FROM Multiple_choice WHERE course_id=:course_id"
    db.session.execute(text(sql), {"course_id":course_id})
    db.session.commit()

def delete_questions(course_id):
    sql = "DELETE FROM AnsweredQuestions WHERE course_id=:course_id"
    db.session.execute(text(sql), {"course_id":course_id})
    sql = "DELETE FROM Questions WHERE course_id=:course_id"
    db.session.execute(text(sql), {"course_id":course_id})
    db.session.commit()

def new_question(id, question, answer):
    sql = "INSERT INTO Questions (course_id, question, answer) VALUES (:course_id, :question, :answer)"
    db.session.execute(text(sql), {"course_id":id, "question":question, "answer":answer})
    db.session.commit()

def new_choice(id, question, choice1, choice2, choice3, answer):
    sql = """INSERT INTO Multiple_choice (course_id, question, choice1, choice2, choice3, answer) VALUES
             (:course_id, :question, :choice1, :choice2, :choice3, :answer)"""
    db.session.execute(text(sql), {"course_id":id, "question":question, "choice1":choice1, "choice2":choice2, "choice3":choice3, "answer":answer})
    db.session.commit()

def correct_question(course_id, question_id, student):
    sql = "INSERT INTO AnsweredQuestions (course_id, question_id, student) VALUES (:course_id, :question_id, :student)"
    db.session.execute(text(sql), {"course_id":course_id, "question_id":question_id, "student":student})
    db.session.commit()

def correct_multiple_choice(course_id, question_id, student):
    sql = "INSERT INTO AnsweredMultiple_choice (course_id, question_id, student) VALUES (:course_id, :question_id, :student)"
    db.session.execute(text(sql), {"course_id":course_id, "question_id":question_id, "student":student})
    db.session.commit()

def delete_question(question_id):
    sql = "DELETE FROM AnsweredQuestions WHERE question_id=:question_id"
    db.session.execute(text(sql), {"question_id":question_id})
    sql = "DELETE FROM Questions WHERE id=:id"
    db.session.execute(text(sql), {"id":question_id})
    db.session.commit()

def delete_multiplechoice(question_id):
    sql = "DELETE FROM AnsweredMultiple_choice WHERE question_id=:question_id"
    db.session.execute(text(sql), {"question_id":question_id})
    sql = "DELETE FROM Multiple_choice WHERE id=:id"
    db.session.execute(text(sql), {"id":question_id})
    db.session.commit()

def add_content(course_id, content):
    sql = "INSERT INTO Content (course_id, text_content) VALUES (:course_id, :text_content)"
    db.session.execute(text(sql), {"course_id":course_id, "text_content":content})
    db.session.commit()

def edit_content(course_id, new_content):
    sql = "UPDATE Content SET text_content=:new_content WHERE course_id=:course_id"
    db.session.execute(text(sql), {"course_id":course_id, "new_content":new_content})
    db.session.commit()

def delete_user(username):
    sql = "DELETE FROM AnsweredQuestions WHERE student=:username"
    db.session.execute(text(sql), {"username":username})
    sql = "DELETE FROM AnsweredMultiple_choice WHERE student=:username"
    db.session.execute(text(sql), {"username":username})
    sql = "DELETE FROM Users WHERE username=:username"
    db.session.execute(text(sql), {"username":username})
    db.session.commit()