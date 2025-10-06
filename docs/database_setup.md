# how to run mysql:
1. brew install mysql
2. to start: brew services start mysql
3. to stop: brew services stop mysql

# checking Database name:
1. mysql -u root -p
2. SHOWDATABASES;

# adding database for the project

### Create the database for your project
CREATE DATABASE python_project;

### Tell MySQL that you want to work inside this new database
USE python_project;

### Create the table to store teacher information
CREATE TABLE teacher_infos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    department VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    phone_number VARCHAR(50)
);

### Create the table to store course information
CREATE TABLE courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_code VARCHAR(20) NOT NULL UNIQUE,
    course_title VARCHAR(255) NOT NULL,
    course_credit_hours INT,
    course_semester VARCHAR(50)
);

### Create the table to link teachers to courses
CREATE TABLE assignments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    teacher_name VARCHAR(255),
    course_name VARCHAR(255),
    -- This prevents the same teacher from being assigned the same course twice
    UNIQUE KEY uk_assignment (teacher_name, course_name)
);

### Show a success message
SELECT 'Database and tables created successfully!' AS status;

## Checking if everything works fine
1. Check if database is set -> SHOW DATABASES;
2. Check tables - > SHOW TABLES;
