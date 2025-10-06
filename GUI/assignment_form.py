import tkinter as tk
from tkinter import ttk, messagebox

from main.Models.assignment import Assignment
from DB import assignmentDAO, teacherDAO, courseDAO


def launch_assignment_form():
    window = tk.Toplevel()
    window.title("Assign Courses to Teachers")
    window.geometry("700x500")

    current_teachers = []
    current_courses = []

    def populate_comboboxes():
        """Fetches fresh data and populates the dropdowns."""
        nonlocal current_teachers, current_courses

        current_teachers = teacherDAO.getInfosFromDatabaseTeachers()
        teacher_names = [t.name for t in current_teachers]
        teacher_combo["values"] = teacher_names

        current_courses = courseDAO.getInfosFromDatabaseCourses()
        course_display_names = [f"{c.courseCode} - {c.title}" for c in current_courses]
        course_combo["values"] = course_display_names

    def populate_treeview():
        """Clears the treeview and reloads it with current assignments."""
        for item in tree.get_children():
            tree.delete(item)

        assignments_data = assignmentDAO.getInfosFromDatabase()
        for assignment in assignments_data:
            tree.insert("", tk.END, values=(assignment[1], assignment[2]))

    def assign_course():
        teacher_name = teacher_combo.get()
        course_display_name = course_combo.get()

        if not teacher_name or not course_display_name:
            messagebox.showwarning("Input Error", "Please select both a teacher and a course.")
            return

        new_assignment = Assignment(id=None, teacherName=teacher_name, courseName=course_display_name)

        try:
            assignmentDAO.insertInfosToDatabase(new_assignment)
            populate_treeview()
            teacher_combo.set('')
            course_combo.set('')
        except Exception as e:
            messagebox.showerror("Database Error",
                                 f"Could not assign course.\nThis assignment might already exist.\n\nDetails: {e}")

    def remove_assignment():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select an assignment from the list to remove.")
            return

        if messagebox.askyesno("Delete Confirmation", "Are you sure you want to remove the selected assignment?"):
            values = tree.item(selected_item[0], 'values')
            teacher_name_to_delete = values[0]
            course_name_to_delete = values[1]
            assignmentDAO.deleteInfosFromDatabase(teacher_name_to_delete, course_name_to_delete)
            populate_treeview()


    form_frame = ttk.Frame(window, padding="10")
    form_frame.pack(fill="x")

    ttk.Label(form_frame, text="Select Teacher:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    teacher_combo = ttk.Combobox(form_frame, state="readonly", width=40)
    teacher_combo.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(form_frame, text="Select Course:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    course_combo = ttk.Combobox(form_frame, state="readonly", width=40)
    course_combo.grid(row=1, column=1, padx=5, pady=5)

    button_frame = ttk.Frame(window, padding="10")
    button_frame.pack(fill="x")
    ttk.Button(button_frame, text="Assign Course", command=assign_course).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Remove Selected", command=remove_assignment).pack(side="left", padx=5)

    tree_frame = ttk.Frame(window, padding="10")
    tree_frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(tree_frame, columns=("Teacher", "Course"), show="headings")
    tree.heading("Teacher", text="Teacher")
    tree.heading("Course", text="Course")
    tree.pack(fill="both", expand=True)

    try:
        populate_comboboxes()
        populate_treeview()
    except Exception as e:
        messagebox.showerror("Fatal Error",
                             f"Could not load data from the database.\nPlease check your database connection and restart the application.\n\nError: {e}")
        window.destroy()