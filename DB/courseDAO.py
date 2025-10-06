import mysql.connector
from main.Models.course import Course

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'port': '3306',
    'database': 'python_project'
}

def getInfosFromDatabaseCourses():
    """Fetches all courses from the database and returns them as a list of Course objects."""
    courses = []
    try:
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()
        mycursor.execute('SELECT * FROM courses')
        courses_datas = mycursor.fetchall()
        for row in courses_datas:
            course = Course(row[0], row[1], row[2], str(row[3]), str(row[4]))
            courses.append(course)
        return courses
    except Exception as e:
        print(f"Error while selecting course data: {e}")
        return []
    finally:
        if 'mycursor' in locals() and mycursor:
            mycursor.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()


def insertInfosToDatabase(course: Course):
    """Inserts a single course into the database."""
    try:
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()
        query = "INSERT INTO courses(`course_code`,`course_title`,`course_credit_hours`,`course_semester`) VALUES(%s,%s,%s,%s)"
        data = (course.courseCode, course.title, course.creditHours, course.semester)
        mycursor.execute(query, data)
        mydb.commit()
        print("Course inserted successfully.")
    except Exception as e:
        print(f"Error inserting course: {e}")
    finally:
        if 'mycursor' in locals() and mycursor:
            mycursor.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()

def deleteInfosFromDatabase(id):
    """Deletes a course by its ID."""
    try:
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()
        query = "DELETE FROM courses WHERE id = %s"
        mycursor.execute(query, (id,))
        mydb.commit()
        print("Course deleted successfully.")
    except Exception as e:
        print(f"Error deleting course: {e}")
    finally:
        if 'mycursor' in locals() and mycursor:
            mycursor.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()

def updateInfosInsideDatabase(course: Course):
    """Updates a course's information based on its ID."""
    try:
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()
        query = ("UPDATE courses SET course_code = %s, course_title = %s, "
                 "course_credit_hours = %s, course_semester = %s "
                 "WHERE id = %s")
        data = (course.courseCode, course.title, course.creditHours, course.semester, course.id)
        mycursor.execute(query, data)
        mydb.commit()
        print("Course updated successfully.")
    except Exception as e:
        print(f"Error updating course: {e}")
    finally:
        if 'mycursor' in locals() and mycursor:
            mycursor.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()

def getCourseIdByCourseCode(courseCode):
    """Finds the ID of a course given its code."""
    try:
        mydb = mysql.connector.connect(**db_config)
        cursor = mydb.cursor()
        cursor.execute("SELECT id FROM courses WHERE course_code = %s", (courseCode,))
        row = cursor.fetchone()
        return row[0] if row else None
    except Exception as e:
        print(f"Error getting course ID: {e}")
        return None
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()