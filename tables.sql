CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    passkey TEXT,
    student BOOLEAN);

CREATE TABLE Courses (
    id SERIAL PRIMARY KEY,
    coursename TEXT UNIQUE,
    teacher TEXT);

CREATE TABLE Content (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES Courses(id),
    text_content TEXT);

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

CREATE TABLE AnsweredQuestions (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES Courses(id),
    question_id INTEGER REFERENCES Questions(id),
    student TEXT REFERENCES Users(username));

CREATE TABLE AnsweredMultiple_choice (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES Courses(id),
    question_id INTEGER REFERENCES Multiple_choice(id),
    student TEXT REFERENCES Users(username));
