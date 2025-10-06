import mysql.connector
from main.Models.assignment import Assignment

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'port': '3306',
    'database': 'python_project'
}

def getInfosFromDatabase():
    """Get all assignments from database. Returns raw tuples."""
    try:
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()
        mycursor.execute('SELECT * FROM assignments')
        return mycursor.fetchall()
    except Exception as e:
        print(f"Error while selecting assignment data: {e}")
        return []
    finally:
        if 'mycursor' in locals() and mycursor:
            mycursor.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()

def insertInfosToDatabase(assignment: Assignment):
    """Insert assignment into database."""
    try:
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()
        query = "INSERT INTO assignments(`teacher_name`, `course_name`) VALUES(%s, %s)"
        data = (assignment.teacherName, assignment.courseName)
        mycursor.execute(query, data)
        mydb.commit()
        print("Assignment inserted successfully.")
    except Exception as e:
        print(f"Error inserting assignment: {e}")
    finally:
        if 'mycursor' in locals() and mycursor:
            mycursor.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()

def deleteInfosFromDatabase(teacher_name, course_name):
    """Delete assignment from database using teacher and course names."""
    try:
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()
        query = "DELETE FROM assignments WHERE teacher_name = %s AND course_name = %s"
        mycursor.execute(query, (teacher_name, course_name))
        mydb.commit()
        print("Assignment deleted successfully.")
    except Exception as e:
        print(f"Error deleting assignment: {e}")
    finally:
        if 'mycursor' in locals() and mycursor:
            mycursor.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()

def get_assignments_with_details():
    """Get assignments with full teacher and course details"""
    try:
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor(dictionary=True) # IMPROVEMENT: Use dictionary cursor for easier access
        ## NOTE: The LIKE query is fragile. Using Foreign Keys is the proper solution.
        query = """
        SELECT
            a.id as assignment_id,
            a.teacher_name,
            a.course_name,
            t.department,
            t.email,
            c.course_title,
            c.course_credit_hours,
            c.course_semester
        FROM assignments a
        LEFT JOIN teacher_infos t ON a.teacher_name = t.name
        LEFT JOIN courses c ON a.course_name LIKE CONCAT(c.course_code, '%%')
        """
        mycursor.execute(query)
        return mycursor.fetchall()
    except Exception as e:
        print(f"Error getting assignment details: {e}")
        return []
    finally:
        if 'mycursor' in locals() and mycursor:
            mycursor.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()