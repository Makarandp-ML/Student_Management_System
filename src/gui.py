import re
import tkinter as tk
from tkinter import ttk, messagebox

from database import (
    add_student,
    get_students,
    update_student,
    delete_student,
    search_students
)


class StudentManagementSystem:

    def __init__(self):
        self.root = tk.Tk()
        self.root.configure(bg="#F5F5F5")
        self.root.title("Student Management System")
        self.root.geometry("1150x720")
        self.root.resizable(False, False)
        self.selected_id = None
       

        self.create_widgets()
        self.load_students()
        self.root.bind("<Return>", lambda event: self.add_student_gui())
        self.root.bind("<Escape>", lambda event: self.clear_fields())
        self.root.bind("<Delete>", lambda event: self.delete_student_gui())
        
    # -------------------------
    # Create Widgets
    # -------------------------
    def create_widgets(self):

        title = tk.Label(
            self.root,
            text="Student Management System",
            font=("Arial",24,"bold"),
            fg="#1565C0"
        )
        title.pack(pady=10)

        # -------------------------
        # Form Frame
        # -------------------------
        form = tk.LabelFrame(
            self.root,
            text="Student Details",
            font=("Arial",11,"bold"),
            padx=15,
            pady=10
        )
        form.pack(pady=10, padx=20, fill="x")
        

        # Name
        tk.Label(form, text="Name").grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(form, width=30)
        self.name_entry.grid(row=0, column=1)

        # Roll No
        tk.Label(form, text="Roll No").grid(row=0, column=2, padx=10, pady=5)
        self.roll_entry = tk.Entry(form, width=30)
        self.roll_entry.grid(row=0, column=3)

        # Course
        tk.Label(form, text="Course").grid(row=1, column=0, padx=10, pady=5)
        self.course_entry = tk.Entry(form, width=30)
        self.course_entry.grid(row=1, column=1)

        # Email
        tk.Label(form, text="Email").grid(row=1, column=2, padx=10, pady=5)
        self.email_entry = tk.Entry(form, width=30)
        self.email_entry.grid(row=1, column=3)

        # Phone
        tk.Label(form, text="Phone").grid(row=2, column=0, padx=10, pady=5)
        self.phone_entry = tk.Entry(form, width=30)
        self.phone_entry.grid(row=2, column=1)

        # -------------------------
        # Buttons
        # -------------------------
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(
        button_frame,
        text="Add Student",
        bg="#4CAF50",
        fg="white",
        width=15,
        font=("Arial",10,"bold"),
        command=self.add_student_gui
    )
        tk.Button(
        button_frame,
        text="Add Student",
        width=15,
        bg="#4CAF50",
        fg="white",
        font=("Arial",10,"bold"),
        command=self.add_student_gui
    ).grid(row=0, column=0, padx=5)
        tk.Button(
            button_frame,
            text="Update",
            bg="#2196F3",
            width=15,
            command=self.update_student_gui
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            button_frame,
            text="Delete",
            bg="#F44336",
            width=15,
            command=self.delete_student_gui
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            button_frame,
            text="Clear",
            bg="#9E9E9E",
            width=15,
            command=self.clear_fields
        ).grid(row=0, column=3, padx=5)
        # -------------------------
            # Search
            # -------------------------
        
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=10)
        
        tk.Label(
                search_frame,
                text="Search (Name / Roll No):"
            ).pack(side=tk.LEFT)
        
        self.search_entry = tk.Entry(
                search_frame,
                width=30
            )
        self.search_entry.pack(side=tk.LEFT, padx=10)
        
        tk.Button(
                search_frame,
                text="Search",
                bg="#673AB7",
                fg="white",
                command=self.search_student
            ).pack(side=tk.LEFT)
        
        tk.Button(
                search_frame,
                text="Show All",
                bg="#009688",
                fg="white",
                command=self.load_students
        ).pack(side=tk.LEFT, padx=10)
        style = ttk.Style()

        style.configure(
            "Treeview",
            rowheight=28,
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 11, "bold")
        )
        # -------------------------
        # Student Table
        # -------------------------
        columns = (
            "ID",
            "Name",
            "Roll No",
            "Course",
            "Email",
            "Phone"
        )

        self.status_label = tk.Label(
        self.root,
        text="📚 Total Students : 3",
        font=("Arial", 11, "bold")
        )

        self.status_label.pack(pady=5)
        table_frame = tk.LabelFrame(
            self.root,
            text="Student Records",
            font=("Arial",11,"bold"),
            padx=10,
            pady=10
        )
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical")

        self.student_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15,
            yscrollcommand=scrollbar.set
        )

        scrollbar.config(command=self.student_table.yview)

        scrollbar.pack(side="right", fill="y")
        self.student_table.pack(side="left", fill="both", expand=True)
        # Horizontal Scrollbar
        x_scroll = ttk.Scrollbar(
            table_frame,
            orient="horizontal"
        )

        x_scroll.pack(side="bottom", fill="x")

        self.student_table.configure(
            xscrollcommand=x_scroll.set
        )

        x_scroll.config(
            command=self.student_table.xview
        )
        # Configure headings AFTER creating Treeview
        for col in columns:
            self.student_table.heading(col, text=col)

        self.student_table.column("ID", width=50, anchor="center")
        self.student_table.column("Name", width=180)
        self.student_table.column("Roll No", width=100, anchor="center")
        self.student_table.column("Course", width=180)
        self.student_table.column("Email", width=250)
        self.student_table.column("Phone", width=150)

        scrollbar.pack(side="right", fill="y")
        self.student_table.pack(side="left", fill="both", expand=True)
        self.student_table.bind(
        "<<TreeviewSelect>>",
            self.select_student
        )
        footer = tk.Label(
        self.root,
            text="Developed by Makarand Patil",
            font=("Arial",9),
            fg="gray"
        )

        footer.pack(pady=5)
    # -------------------------
    # Load Students
    # -------------------------
    def load_students(self):

        # Clear table
        for row in self.student_table.get_children():
            self.student_table.delete(row)

        # Load data from database
        students = get_students()

        self.student_table.tag_configure("even", background="#F9F9F9")
        self.student_table.tag_configure("odd", background="white")

        for index, student in enumerate(students):

            tag = "even" if index % 2 == 0 else "odd"

            self.student_table.insert(
                "",
                tk.END,
                values=student,
                tags=(tag,)
            )

        self.status_label.config(
        text=f"📚 Total Students : {len(students)}"
        )
        style = ttk.Style()

        style.configure(
            "Treeview",
            rowheight=28,
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 11, "bold")
        )

    # -------------------------
    # Clear Input Fields
    # -------------------------
    def clear_fields(self):

        self.name_entry.delete(0, tk.END)
        self.roll_entry.delete(0, tk.END)
        self.course_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)

        self.selected_id = None
    
    def select_student(self, event):

        selected = self.student_table.focus()

        if not selected:
            return

        values = self.student_table.item(selected, "values")

        if not values:
            return

        # Clear only the entry boxes
        self.name_entry.delete(0, tk.END)
        self.roll_entry.delete(0, tk.END)
        self.course_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)

        # Save selected ID
        self.selected_id = int(values[0])

        # Fill the form
        self.name_entry.insert(0, values[1])
        self.roll_entry.insert(0, values[2])
        self.course_entry.insert(0, values[3])
        self.email_entry.insert(0, values[4])
        self.phone_entry.insert(0, values[5])
    # -------------------------
    # Add Student
    # -------------------------
    def add_student_gui(self):

        name = self.name_entry.get().strip()
        roll = self.roll_entry.get().strip()
        course = self.course_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()

        if not name or not roll or not course:
            messagebox.showerror(
                "Error",
                "Name, Roll No and Course are required."
            )
            return

        # Email Validation
        if email:
            email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

            if not re.match(email_pattern, email):
                messagebox.showerror(
                    "Invalid Email",
                    "Please enter a valid email address."
                )
                return

        # Phone Validation
        if phone:
            if not phone.isdigit() or len(phone) != 10:
                messagebox.showerror(
                    "Invalid Phone",
                    "Phone number must contain exactly 10 digits."
                )
                return

        success = add_student(
            name,
            roll,
            course,
            email,
            phone
        )

        if success:
            messagebox.showinfo(
                "Success",
                "Student added successfully."
            )

            self.clear_fields()
            self.load_students()

        else:
            messagebox.showerror(
                "Error",
                "Roll Number already exists."
            )
    def update_student_gui(self):

        if self.selected_id is None:
            messagebox.showwarning(
                "Warning",
                "Please select a student first."
            )
            return

        name = self.name_entry.get().strip()
        roll = self.roll_entry.get().strip()
        course = self.course_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()

        # Required Fields
        if not name or not roll or not course:
            messagebox.showerror(
                "Error",
                "Name, Roll No and Course are required."
            )
            return

        # Email Validation
        if email:
            email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

            if not re.match(email_pattern, email):
                messagebox.showerror(
                    "Invalid Email",
                    "Please enter a valid email address."
                )
                return

        # Phone Validation
        if phone:
            if not phone.isdigit() or len(phone) != 10:
                messagebox.showerror(
                    "Invalid Phone",
                    "Phone number must contain exactly 10 digits."
                )
                return

            update_student(
                self.selected_id,
                name,
                roll,
                course,
                email,
                phone
            )

            messagebox.showinfo(
                "Success",
                "Student updated successfully."
            )

            self.load_students()
            self.clear_fields()
            
    def delete_student_gui(self):

        if self.selected_id is None:
            messagebox.showwarning(
                "Warning",
                "Please select a student first."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this student?"
        )

        if confirm:
            delete_student(self.selected_id)

            messagebox.showinfo(
                "Success",
                "Student deleted successfully."
            )

            self.load_students()
            self.clear_fields()
            self.selected_id = None
            
        
    def search_student(self):

        keyword = self.search_entry.get().strip()

        students = search_students(keyword)

        # Clear table
        for row in self.student_table.get_children():
            self.student_table.delete(row)

        # Show matching students
        for student in students:
            self.student_table.insert("", tk.END, values=student)
    # -------------------------
    # Run Application
    # -------------------------
    def run(self):
        self.root.mainloop()


# -------------------------
# Main
# -------------------------
if __name__ == "__main__":
    app = StudentManagementSystem()
    app.run()