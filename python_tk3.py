import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

class PayrollSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Payroll Management System (Offline)")
        self.root.geometry("750x500")

        # Title Label
        tk.Label(root, text="Employee Payroll Management System", 
                 font=("Arial", 18, "bold"), bg="blue", fg="white").pack(fill="x")

        # Input Frame
        frame = tk.Frame(root)
        frame.pack(pady=20)

        # Input Fields
        tk.Label(frame, text="Name").grid(row=0, column=0, padx=10, pady=5)
        self.name = tk.Entry(frame)
        self.name.grid(row=0, column=1)

        tk.Label(frame, text="Designation").grid(row=1, column=0, padx=10, pady=5)
        self.designation = tk.Entry(frame)
        self.designation.grid(row=1, column=1)

        tk.Label(frame, text="Basic Salary").grid(row=2, column=0, padx=10, pady=5)
        self.basic = tk.Entry(frame)
        self.basic.grid(row=2, column=1)

        # Buttons
        tk.Button(frame, text="Add Employee", command=self.add_employee, bg="green", fg="white").grid(row=3, column=0, pady=10)
        tk.Button(frame, text="View Employees", command=self.view_employees, bg="blue", fg="white").grid(row=3, column=1, pady=10)
        tk.Button(frame, text="Calculate Salary", command=self.calculate_salary, bg="orange", fg="white").grid(row=3, column=2, pady=10)

        # Treeview (Table)
        self.tree = ttk.Treeview(root, columns=("id", "name", "designation", "net_salary"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("designation", text="Designation")
        self.tree.heading("net_salary", text="Net Salary")
        self.tree.pack(pady=20, fill="x")

        # CSV File Check
        if not os.path.exists("employees.csv"):
            with open("employees.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Name", "Designation", "Basic Salary", "HRA", "DA", "Tax", "Net Salary"])

    # Add Employee
    def add_employee(self):
        try:
            name = self.name.get()
            designation = self.designation.get()
            basic = float(self.basic.get())

            hra = 0.2 * basic
            da = 0.1 * basic
            tax = 0.05 * basic
            net = basic + hra + da - tax

            # Count existing records for ID
            with open("employees.csv", "r") as f:
                reader = list(csv.reader(f))
                emp_id = len(reader)

            # Save to CSV
            with open("employees.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([emp_id, name, designation, basic, hra, da, tax, net])

            messagebox.showinfo("Success", f"Employee '{name}' added successfully!\nNet Salary: ₹{net:.2f}")
            self.clear_entries()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric salary!")

    # View Employees
    def view_employees(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            with open("employees.csv", "r") as f:
                reader = csv.reader(f)
                next(reader)  # skip header
                for r in reader:
                    self.tree.insert("", tk.END, values=(r[0], r[1], r[2], r[7]))
        except FileNotFoundError:
            messagebox.showerror("Error", "No employee data found!")

    # Calculate Salary
    def calculate_salary(self):
        try:
            basic = float(self.basic.get())
            hra = 0.2 * basic
            da = 0.1 * basic
            tax = 0.05 * basic
            net = basic + hra + da - tax
            messagebox.showinfo("Salary Calculation", f"Net Salary = ₹{net:.2f}")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric Basic Salary")

    # Clear Input Fields
    def clear_entries(self):
        self.name.delete(0, tk.END)
        self.designation.delete(0, tk.END)
        self.basic.delete(0, tk.END)

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    PayrollSystem(root)
    root.mainloop()
