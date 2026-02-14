#!/usr/bin/env python3
"""
Employee Payroll Management System
A comprehensive payroll management system built with Python and Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import os

class PayrollDatabase:
    """Handles all database operations for the payroll system"""
    
    def __init__(self, db_name="payroll.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Establish database connection"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
    
    def create_tables(self):
        """Create necessary database tables"""
        # Employees table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                department TEXT,
                position TEXT,
                hourly_rate REAL NOT NULL,
                hire_date TEXT,
                status TEXT DEFAULT 'Active'
            )
        ''')
        
        # Payroll records table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS payroll (
                payroll_id INTEGER PRIMARY KEY AUTOINCREMENT,
                emp_id INTEGER,
                hours_worked REAL,
                overtime_hours REAL DEFAULT 0,
                gross_salary REAL,
                tax_deduction REAL,
                insurance REAL DEFAULT 0,
                net_salary REAL,
                payment_date TEXT,
                payment_period TEXT,
                FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
            )
        ''')
        
        self.conn.commit()
    
    def add_employee(self, name, email, phone, department, position, hourly_rate, hire_date):
        """Add a new employee to the database"""
        try:
            self.cursor.execute('''
                INSERT INTO employees (name, email, phone, department, position, hourly_rate, hire_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, email, phone, department, position, hourly_rate, hire_date))
            self.conn.commit()
            return True, "Employee added successfully"
        except sqlite3.IntegrityError:
            return False, "Email already exists"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_all_employees(self):
        """Retrieve all employees"""
        self.cursor.execute('SELECT * FROM employees')
        return self.cursor.fetchall()
    
    def get_employee_by_id(self, emp_id):
        """Get employee details by ID"""
        self.cursor.execute('SELECT * FROM employees WHERE emp_id = ?', (emp_id,))
        return self.cursor.fetchone()
    
    def update_employee(self, emp_id, name, email, phone, department, position, hourly_rate):
        """Update employee information"""
        try:
            self.cursor.execute('''
                UPDATE employees 
                SET name=?, email=?, phone=?, department=?, position=?, hourly_rate=?
                WHERE emp_id=?
            ''', (name, email, phone, department, position, hourly_rate, emp_id))
            self.conn.commit()
            return True, "Employee updated successfully"
        except sqlite3.IntegrityError:
            return False, "Email already exists"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def delete_employee(self, emp_id):
        """Delete an employee"""
        try:
            self.cursor.execute('DELETE FROM employees WHERE emp_id = ?', (emp_id,))
            self.conn.commit()
            return True, "Employee deleted successfully"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def add_payroll(self, emp_id, hours_worked, overtime_hours, gross_salary, 
                   tax_deduction, insurance, net_salary, payment_date, payment_period):
        """Add a payroll record"""
        try:
            self.cursor.execute('''
                INSERT INTO payroll (emp_id, hours_worked, overtime_hours, gross_salary, 
                                   tax_deduction, insurance, net_salary, payment_date, payment_period)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (emp_id, hours_worked, overtime_hours, gross_salary, 
                  tax_deduction, insurance, net_salary, payment_date, payment_period))
            self.conn.commit()
            return True, "Payroll record added successfully"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_payroll_by_employee(self, emp_id):
        """Get all payroll records for an employee"""
        self.cursor.execute('''
            SELECT p.*, e.name 
            FROM payroll p
            JOIN employees e ON p.emp_id = e.emp_id
            WHERE p.emp_id = ?
            ORDER BY p.payment_date DESC
        ''', (emp_id,))
        return self.cursor.fetchall()
    
    def get_all_payroll(self):
        """Get all payroll records"""
        self.cursor.execute('''
            SELECT p.*, e.name 
            FROM payroll p
            JOIN employees e ON p.emp_id = e.emp_id
            ORDER BY p.payment_date DESC
        ''')
        return self.cursor.fetchall()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


class EmployeeManagementTab:
    """Employee Management Tab - Add, View, Update, Delete employees"""
    
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.create_widgets()
    
    def create_widgets(self):
        """Create all widgets for employee management"""
        # Main container with two panels
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Employee form
        left_frame = ttk.LabelFrame(main_frame, text="Employee Information", padding=10)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Form fields
        fields = [
            ("Name:", "name"),
            ("Email:", "email"),
            ("Phone:", "phone"),
            ("Department:", "department"),
            ("Position:", "position"),
            ("Hourly Rate ($):", "hourly_rate"),
        ]
        
        self.entries = {}
        for idx, (label, field) in enumerate(fields):
            ttk.Label(left_frame, text=label).grid(row=idx, column=0, sticky="w", pady=5)
            entry = ttk.Entry(left_frame, width=30)
            entry.grid(row=idx, column=1, pady=5, padx=5)
            self.entries[field] = entry
        
        # Hire date
        ttk.Label(left_frame, text="Hire Date:").grid(row=len(fields), column=0, sticky="w", pady=5)
        self.hire_date_entry = ttk.Entry(left_frame, width=30)
        self.hire_date_entry.grid(row=len(fields), column=1, pady=5, padx=5)
        self.hire_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Add Employee", command=self.add_employee).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update Employee", command=self.update_employee).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Employee", command=self.delete_employee).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_form).pack(side=tk.LEFT, padx=5)
        
        # Right panel - Employee list
        right_frame = ttk.LabelFrame(main_frame, text="Employee List", padding=10)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=2)
        main_frame.rowconfigure(0, weight=1)
        
        # Treeview for employee list
        columns = ("ID", "Name", "Email", "Department", "Position", "Rate", "Status")
        self.tree = ttk.Treeview(right_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        
        # Load employees
        self.refresh_employee_list()
        
        self.selected_emp_id = None
    
    def add_employee(self):
        """Add a new employee"""
        # Validate inputs
        name = self.entries["name"].get().strip()
        email = self.entries["email"].get().strip()
        phone = self.entries["phone"].get().strip()
        department = self.entries["department"].get().strip()
        position = self.entries["position"].get().strip()
        hourly_rate = self.entries["hourly_rate"].get().strip()
        hire_date = self.hire_date_entry.get().strip()
        
        if not all([name, email, department, position, hourly_rate]):
            messagebox.showerror("Error", "Please fill all required fields")
            return
        
        try:
            hourly_rate = float(hourly_rate)
            if hourly_rate <= 0:
                raise ValueError("Hourly rate must be positive")
        except ValueError:
            messagebox.showerror("Error", "Invalid hourly rate")
            return
        
        success, message = self.db.add_employee(name, email, phone, department, 
                                               position, hourly_rate, hire_date)
        
        if success:
            messagebox.showinfo("Success", message)
            self.clear_form()
            self.refresh_employee_list()
        else:
            messagebox.showerror("Error", message)
    
    def update_employee(self):
        """Update selected employee"""
        if not self.selected_emp_id:
            messagebox.showerror("Error", "Please select an employee to update")
            return
        
        name = self.entries["name"].get().strip()
        email = self.entries["email"].get().strip()
        phone = self.entries["phone"].get().strip()
        department = self.entries["department"].get().strip()
        position = self.entries["position"].get().strip()
        hourly_rate = self.entries["hourly_rate"].get().strip()
        
        if not all([name, email, department, position, hourly_rate]):
            messagebox.showerror("Error", "Please fill all required fields")
            return
        
        try:
            hourly_rate = float(hourly_rate)
            if hourly_rate <= 0:
                raise ValueError("Hourly rate must be positive")
        except ValueError:
            messagebox.showerror("Error", "Invalid hourly rate")
            return
        
        success, message = self.db.update_employee(self.selected_emp_id, name, email, 
                                                  phone, department, position, hourly_rate)
        
        if success:
            messagebox.showinfo("Success", message)
            self.clear_form()
            self.refresh_employee_list()
        else:
            messagebox.showerror("Error", message)
    
    def delete_employee(self):
        """Delete selected employee"""
        if not self.selected_emp_id:
            messagebox.showerror("Error", "Please select an employee to delete")
            return
        
        confirm = messagebox.askyesno("Confirm Delete", 
                                     "Are you sure you want to delete this employee?")
        if confirm:
            success, message = self.db.delete_employee(self.selected_emp_id)
            if success:
                messagebox.showinfo("Success", message)
                self.clear_form()
                self.refresh_employee_list()
            else:
                messagebox.showerror("Error", message)
    
    def clear_form(self):
        """Clear all form fields"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.hire_date_entry.delete(0, tk.END)
        self.hire_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.selected_emp_id = None
    
    def on_select(self, event):
        """Handle employee selection"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            self.selected_emp_id = values[0]
            
            # Load employee details
            employee = self.db.get_employee_by_id(self.selected_emp_id)
            if employee:
                self.entries["name"].delete(0, tk.END)
                self.entries["name"].insert(0, employee[1])
                
                self.entries["email"].delete(0, tk.END)
                self.entries["email"].insert(0, employee[2])
                
                self.entries["phone"].delete(0, tk.END)
                self.entries["phone"].insert(0, employee[3] or "")
                
                self.entries["department"].delete(0, tk.END)
                self.entries["department"].insert(0, employee[4])
                
                self.entries["position"].delete(0, tk.END)
                self.entries["position"].insert(0, employee[5])
                
                self.entries["hourly_rate"].delete(0, tk.END)
                self.entries["hourly_rate"].insert(0, employee[6])
                
                self.hire_date_entry.delete(0, tk.END)
                self.hire_date_entry.insert(0, employee[7])
    
    def refresh_employee_list(self):
        """Refresh the employee list"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load employees
        employees = self.db.get_all_employees()
        for emp in employees:
            self.tree.insert("", tk.END, values=(emp[0], emp[1], emp[2], emp[4], emp[5], f"${emp[6]:.2f}", emp[8]))


