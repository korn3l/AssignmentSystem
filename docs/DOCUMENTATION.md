# Teacher Course Assignment System - Documentation

## Overview
A desktop application for managing teachers, courses, and their assignments in an educational institution. Built with Python Tkinter and MySQL.

## Quick Start
1. Install requirements: `pip install mysql-connector-python`
2. Set up MySQL database with tables: `teacher_infos`, `courses`, `assignments`
3. Run: `python main/app.py`

### With homebrew
1. Make sure homebrew is installed
2. install mysql (brew install mysql)
3. brew services start mysql
4. check running services: brew services list
5. to stop mysql server: brew services stop mysql


## Project Structure
PythonProject/

main/app.py              
GUI/                     
    dashboard.py         
    teacher_form.py      
    course_form.py       
    assignment_form.py   
Models/                  
    teacher.py
    course.py
    assignment.py
DB/                      
    teacherDAO.py
    courseDAO.py
    assignmentDAO.py
utils/                   
    validator.py         
    reports.py           


## User Guide

### Adding Teachers
1. Click "Manage Teachers" → Fill form → Click "Add"
2. **Required**: Name (2-50 chars), Department, Valid Email, Phone (10-15 digits)

### Adding Courses
1. Click "Manage Courses" → Fill form → Click "Add Course"
2. **Required**: Course Code (CS101 format), Title, Credits (1-99), Semester

### Assigning Courses
1. Click "Assign Courses" → Select teacher and course → Click "Assign"
2. Each teacher-course pair can only be assigned once

### Generating Reports
```python
from utils.reports import ReportGenerator
generator = ReportGenerator()
report = generator.generate_summary_report()
print(report)
```

## Technical Details

### Database Schema
1. **teacher_infos** id, name, department, email, phone_number
2. **courses**  id, course_code, course_title, course_credit_hours, course_semester
3. **assignments** id, teacher_name, course_name

### Key Classes
1. Teacher/Course/Assignment: Data models with validation
2. Validator: Input validation with regex patterns
3. ReportGenerator: Creates teacher-course, course-teacher, and summary reports
4. DAO Classes: Handle database CRUD operations

### Validation Rules
1. Names: Letters, spaces, hyphens only
2. Email: Standard email format
3. Phone: International format (+1234567890)
4. Course Code: Letters + numbers (CS101, MATH-203)
