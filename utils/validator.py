import re


class Validator:
    @staticmethod
    def validate_teacher_name(name):
        if not name or not name.strip():
            return False, "Name cannot be empty"

        name_pattern = r"^[A-Za-zÀ-ÿ\s\-']{2,50}$"
        if not re.match(name_pattern, name.strip()):
            return False, "Name must be 2-50 characters (letters, spaces, hyphens, apostrophes only)"
        return True, "Valid"

    @staticmethod
    def validate_department(department):
        if not department or not department.strip():
            return False, "Department cannot be empty"

        dept_pattern = r"^[A-Za-z\s]{2,50}$"
        if not re.match(dept_pattern, department.strip()):
            return False, "Department must be 2-50 characters (letters and spaces only)"
        return True, "Valid"

    @staticmethod
    def validate_email(email):
        if not email or not email.strip():
            return False, "Email cannot be empty"

        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_pattern, email.strip()):
            return False, "Please enter a valid email address"
        return True, "Valid"

    @staticmethod
    def validate_phone(phone):
        if not phone or not phone.strip():
            return False, "Phone number cannot be empty"

        phone_pattern = r"^\+?[1-9]\d{9,14}$"
        if not re.match(phone_pattern, phone.strip()):
            return False, "Phone number must be 10-15 digits (international format preferred)"
        return True, "Valid"

    @staticmethod
    def validate_course_code(code):
        if not code or not code.strip():
            return False, "Course code cannot be empty"

        code_pattern = r"^[A-Z]{2,5}[-]?\d{3}$"
        if not re.match(code_pattern, code.strip().upper()):
            return False, "Course code must be like CS101 or MATH-203"
        return True, "Valid"

    @staticmethod
    def validate_course_title(title):
        if not title or not title.strip():
            return False, "Course title cannot be empty"

        title_pattern = r"^[\w\s\-:]{4,100}$"
        if not re.match(title_pattern, title.strip()):
            return False, "Course title must be 4-100 characters (letters, digits, spaces, hyphens, colons)"
        return True, "Valid"

    @staticmethod
    def validate_credit_hours(credit):
        if not credit or not str(credit).strip():
            return False, "Credit hours cannot be empty"

        try:
            credit_num = int(credit)
            if credit_num < 1 or credit_num > 99:
                return False, "Credit hours must be between 1 and 99"
            return True, "Valid"
        except ValueError:
            return False, "Credit hours must be a number"

    @staticmethod
    def validate_semester(semester):
        if not semester or not semester.strip():
            return False, "Semester cannot be empty"

        semester_pattern = r"^(Fall|Spring|Summer)\s?\d{4}$|^[A-Za-z0-9\s\-]{3,30}$"
        if not re.match(semester_pattern, semester.strip()):
            return False, "Semester must be like 'Fall 2025' or a custom label (3-30 characters)"
        return True, "Valid"

    @staticmethod
    def validate_all_teacher_fields(name, department, email, phone):
        errors = []

        name_valid, name_msg = Validator.validate_teacher_name(name)
        if not name_valid:
            errors.append(f"Name: {name_msg}")

        dept_valid, dept_msg = Validator.validate_department(department)
        if not dept_valid:
            errors.append(f"Department: {dept_msg}")

        email_valid, email_msg = Validator.validate_email(email)
        if not email_valid:
            errors.append(f"Email: {email_msg}")

        phone_valid, phone_msg = Validator.validate_phone(phone)
        if not phone_valid:
            errors.append(f"Phone: {phone_msg}")

        return len(errors) == 0, errors

    @staticmethod
    def validate_all_course_fields(code, title, credit, semester):
        errors = []

        code_valid, code_msg = Validator.validate_course_code(code)
        if not code_valid:
            errors.append(f"Course Code: {code_msg}")

        title_valid, title_msg = Validator.validate_course_title(title)
        if not title_valid:
            errors.append(f"Title: {title_msg}")

        credit_valid, credit_msg = Validator.validate_credit_hours(credit)
        if not credit_valid:
            errors.append(f"Credit Hours: {credit_msg}")

        semester_valid, semester_msg = Validator.validate_semester(semester)
        if not semester_valid:
            errors.append(f"Semester: {semester_msg}")

        return len(errors) == 0, errors


#testing validator
if __name__ == "__main__":
    print("=== Testing Validator ===")

    print("\n--- Teacher Validation Tests ---")
    test_cases = [
        ("John Doe", "Computer Science", "john@email.com", "+1234567890"),
        ("", "CS", "invalid-email", "123"),  # Invalid case
        ("A", "Math Department", "prof@university.edu", "+9876543210"),  # Invalid name
    ]

    for name, dept, email, phone in test_cases:
        valid, errors = Validator.validate_all_teacher_fields(name, dept, email, phone)
        print(f"Teacher: {name} | Valid: {valid}")
        if not valid:
            for error in errors:
                print(f"  - {error}")

    print("\n--- Course Validation Tests ---")
    course_cases = [
        ("CS101", "Introduction to Programming", "3", "Fall 2025"),
        ("MATH-203", "Calculus II", "4", "Spring 2025"),
        ("X", "Short", "0", "Invalid Semester"),  # Invalid case
    ]

    for code, title, credit, semester in course_cases:
        valid, errors = Validator.validate_all_course_fields(code, title, credit, semester)
        print(f"Course: {code} | Valid: {valid}")
        if not valid:
            for error in errors:
                print(f"  - {error}")