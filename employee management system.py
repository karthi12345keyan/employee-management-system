import tkinter as tk
from tkinter import messagebox
import mysql.connector

def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",  # Replace with your MySQL password
            database="employee_db"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

class EmployeeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System")

        # Connect to the database
        self.conn = connect_db()
        if self.conn is None:
            self.root.quit()  # Exit the application if the connection failed

        self.cursor = self.conn.cursor()

        # Create UI components
        self.create_widgets()

    def create_widgets(self):
        # Customize labels
        tk.Label(self.root, text="Name", font=("Helvetica", 12), bg="lightblue").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.root, text="Position", font=("Helvetica", 12), bg="lightblue").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self.root, text="Salary", font=("Helvetica", 12), bg="lightblue").grid(row=2, column=0, padx=10, pady=5)
        
        # Customize entry fields
        self.name_entry = tk.Entry(self.root, font=("Helvetica", 12))
        self.position_entry = tk.Entry(self.root, font=("Helvetica", 12))
        self.salary_entry = tk.Entry(self.root, font=("Helvetica", 12))
 
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)
        self.position_entry.grid(row=1, column=1, padx=10, pady=5)
        self.salary_entry.grid(row=2, column=1, padx=10, pady=5)

        # Customize button
        tk.Button(self.root, text="Add Employee", command=self.add_employee, bg="lightgreen", font=("Helvetica", 12)).grid(row=3, column=0, columnspan=2, pady=10)

        # Customize text area
        self.text_area = tk.Text(self.root, height=10, width=50, font=("Helvetica", 12), bg="lightyellow")
        self.text_area.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    

        

    def add_employee(self):
        name = self.name_entry.get()
        position = self.position_entry.get()
        salary = self.salary_entry.get()

        if not name or not position or not salary:
            messagebox.showerror("Input Error", "All fields must be filled")
            return

        try:
            salary = float(salary)
        except ValueError:
            messagebox.showerror("Input Error", "Salary must be a number")
            return

        try:
            query = "INSERT INTO employees (name, position, salary) VALUES (%s, %s, %s)"
            values = (name, position, salary)
            self.cursor.execute(query, values)
            self.conn.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return

        messagebox.showinfo("Success", "Employee added successfully")

        # Clear entry fields
        self.name_entry.delete(0, tk.END)
        self.position_entry.delete(0, tk.END)
        self.salary_entry.delete(0, tk.END)

        # Reload employee list
        self.load_employees()

    def load_employees(self):
        self.text_area.delete(1.0, tk.END)  # Clear existing content

        try:
            query = "SELECT * FROM employees"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return

        for row in rows:
            self.text_area.insert(tk.END, f"ID: {row[0]}, Name: {row[1]}, Position: {row[2]}, Salary: {row[3]}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeApp(root)
    root.mainloop()