class PayrollManagementTab:
    """Payroll Management Tab - Calculate and manage payroll"""
    
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.create_widgets()
    
    def create_widgets(self):
        """Create all widgets for payroll management"""
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top panel - Payroll calculation
        top_frame = ttk.LabelFrame(main_frame, text="Process Payroll", padding=10)
        top_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Employee selection
        ttk.Label(top_frame, text="Select Employee:").grid(row=0, column=0, sticky="w", pady=5)
        
        self.employee_var = tk.StringVar()
        self.employee_combo = ttk.Combobox(top_frame, textvariable=self.employee_var, 
                                          width=40, state="readonly")
        self.employee_combo.grid(row=0, column=1, pady=5, padx=5)
        self.employee_combo.bind("<<ComboboxSelected>>", self.on_employee_select)
        
        # Load employees
        self.load_employees()
        
        # Payroll details
        fields_frame = ttk.Frame(top_frame)
        fields_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Left column
        left_col = ttk.Frame(fields_frame)
        left_col.grid(row=0, column=0, padx=20)
        
        ttk.Label(left_col, text="Regular Hours:").grid(row=0, column=0, sticky="w", pady=5)
        self.hours_entry = ttk.Entry(left_col, width=20)
        self.hours_entry.grid(row=0, column=1, pady=5, padx=5)
        self.hours_entry.insert(0, "160")
        
        ttk.Label(left_col, text="Overtime Hours:").grid(row=1, column=0, sticky="w", pady=5)
        self.overtime_entry = ttk.Entry(left_col, width=20)
        self.overtime_entry.grid(row=1, column=1, pady=5, padx=5)
        self.overtime_entry.insert(0, "0")
        
        ttk.Label(left_col, text="Insurance:").grid(row=2, column=0, sticky="w", pady=5)
        self.insurance_entry = ttk.Entry(left_col, width=20)
        self.insurance_entry.grid(row=2, column=1, pady=5, padx=5)
        self.insurance_entry.insert(0, "50")
        
        # Right column
        right_col = ttk.Frame(fields_frame)
        right_col.grid(row=0, column=1, padx=20)
        
        ttk.Label(right_col, text="Hourly Rate:").grid(row=0, column=0, sticky="w", pady=5)
        self.rate_label = ttk.Label(right_col, text="$0.00", font=("Arial", 10, "bold"))
        self.rate_label.grid(row=0, column=1, sticky="w", pady=5, padx=5)
        
        ttk.Label(right_col, text="Tax Rate (%):").grid(row=1, column=0, sticky="w", pady=5)
        self.tax_entry = ttk.Entry(right_col, width=20)
        self.tax_entry.grid(row=1, column=1, pady=5, padx=5)
        self.tax_entry.insert(0, "15")
        
        ttk.Label(right_col, text="Payment Period:").grid(row=2, column=0, sticky="w", pady=5)
        self.period_entry = ttk.Entry(right_col, width=20)
        self.period_entry.grid(row=2, column=1, pady=5, padx=5)
        self.period_entry.insert(0, datetime.now().strftime("%B %Y"))
        
        # Calculation button
        button_frame = ttk.Frame(top_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Calculate Payroll", 
                  command=self.calculate_payroll).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Process Payment", 
                  command=self.process_payment).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", 
                  command=self.clear_form).pack(side=tk.LEFT, padx=5)
        
        # Calculation results
        result_frame = ttk.LabelFrame(top_frame, text="Calculation Summary", padding=10)
        result_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)
        
        self.result_text = tk.Text(result_frame, height=8, width=70, font=("Courier", 10))
        self.result_text.pack()
        
        # Bottom panel - Payroll history
        bottom_frame = ttk.LabelFrame(main_frame, text="Payroll History", padding=10)
        bottom_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview for payroll records
        columns = ("ID", "Employee", "Hours", "OT Hours", "Gross", "Tax", "Insurance", "Net", "Date", "Period")
        self.tree = ttk.Treeview(bottom_frame, columns=columns, show="headings", height=10)
        
        widths = [50, 150, 70, 70, 90, 70, 80, 90, 100, 120]
        for col, width in zip(columns, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(bottom_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load payroll history
        self.refresh_payroll_list()
        
        self.current_calculation = None
    
    def load_employees(self):
        """Load employees into combobox"""
        employees = self.db.get_all_employees()
        employee_list = [f"{emp[0]} - {emp[1]} ({emp[5]})" for emp in employees if emp[8] == 'Active']
        self.employee_combo['values'] = employee_list
    
    def on_employee_select(self, event):
        """Handle employee selection"""
        selection = self.employee_var.get()
        if selection:
            emp_id = int(selection.split(" - ")[0])
            employee = self.db.get_employee_by_id(emp_id)
            if employee:
                self.rate_label.config(text=f"${employee[6]:.2f}")
    
    def calculate_payroll(self):
        """Calculate payroll for selected employee"""
        if not self.employee_var.get():
            messagebox.showerror("Error", "Please select an employee")
            return
        
        try:
            emp_id = int(self.employee_var.get().split(" - ")[0])
            employee = self.db.get_employee_by_id(emp_id)
            
            hours = float(self.hours_entry.get())
            overtime = float(self.overtime_entry.get())
            insurance = float(self.insurance_entry.get())
            tax_rate = float(self.tax_entry.get())
            
            hourly_rate = employee[6]
            
            # Calculate gross salary
            regular_pay = hours * hourly_rate
            overtime_pay = overtime * hourly_rate * 1.5  # 1.5x for overtime
            gross_salary = regular_pay + overtime_pay
            
            # Calculate deductions
            tax_deduction = gross_salary * (tax_rate / 100)
            total_deductions = tax_deduction + insurance
            
            # Calculate net salary
            net_salary = gross_salary - total_deductions
            
            # Display results
            result = f"""
{'='*60}
PAYROLL CALCULATION SUMMARY
{'='*60}
Employee: {employee[1]}
Position: {employee[5]}
Department: {employee[4]}
{'='*60}
Regular Hours:          {hours:>10.2f} hrs @ ${hourly_rate:.2f}/hr
Overtime Hours:         {overtime:>10.2f} hrs @ ${hourly_rate * 1.5:.2f}/hr
{'='*60}
Regular Pay:                           ${regular_pay:>12.2f}
Overtime Pay:                          ${overtime_pay:>12.2f}
                                       ----------------
GROSS SALARY:                          ${gross_salary:>12.2f}
{'='*60}
Tax Deduction ({tax_rate}%):                     ${tax_deduction:>12.2f}
Insurance:                             ${insurance:>12.2f}
                                       ----------------
Total Deductions:                      ${total_deductions:>12.2f}
{'='*60}
NET SALARY:                            ${net_salary:>12.2f}
{'='*60}
"""
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, result)
            
            # Store calculation for processing
            self.current_calculation = {
                'emp_id': emp_id,
                'hours': hours,
                'overtime': overtime,
                'gross': gross_salary,
                'tax': tax_deduction,
                'insurance': insurance,
                'net': net_salary
            }
            
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
    
    def process_payment(self):
        """Process and save payroll payment"""
        if not self.current_calculation:
            messagebox.showerror("Error", "Please calculate payroll first")
            return
        
        payment_date = datetime.now().strftime("%Y-%m-%d")
        payment_period = self.period_entry.get()
        
        success, message = self.db.add_payroll(
            self.current_calculation['emp_id'],
            self.current_calculation['hours'],
            self.current_calculation['overtime'],
            self.current_calculation['gross'],
            self.current_calculation['tax'],
            self.current_calculation['insurance'],
            self.current_calculation['net'],
            payment_date,
            payment_period
        )
        
        if success:
            messagebox.showinfo("Success", "Payroll processed successfully")
            self.clear_form()
            self.refresh_payroll_list()
        else:
            messagebox.showerror("Error", message)
    
    def clear_form(self):
        """Clear all form fields"""
        self.employee_var.set("")
        self.hours_entry.delete(0, tk.END)
        self.hours_entry.insert(0, "160")
        self.overtime_entry.delete(0, tk.END)
        self.overtime_entry.insert(0, "0")
        self.insurance_entry.delete(0, tk.END)
        self.insurance_entry.insert(0, "50")
        self.tax_entry.delete(0, tk.END)
        self.tax_entry.insert(0, "15")
        self.period_entry.delete(0, tk.END)
        self.period_entry.insert(0, datetime.now().strftime("%B %Y"))
        self.rate_label.config(text="$0.00")
        self.result_text.delete(1.0, tk.END)
        self.current_calculation = None
    
    def refresh_payroll_list(self):
        """Refresh the payroll history list"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load payroll records
        records = self.db.get_all_payroll()
        for record in records:
            self.tree.insert("", tk.END, values=(
                record[0],  # payroll_id
                record[10],  # employee name
                f"{record[2]:.1f}",  # hours
                f"{record[3]:.1f}",  # overtime
                f"${record[4]:.2f}",  # gross
                f"${record[5]:.2f}",  # tax
                f"${record[6]:.2f}",  # insurance
                f"${record[7]:.2f}",  # net
                record[8],  # date
                record[9]   # period
            ))


class PayrollManagementSystem:
    """Main application class"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Payroll Management System")
        self.root.geometry("1200x700")
        
        # Initialize database
        self.db = PayrollDatabase()
        
        # Create menu
        self.create_menu()
        
        # Create main interface
        self.create_main_interface()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_menu(self):
        """Create application menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.on_closing)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_main_interface(self):
        """Create the main application interface"""
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = ttk.Label(header_frame, text="Employee Payroll Management System",
                               font=("Arial", 18, "bold"))
        title_label.pack()
        
        subtitle_label = ttk.Label(header_frame, text="Manage employees and process payroll efficiently",
                                  font=("Arial", 10))
        subtitle_label.pack()
        
        # Notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Employee Management tab
        emp_tab = ttk.Frame(self.notebook)
        self.notebook.add(emp_tab, text="Employee Management")
        self.emp_management = EmployeeManagementTab(emp_tab, self.db)
        
        # Payroll Management tab
        payroll_tab = ttk.Frame(self.notebook)
        self.notebook.add(payroll_tab, text="Payroll Management")
        self.payroll_management = PayrollManagementTab(payroll_tab, self.db)
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo("About", 
                          "Employee Payroll Management System\n\n"
                          "Version 1.0\n\n"
                          "A comprehensive payroll management system\n"
                          "built with Python and Tkinter")
    
    def on_closing(self):
        """Handle application closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.db.close()
            self.root.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = PayrollManagementSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()
