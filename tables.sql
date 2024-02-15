CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    passkey TEXT,
    student BOOLEAN);

CREATE TABLE Courses (
    id SERIAL PRIMARY KEY,
    coursename TEXT UNIQUE,
    teacher TEXT,
    students TEXT);

CREATE TABLE Content (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES Courses(id),
    text_content TEXT,
    pictures IMAGE);

CREATE TABLE Questions (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES Courses(id),
    question TEXT,
    answer TEXT);

CREATE TABLE Multiple_choice (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES Courses(id),
    question TEXT,
    choice1 TEXT,
    choice2 TEXT,
    choice3 TEXT,
    answer INTEGER);

CREATE TABLE Answered (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES Courses(id),
    text_question BOOLEAN,
    question_id INTEGER,
    student TEXT);