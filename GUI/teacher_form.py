import tkinter as tk
from tkinter import ttk, messagebox
from main.Models.teacher import Teacher
from DB import teacherDAO
from utils.validator import Validator


def launch_teacher_form():
    window = tk.Toplevel()
    window.title("Teacher Management")
    window.geometry("800x500")

    tree_item_map = {}

    def populate_treeview():

        for item in teacher_list.get_children():
            teacher_list.delete(item)
        tree_item_map.clear()

        teachers = teacherDAO.getInfosFromDatabaseTeachers()
        for teacher in teachers:
            item_id = teacher_list.insert("", "end", values=teacher.as_tuple())
            tree_item_map[item_id] = teacher.id

    def add_teacher():
        name = name_var.get()
        dept = dept_var.get()
        email = email_var.get()
        phone = phone_var.get()

        is_valid, errors = Validator.validate_all_teacher_fields(name, dept, email, phone)
        if not is_valid:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return

        teacher = Teacher(id=None, name=name, department=dept, email=email, phoneNumber=phone)
        teacherDAO.insertInfosToDatabase(teacher)

        clear_entries()
        populate_treeview()
        messagebox.showinfo("Success", "Teacher added successfully.")

    def edit_teacher():
        selected = teacher_list.selection()
        if not selected:
            messagebox.showwarning("Selection", "Select a teacher to edit")
            return

        values = teacher_list.item(selected[0])['values']
        name_var.set(values[0])
        dept_var.set(values[1])
        email_var.set(values[2])
        phone_var.set(values[3])

        add_btn.config(state="disabled")
        save_btn.config(state="normal")
        teacher_list.config(selectmode="none")

    def save_teacher():
        selected = teacher_list.selection()
        if not selected:
            messagebox.showerror("Save Error",
                                 "No teacher was selected for saving.\nPlease select a teacher from the list and click 'Edit' first.")
            return

        db_id = tree_item_map.get(selected[0])
        if db_id is None:
            messagebox.showerror("Save Error", "Could not find the original teacher ID to update.")
            return

        name = name_var.get()
        dept = dept_var.get()
        email = email_var.get()
        phone = phone_var.get()

        is_valid, errors = Validator.validate_all_teacher_fields(name, dept, email, phone)
        if not is_valid:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return

        updated_teacher = Teacher(id=db_id, name=name, department=dept, email=email, phoneNumber=phone)
        teacherDAO.updateInfosInsideDatabase(updated_teacher)  # The DAO needs to be fixed to use the ID

        clear_entries()
        populate_treeview()

        add_btn.config(state="normal")
        save_btn.config(state="disabled")
        teacher_list.config(selectmode="browse")
        messagebox.showinfo("Success", "Teacher updated successfully.")

    def delete_teacher():
        selected = teacher_list.selection()
        if not selected:
            messagebox.showwarning("Selection", "Select a teacher to delete")
            return

        if messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete the selected teacher?"):
            db_id = tree_item_map.get(selected[0])
            if db_id:
                teacherDAO.deleteInfosFromDatabase(db_id)
                populate_treeview()
                messagebox.showinfo("Success", "Teacher deleted.")
            else:
                messagebox.showerror("Error", "Could not find teacher to delete.")

    def clear_entries():
        name_var.set("")
        dept_var.set("")
        email_var.set("")
        phone_var.set("")
        add_btn.config(state="normal")
        save_btn.config(state="disabled")
        teacher_list.config(selectmode="browse")
        if teacher_list.selection():
            teacher_list.selection_remove(teacher_list.selection()[0])

    form_frame = ttk.Frame(window, padding="10")
    form_frame.pack(fill="x")

    name_var, dept_var, email_var, phone_var = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()

    ttk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
    ttk.Entry(form_frame, textvariable=name_var, width=40).grid(row=0, column=1, sticky="ew", padx=5, pady=2)
    ttk.Label(form_frame, text="Department:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
    ttk.Entry(form_frame, textvariable=dept_var, width=40).grid(row=1, column=1, sticky="ew", padx=5, pady=2)
    ttk.Label(form_frame, text="Email:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
    ttk.Entry(form_frame, textvariable=email_var, width=40).grid(row=2, column=1, sticky="ew", padx=5, pady=2)
    ttk.Label(form_frame, text="Phone:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
    ttk.Entry(form_frame, textvariable=phone_var, width=40).grid(row=3, column=1, sticky="ew", padx=5, pady=2)

    button_frame = ttk.Frame(window, padding="10")
    button_frame.pack(fill="x")
    add_btn = ttk.Button(button_frame, text="Add Teacher", command=add_teacher)
    add_btn.pack(side="left", padx=5)
    edit_btn = ttk.Button(button_frame, text="Edit Selected", command=edit_teacher)
    edit_btn.pack(side="left", padx=5)
    save_btn = ttk.Button(button_frame, text="Save Changes", command=save_teacher, state="disabled")
    save_btn.pack(side="left", padx=5)
    delete_btn = ttk.Button(button_frame, text="Delete Selected", command=delete_teacher)
    delete_btn.pack(side="left", padx=5)
    clear_btn = ttk.Button(button_frame, text="Clear Form", command=clear_entries)
    clear_btn.pack(side="left", padx=5)

    tree_frame = ttk.Frame(window, padding="10")
    tree_frame.pack(fill="both", expand=True)
    columns = ("Name", "Department", "Email", "Phone")
    teacher_list = ttk.Treeview(tree_frame, columns=columns, show="headings")
    for col in columns:
        teacher_list.heading(col, text=col)
        teacher_list.column(col, width=180)
    teacher_list.pack(fill="both", expand=True)

    populate_treeview()