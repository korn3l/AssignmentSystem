import mysql.connector
from main.Models.teacher import Teacher

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'port': '3306',
    'database': 'python_project'
}

def getInfosFromDatabaseTeachers():
    """Fetches all teachers from the database and returns them as a list of Teacher objects."""
    teachers = []
    try:
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()
        mycursor.execute('SELECT * FROM teacher_infos')
        teachersDatas = mycursor.fetchall()
        for row in teachersDatas:
            teacher = Teacher(row[0], row[1], row[2], row[3], row[4])
            teachers.append(teacher)
        return teachers
    except Exception as e:
        print(f"Error while selecting teacher data: {e}")
        return []
    finally:
        if 'mycursor' in locals() and mycursor:
            mycursor.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()

def insertInfosToDatabase(teacher: Teacher):
    """Inserts a single teacher into the database."""
    try:
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()
        query = "INSERT INTO teacher_infos(`name`,`department`,`email`,`phone_number`) VALUES(%s,%s,%s,%s)"
        data = (teacher.name, teacher.department, teacher.email, teacher.phoneNumber)
        mycursor.execute(query, data)
        mydb.commit()
        print("Teacher data inserted successfully.")
    except Exception as e:
        print(f"Error inserting teacher: {e}")
    finally:
        if 'mycursor' in locals() and mycursor:
            mycursor.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()

def deleteInfosFromDatabase(id):
    """Deletes a teacher by their ID."""
    try:
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()
        query = "DELETE FROM teacher_infos WHERE id = %s"
        mycursor.execute(query, (id,))
        mydb.commit()
        print("Teacher data deleted successfully.")
    except Exception as e:
        print(f"Error deleting teacher: {e}")
    finally:
        if 'mycursor' in locals() and mycursor:
            mycursor.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()

def updateInfosInsideDatabase(teacher: Teacher):
    """Updates a teacher's information based on their ID."""
    try:
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()
        query = ("UPDATE teacher_infos "
                 "SET name = %s, department = %s, email = %s, phone_number = %s "
                 "WHERE id = %s")
        data = (teacher.name, teacher.department, teacher.email, teacher.phoneNumber, teacher.id)
        mycursor.execute(query, data)
        mydb.commit()
        print("Teacher data updated successfully.")
    except Exception as e:
        print(f"Error updating teacher: {e}")
    finally:
        if 'mycursor' in locals() and mycursor:
            mycursor.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()

def getTeacherIdByName(name):
    """Finds the ID of a teacher given their name."""
    try:
        mydb = mysql.connector.connect(**db_config)
        cursor = mydb.cursor()
        cursor.execute("SELECT id FROM teacher_infos WHERE name = %s", (name,))
        row = cursor.fetchone()
        return row[0] if row else None
    except Exception as e:
        print(f"Error getting teacher ID by name: {e}")
        return None
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()