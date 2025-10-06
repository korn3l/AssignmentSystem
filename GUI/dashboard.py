import tkinter as tk
from tkinter import ttk
import sys


def open_teacher_page():
    from GUI.teacher_form import launch_teacher_form
    launch_teacher_form()


def open_course_page():
    from GUI.course_form import CourseForm
    win = tk.Toplevel()
    CourseForm(win)


def open_assignment_page():
    from GUI.assignment_form import launch_assignment_form
    launch_assignment_form()


def exit_app():
    sys.exit()


def main():
    root = tk.Tk()
    root.title("Teacher Course Assignment System")
    root.geometry("400x300")

    title = ttk.Label(root, text="Teacher Course Assignment System", font=("Roboto", 18))
    title.pack(pady=20)

    teacher_btn = ttk.Button(root, text="Manage Teachers", command=open_teacher_page)
    teacher_btn.pack(pady=5)

    course_btn = ttk.Button(root, text="Manage Courses", command=open_course_page)
    course_btn.pack(pady=5)

    assign_btn = ttk.Button(root, text="Assign Courses", command=open_assignment_page)
    assign_btn.pack(pady=5)

    exit_btn = ttk.Button(root, text="Exit", command=exit_app)
    exit_btn.pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    main()