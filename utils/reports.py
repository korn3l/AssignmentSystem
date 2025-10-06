from datetime import datetime

from DB.assignmentDAO import get_assignments_with_details
from DB.teacherDAO import getInfosFromDatabaseTeachers
from DB.courseDAO import getInfosFromDatabaseCourses


class ReportGenerator:

    @staticmethod
    def generate_teacher_course_report():
        try:
            assignments = get_assignments_with_details()
            teachers = getInfosFromDatabaseTeachers()

            teacher_courses = {}

            for assignment in assignments:
                teacher_name = assignment[0]
                course_info = f"{assignment[1]} - {assignment[4]} ({assignment[5]} credits, {assignment[6]})"
                department = assignment[2]
                email = assignment[3]

                if teacher_name not in teacher_courses:
                    teacher_courses[teacher_name] = {
                        'department': department,
                        'email': email,
                        'courses': []
                    }
                teacher_courses[teacher_name]['courses'].append(course_info)

            for teacher in teachers:
                if teacher.name not in teacher_courses:
                    teacher_courses[teacher.name] = {
                        'department': teacher.department,
                        'email': teacher.email,
                        'courses': ['No courses assigned']
                    }

            report = []
            report.append("=" * 80)
            report.append("TEACHER-COURSE ASSIGNMENT REPORT")
            report.append("=" * 80)
            report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append("=" * 80)

            for teacher_name, info in sorted(teacher_courses.items()):
                report.append(f"\nTeacher: {teacher_name}")
                report.append(f"Department: {info['department']}")
                report.append(f"Email: {info['email']}")
                report.append("Courses:")
                for course in info['courses']:
                    report.append(f"  • {course}")
                report.append("-" * 50)

            report.append(f"\nTotal Teachers: {len(teacher_courses)}")
            report.append("=" * 80)

            return "\n".join(report)

        except Exception as e:
            return f"Error generating teacher-course report: {str(e)}"

    @staticmethod
    def generate_course_teacher_report():
        try:
            assignments = get_assignments_with_details()
            courses = getInfosFromDatabaseCourses()

            course_teachers = {}

            for assignment in assignments:
                course_key = assignment[1]
                course_title = assignment[4]
                credit_hours = assignment[5]
                semester = assignment[6]
                teacher_info = f"{assignment[0]} ({assignment[2]}, {assignment[3]})"

                if course_key not in course_teachers:
                    course_teachers[course_key] = {
                        'title': course_title,
                        'credits': credit_hours,
                        'semester': semester,
                        'teachers': []
                    }
                course_teachers[course_key]['teachers'].append(teacher_info)

            for course in courses:
                course_key = f"{course.courseCode} - {course.title}"
                if course_key not in course_teachers:
                    course_teachers[course_key] = {
                        'title': course.title,
                        'credits': course.creditHours,
                        'semester': course.semester,
                        'teachers': ['No teacher assigned']
                    }

            report = []
            report.append("=" * 80)
            report.append("COURSE-TEACHER ASSIGNMENT REPORT")
            report.append("=" * 80)
            report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append("=" * 80)

            for course_key, info in sorted(course_teachers.items()):
                report.append(f"\nCourse: {course_key}")
                report.append(f"Credits: {info['credits']}")
                report.append(f"Semester: {info['semester']}")
                report.append("Assigned Teachers:")
                for teacher in info['teachers']:
                    report.append(f"  • {teacher}")
                report.append("-" * 50)

            report.append(f"\nTotal Courses: {len(course_teachers)}")
            report.append("=" * 80)

            return "\n".join(report)

        except Exception as e:
            return f"Error generating course-teacher report: {str(e)}"

    @staticmethod
    def generate_summary_report():
        try:
            teachers = getInfosFromDatabaseTeachers()
            courses = getInfosFromDatabaseCourses()
            assignments = get_assignments_with_details()

            total_teachers = len(teachers)
            total_courses = len(courses)
            total_assignments = len(assignments)

            teachers_with_courses = len(set([assignment[0] for assignment in assignments]))
            teachers_without_courses = total_teachers - teachers_with_courses

            courses_with_teachers = len(set([assignment[1] for assignment in assignments]))
            courses_without_teachers = total_courses - courses_with_teachers

            dept_counts = {}
            for teacher in teachers:
                dept = teacher.department
                dept_counts[dept] = dept_counts.get(dept, 0) + 1

            report = []
            report.append("=" * 60)
            report.append("SYSTEM SUMMARY REPORT")
            report.append("=" * 60)
            report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append("=" * 60)

            report.append("\n📊 OVERVIEW STATISTICS")
            report.append("-" * 30)
            report.append(f"Total Teachers: {total_teachers}")
            report.append(f"Total Courses: {total_courses}")
            report.append(f"Total Assignments: {total_assignments}")

            report.append("\n👥 TEACHER STATISTICS")
            report.append("-" * 30)
            report.append(f"Teachers with courses: {teachers_with_courses}")
            report.append(f"Teachers without courses: {teachers_without_courses}")

            report.append("\n📚 COURSE STATISTICS")
            report.append("-" * 30)
            report.append(f"Courses with teachers: {courses_with_teachers}")
            report.append(f"Courses without teachers: {courses_without_teachers}")

            report.append("\n🏢 DEPARTMENT DISTRIBUTION")
            report.append("-" * 30)
            for dept, count in sorted(dept_counts.items()):
                report.append(f"{dept}: {count} teachers")

            report.append("=" * 60)

            return "\n".join(report)

        except Exception as e:
            return f"Error generating summary report: {str(e)}"

    @staticmethod
    def save_report_to_file(report_content, filename=None):
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"report_{timestamp}.txt"

        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(report_content)
            return f"Report saved to {filename}"
        except Exception as e:
            return f"Error saving report: {str(e)}"


if __name__ == "__main__":
    print("=== Testing Report Generator ===")

    generator = ReportGenerator()

    print("\n1. Testing Teacher-Course Report:")
    print("-" * 50)
    teacher_report = generator.generate_teacher_course_report()
    print(teacher_report[:500] + "..." if len(teacher_report) > 500 else teacher_report)

    print("\n2. Testing Course-Teacher Report:")
    print("-" * 50)
    course_report = generator.generate_course_teacher_report()
    print(course_report[:500] + "..." if len(course_report) > 500 else course_report)

    print("\n3. Testing Summary Report:")
    print("-" * 50)
    summary_report = generator.generate_summary_report()
    print(summary_report)

    print("\n4. Testing File Save:")
    print("-" * 50)
    save_result = generator.save_report_to_file(summary_report, "test_report.txt")
    print(save_result)