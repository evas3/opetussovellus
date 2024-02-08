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
