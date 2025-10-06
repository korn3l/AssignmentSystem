import tkinter as tk
from tkinter import ttk, messagebox
from main.Models.course import Course
from DB import courseDAO
from utils.validator import Validator


class CourseForm:
    def __init__(self, master):
        self.master = master
        self.master.title("Course Management")
        self.master.geometry("800x500")

        self.tree_item_map = {}

        entry_frame = tk.Frame(master, padx=10, pady=10)
        entry_frame.pack(fill="x")

        self.course_code_entry = tk.Entry(entry_frame)
        self.title_entry = tk.Entry(entry_frame)
        self.credit_entry = tk.Entry(entry_frame)
        self.semester_entry = tk.Entry(entry_frame)

        tk.Label(entry_frame, text="Course Code").grid(row=0, column=0, sticky="w", pady=2)
        self.course_code_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        tk.Label(entry_frame, text="Title").grid(row=0, column=2, sticky="w", padx=10, pady=2)
        self.title_entry.grid(row=0, column=3, padx=5, pady=2, sticky="ew")
        tk.Label(entry_frame, text="Credit Hours").grid(row=1, column=0, sticky="w", pady=2)
        self.credit_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
        tk.Label(entry_frame, text="Semester").grid(row=1, column=2, sticky="w", padx=10, pady=2)
        self.semester_entry.grid(row=1, column=3, padx=5, pady=2, sticky="ew")
        entry_frame.grid_columnconfigure(1, weight=1)
        entry_frame.grid_columnconfigure(3, weight=1)

        button_frame = tk.Frame(master, pady=10)
        button_frame.pack(fill="x", padx=10)
        self.add_btn = tk.Button(button_frame, text="Add Course", command=self.add_course)
        self.add_btn.pack(side="left", padx=5)
        self.edit_btn = tk.Button(button_frame, text="Edit Selected", command=self.edit_selected)
        self.edit_btn.pack(side="left", padx=5)
        self.save_btn = tk.Button(button_frame, text="Save Changes", command=self.save_changes, state="disabled")
        self.save_btn.pack(side="left", padx=5)
        self.delete_btn = tk.Button(button_frame, text="Delete Selected", command=self.delete_selected)
        self.delete_btn.pack(side="left", padx=5)
        self.clear_btn = tk.Button(button_frame, text="Clear Form", command=self.clear_entries)
        self.clear_btn.pack(side="left", padx=5)

        tree_frame = tk.Frame(master, padx=10, pady=5)
        tree_frame.pack(fill="both", expand=True)
        self.tree = ttk.Treeview(tree_frame, columns=("Code", "Title", "Credit", "Semester"), show="headings")
        self.tree.heading("Code", text="Course Code")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Credit", text="Credit Hours")
        self.tree.heading("Semester", text="Semester")
        self.tree.pack(fill="both", expand=True)

        self.load_courses()

    def load_courses(self):
        """Clears the treeview and reloads it with fresh data from the database."""
        self.tree.delete(*self.tree.get_children())
        self.tree_item_map.clear()
        db_courses = courseDAO.getInfosFromDatabaseCourses()
        for course in db_courses:
            item_id = self.tree.insert("", tk.END, values=course.as_tuple())
            self.tree_item_map[item_id] = course.id

    def add_course(self):
        """Adds a new course to the database after validation."""
        code = self.course_code_entry.get().strip().upper()
        title = self.title_entry.get().strip()
        credit = self.credit_entry.get().strip()
        semester = self.semester_entry.get().strip()

        is_valid, errors = Validator.validate_all_course_fields(code, title, credit, semester)
        if not is_valid:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return

        new_course = Course(id=None, courseCode=code, title=title, creditHours=credit, semester=semester)
        courseDAO.insertInfosToDatabase(new_course)
        self.load_courses()
        self.clear_entries()
        messagebox.showinfo("Success", "Course added successfully.")

    def edit_selected(self):
        """Populates the form with data from the selected treeview item for editing."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Edit Course", "Select a course to edit.")
            return

        values = self.tree.item(selected_item[0], 'values')
        self.course_code_entry.delete(0, tk.END);
        self.course_code_entry.insert(0, values[0])
        self.title_entry.delete(0, tk.END);
        self.title_entry.insert(0, values[1])
        self.credit_entry.delete(0, tk.END);
        self.credit_entry.insert(0, values[2])
        self.semester_entry.delete(0, tk.END);
        self.semester_entry.insert(0, values[3])

        self.add_btn.config(state="disabled")
        self.save_btn.config(state="normal")
        self.tree.config(selectmode="none")

    def save_changes(self):
        """Saves the updated course information to the database."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Save Error",
                                 "No course was selected for saving.\nPlease select a course and click 'Edit' first.")
            return

        db_id = self.tree_item_map.get(selected_item[0])
        if not db_id:
            messagebox.showerror("Save Error", "Could not find the original course ID to update.")
            return

        code = self.course_code_entry.get().strip().upper()
        title = self.title_entry.get().strip()
        credit = self.credit_entry.get().strip()
        semester = self.semester_entry.get().strip()

        is_valid, errors = Validator.validate_all_course_fields(code, title, credit, semester)
        if not is_valid:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return

        updated_course = Course(id=db_id, courseCode=code, title=title, creditHours=credit, semester=semester)
        courseDAO.updateInfosInsideDatabase(updated_course)

        self.load_courses()
        self.clear_entries()
        messagebox.showinfo("Success", "Course updated successfully.")

    def delete_selected(self):
        """Deletes the selected course from the database."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Delete Course", "Select a course to delete.")
            return

        if messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete the selected course?"):
            db_id = self.tree_item_map.get(selected_item[0])
            if db_id:
                # IMPORTANT: This requires your courseDAO.deleteInfosFromDatabase to accept an ID
                courseDAO.deleteInfosFromDatabase(db_id)
                self.load_courses()
                messagebox.showinfo("Success", "Course deleted.")
            else:
                messagebox.showerror("Error", "Could not find the course to delete.")

    def clear_entries(self):
        """Clears all form fields and resets the UI state."""
        self.course_code_entry.delete(0, tk.END)
        self.title_entry.delete(0, tk.END)
        self.credit_entry.delete(0, tk.END)
        self.semester_entry.delete(0, tk.END)

        self.add_btn.config(state="normal")
        self.save_btn.config(state="disabled")
        self.tree.config(selectmode="browse")

        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection()[0])


if __name__ == "__main__":
    root = tk.Tk()
    app = CourseForm(root)
    root.mainloop()