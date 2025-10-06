# Teacher Course Assignment System

A desktop application for managing teachers, courses, and their assignments in an educational institution. Built with a Python Tkinter GUI and a MySQL database backend.

## 📸 Application Showcase

Here's a look at the system in action.

| Main Dashboard               | Adding a New Teacher                | Adding a New Course            | Assigning a Course to a Teacher    |
|------------------------------|-------------------------------------|--------------------------------|------------------------------------|
| ![](https://github.com/korn3l/AssignmentSystem/blob/main/assets/dashboard.png)    | ![](https://github.com/korn3l/AssignmentSystem/blob/main/assets/teacher-demo.gif)         | ![](https://github.com/korn3l/AssignmentSystem/blob/main/assets/course-demo.gif)     | ![](https://github.com/korn3l/AssignmentSystem/blob/main/assets/assignment-demo.gif)        |
| **(./assets/dashboard.png)** | **(./assets/add-teacher-demo.gif)** | **(./assets/course-demo.gif)** | **(./assets/assignment-demo.gif)** |


## Features

-   **Manage Teachers**: Add, view, update, and delete teacher records.
-   **Manage Courses**: Add, view, update, and delete course information.
-   **Course Assignments**: Assign courses to teachers with a simple interface, preventing duplicate assignments.
-   **Input Validation**: Ensures data integrity with real-time validation for fields like emails, phone numbers, and course codes.
-   **Reporting**: Generate summary reports on teacher workloads and course assignments.

## Technologies Used

-   **Backend**: Python 3
-   **Database**: MySQL
-   **GUI**: Tkinter (Python's standard GUI toolkit)
-   **Connector**: `mysql-connector-python`

## Getting Started

### 1. Prerequisites

-   **Python 3.7+** installed on your system.
-   **MySQL Server** installed and running. You can download it from the [official MySQL website](https://dev.mysql.com/downloads/mysql/).

### 2. Clone the Repository

```bash
git clone https://github.com/korn3l/AssignmentSystem.git
cd AssignmentSystem
```

### 3. Install Dependencies
```bash
pip install mysql-connector-python
```

### 4. Setup the Database

### 5. Configure Database Connection

### 6. Run the App
```bash
python main/app.py
```
