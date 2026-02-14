#!/usr/bin/env python3
"""
Example/Demo script for Employee Payroll Management System
This demonstrates the basic functionality without requiring GUI
"""

import os
import sqlite3
from datetime import datetime

# Note: This is a simplified version for demonstration
# For the full GUI application, run: python payroll_system.py

class PayrollDemo:
    """Demonstration of payroll system functionality"""
    
    def __init__(self):
        self.db_name = "demo_payroll.db"
        if os.path.exists(self.db_name):
            os.remove(self.db_name)
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.setup_database()
    
    def setup_database(self):
        """Create database tables"""
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
    
    def run_demo(self):
        """Run the demo"""
        print("=" * 70)
        print("EMPLOYEE PAYROLL MANAGEMENT SYSTEM - DEMO")
        print("=" * 70)
        
        # Add sample employees
        print("\n1. ADDING EMPLOYEES")
        print("-" * 70)
        employees = [
            ("Alice Johnson", "alice@company.com", "555-0001", "Engineering", "Senior Developer", 65.0),
            ("Bob Williams", "bob@company.com", "555-0002", "Sales", "Sales Manager", 50.0),
            ("Carol Davis", "carol@company.com", "555-0003", "Marketing", "Marketing Director", 55.0),
            ("David Brown", "david@company.com", "555-0004", "Engineering", "Junior Developer", 35.0),
        ]
        
        for name, email, phone, dept, position, rate in employees:
            self.cursor.execute('''
                INSERT INTO employees (name, email, phone, department, position, hourly_rate, hire_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, email, phone, dept, position, rate, datetime.now().strftime("%Y-%m-%d")))
            print(f"  ✓ Added: {name:20} | {position:20} | ${rate:.2f}/hr")
        
        self.conn.commit()
        
        # Display all employees
        print("\n2. EMPLOYEE DIRECTORY")
        print("-" * 70)
        print(f"{'ID':<5} {'Name':<20} {'Department':<15} {'Position':<20} {'Rate':<10}")
        print("-" * 70)
        
        self.cursor.execute('SELECT emp_id, name, department, position, hourly_rate FROM employees')
        for emp in self.cursor.fetchall():
            print(f"{emp[0]:<5} {emp[1]:<20} {emp[2]:<15} {emp[3]:<20} ${emp[4]:<9.2f}")
        
        # Process payroll for each employee
        print("\n3. PROCESSING PAYROLL")
        print("-" * 70)
        
        # Different scenarios for each employee
        payroll_data = [
            (1, 160, 15),   # Alice: full time + overtime
            (2, 160, 0),    # Bob: full time, no overtime
            (3, 140, 5),    # Carol: part time + some overtime
            (4, 160, 20),   # David: full time + lots of overtime
        ]
        
        for emp_id, hours, overtime in payroll_data:
            self.process_employee_payroll(emp_id, hours, overtime)
        
        # Display payroll summary
        print("\n4. PAYROLL SUMMARY")
        print("-" * 70)
        print(f"{'Employee':<20} {'Gross':<12} {'Deductions':<12} {'Net Salary':<12}")
        print("-" * 70)
        
        self.cursor.execute('''
            SELECT e.name, p.gross_salary, (p.tax_deduction + p.insurance), p.net_salary
            FROM payroll p
            JOIN employees e ON p.emp_id = e.emp_id
        ''')
        
        total_gross = 0
        total_net = 0
        
        for emp_name, gross, deductions, net in self.cursor.fetchall():
            print(f"{emp_name:<20} ${gross:<11.2f} ${deductions:<11.2f} ${net:<11.2f}")
            total_gross += gross
            total_net += net
        
        print("-" * 70)
        print(f"{'TOTALS:':<20} ${total_gross:<11.2f} ${total_gross - total_net:<11.2f} ${total_net:<11.2f}")
        
        print("\n5. DETAILED PAYROLL REPORT")
        print("-" * 70)
        
        # Show detailed report for one employee
        self.cursor.execute('''
            SELECT e.*, p.*
            FROM employees e
            JOIN payroll p ON e.emp_id = p.emp_id
            WHERE e.emp_id = 1
        ''')
        
        emp = self.cursor.fetchone()
        if emp:
            print(f"\nEmployee: {emp[1]}")
            print(f"Position: {emp[5]}")
            print(f"Department: {emp[4]}")
            print(f"Hourly Rate: ${emp[6]:.2f}")
            print(f"\nPayroll Details:")
            print(f"  Regular Hours: {emp[11]:.1f}")
            print(f"  Overtime Hours: {emp[12]:.1f}")
            print(f"  Gross Salary: ${emp[13]:.2f}")
            print(f"  Tax Deduction: ${emp[14]:.2f}")
            print(f"  Insurance: ${emp[15]:.2f}")
            print(f"  Net Salary: ${emp[16]:.2f}")
            print(f"  Payment Date: {emp[17]}")
            print(f"  Payment Period: {emp[18]}")
        
        print("\n" + "=" * 70)
        print("DEMO COMPLETED")
        print("=" * 70)
        print("\nTo use the full GUI application, run:")
        print("  python payroll_system.py")
        print("\nNote: Requires Python 3.6+ with Tkinter")
        print("=" * 70)
    
    def process_employee_payroll(self, emp_id, hours, overtime):
        """Process payroll for an employee"""
        self.cursor.execute('SELECT name, hourly_rate FROM employees WHERE emp_id = ?', (emp_id,))
        emp = self.cursor.fetchone()
        
        if emp:
            name, rate = emp
            
            # Calculate salary
            regular_pay = hours * rate
            overtime_pay = overtime * rate * 1.5
            gross = regular_pay + overtime_pay
            
            # Calculate deductions
            tax_rate = 0.15  # 15%
            tax = gross * tax_rate
            insurance = 50.0
            
            net = gross - tax - insurance
            
            # Save to database
            self.cursor.execute('''
                INSERT INTO payroll (emp_id, hours_worked, overtime_hours, gross_salary,
                                   tax_deduction, insurance, net_salary, payment_date, payment_period)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (emp_id, hours, overtime, gross, tax, insurance, net,
                  datetime.now().strftime("%Y-%m-%d"), "February 2026"))
            
            self.conn.commit()
            
            print(f"  ✓ Processed: {name:20} | Hours: {hours:3.0f} + {overtime:2.0f} OT | Net: ${net:,.2f}")
    
    def cleanup(self):
        """Close database and clean up"""
        self.conn.close()
        # Keep the demo database for inspection
        print(f"\nDemo database saved as: {self.db_name}")

if __name__ == "__main__":
    demo = PayrollDemo()
    demo.run_demo()
    demo.cleanup()
