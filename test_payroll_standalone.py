#!/usr/bin/env python3
"""
Test script for Employee Payroll Management System
Tests core database and calculation functions without GUI
"""

import os
import sqlite3
from datetime import datetime

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


def test_database_operations():
    """Test database operations"""
    print("Testing Employee Payroll Management System")
    print("=" * 60)
    
    # Create a test database
    test_db = "test_payroll.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    db = PayrollDatabase(test_db)
    print("✓ Database created successfully")
    
    # Test 1: Add employees
    print("\nTest 1: Adding employees")
    success, msg = db.add_employee(
        "John Doe", 
        "john.doe@example.com",
        "555-1234",
        "Engineering",
        "Software Engineer",
        50.0,
        datetime.now().strftime("%Y-%m-%d")
    )
    assert success, f"Failed to add employee: {msg}"
    print(f"✓ {msg}")
    
    success, msg = db.add_employee(
        "Jane Smith",
        "jane.smith@example.com",
        "555-5678",
        "Marketing",
        "Marketing Manager",
        45.0,
        datetime.now().strftime("%Y-%m-%d")
    )
    assert success, f"Failed to add employee: {msg}"
    print(f"✓ {msg}")
    
    # Test 2: Get all employees
    print("\nTest 2: Retrieving employees")
    employees = db.get_all_employees()
    assert len(employees) == 2, "Expected 2 employees"
    print(f"✓ Retrieved {len(employees)} employees")
    for emp in employees:
        print(f"  - {emp[1]} ({emp[5]}) - ${emp[6]}/hr")
    
    # Test 3: Get employee by ID
    print("\nTest 3: Get employee by ID")
    employee = db.get_employee_by_id(1)
    assert employee is not None, "Employee not found"
    assert employee[1] == "John Doe", "Wrong employee name"
    print(f"✓ Found employee: {employee[1]}")
    
    # Test 4: Update employee
    print("\nTest 4: Updating employee")
    success, msg = db.update_employee(
        1,
        "John Doe",
        "john.doe@example.com",
        "555-9999",
        "Engineering",
        "Senior Software Engineer",
        60.0
    )
    assert success, f"Failed to update employee: {msg}"
    print(f"✓ {msg}")
    
    employee = db.get_employee_by_id(1)
    assert employee[5] == "Senior Software Engineer", "Position not updated"
    assert employee[6] == 60.0, "Hourly rate not updated"
    print("✓ Employee data updated correctly")
    
    # Test 5: Add payroll
    print("\nTest 5: Adding payroll records")
    
    # Calculate payroll for John Doe
    hours = 160
    overtime = 10
    hourly_rate = 60.0
    regular_pay = hours * hourly_rate
    overtime_pay = overtime * hourly_rate * 1.5
    gross = regular_pay + overtime_pay
    tax = gross * 0.15
    insurance = 50.0
    net = gross - tax - insurance
    
    print(f"\n  Payroll Calculation:")
    print(f"  Regular Hours: {hours} × ${hourly_rate} = ${regular_pay:.2f}")
    print(f"  Overtime Hours: {overtime} × ${hourly_rate * 1.5} = ${overtime_pay:.2f}")
    print(f"  Gross Salary: ${gross:.2f}")
    print(f"  Tax (15%): ${tax:.2f}")
    print(f"  Insurance: ${insurance:.2f}")
    print(f"  Net Salary: ${net:.2f}")
    
    success, msg = db.add_payroll(
        1,  # emp_id
        hours,
        overtime,
        gross,
        tax,
        insurance,
        net,
        datetime.now().strftime("%Y-%m-%d"),
        "February 2026"
    )
    assert success, f"Failed to add payroll: {msg}"
    print(f"\n✓ {msg}")
    
    # Test 6: Get payroll records
    print("\nTest 6: Retrieving payroll records")
    payroll_records = db.get_payroll_by_employee(1)
    assert len(payroll_records) == 1, "Expected 1 payroll record"
    print(f"✓ Retrieved {len(payroll_records)} payroll record(s)")
    
    # Test 7: Verify calculations
    print("\nTest 7: Verifying payroll calculations")
    record = payroll_records[0]
    assert abs(record[4] - gross) < 0.01, "Gross salary mismatch"
    assert abs(record[7] - net) < 0.01, "Net salary mismatch"
    print("✓ Calculations verified")
    
    # Test 8: Test email uniqueness
    print("\nTest 8: Testing email uniqueness constraint")
    success, msg = db.add_employee(
        "Duplicate User",
        "john.doe@example.com",  # Duplicate email
        "555-0000",
        "HR",
        "HR Manager",
        40.0,
        datetime.now().strftime("%Y-%m-%d")
    )
    assert not success, "Should have failed with duplicate email"
    print(f"✓ Duplicate email correctly rejected: {msg}")
    
    # Test 9: Delete employee
    print("\nTest 9: Deleting employee")
    success, msg = db.delete_employee(2)
    assert success, f"Failed to delete employee: {msg}"
    print(f"✓ {msg}")
    
    employees = db.get_all_employees()
    assert len(employees) == 1, "Expected 1 employee after deletion"
    print("✓ Employee count verified after deletion")
    
    # Cleanup
    db.close()
    os.remove(test_db)
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_database_operations()
        exit(0)
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
