-- Create the HEPaS database
CREATE DATABASE HEPaS;
USE HEPaS;

-- Create table for student information
CREATE TABLE students (
    student_id VARCHAR(8) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    oust_email VARCHAR(100) UNIQUE NOT NULL
);

-- Create table for unit scores
CREATE TABLE unit_scores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    unit_code VARCHAR(7) PRIMARY KEY,
    score FLOAT,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

INSERT INTO students (student_id, first_name, last_name, oust_email)
VALUES ('10591936', 'John', 'Doe', 'jd@our.oust.edu.au');

INSERT INTO unit_scores (student_id, unit_code, score)
VALUES 
('10591936', 'ABC1234', 78.5),
('10591936', 'DEF5678', 85.0),
('10591936', 'GHI9101', 92.0);