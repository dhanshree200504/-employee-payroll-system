"""
Database Module for Employee Payroll Management System.

This module provides database operations using SQLite with context managers
for safe and efficient database connection handling.
"""

import sqlite3
from contextlib import contextmanager
from typing import Optional, List, Tuple, Any, Generator
from datetime import datetime, date


# Database file path
DB_PATH = "payroll.db"


@contextmanager
def get_db_connection() -> Generator[sqlite3.Connection, None, None]:
    """
    Context manager for database connections.
    
    Yields:
        sqlite3.Connection: Active database connection.
        
    Ensures proper connection closing even if an exception occurs.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        yield conn
    except sqlite3.Error as e:
        raise Exception(f"Database connection error: {e}")
    finally:
        if conn:
            conn.close()


@contextmanager
def get_db_cursor(conn: sqlite3.Connection) -> Generator[sqlite3.Cursor, None, None]:
    """
    Context manager for database cursors with automatic commit/rollback.
    
    Args:
        conn: Active database connection.
        
    Yields:
        sqlite3.Cursor: Database cursor for executing queries.
    """
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise Exception(f"Database operation error: {e}")
    finally:
        cursor.close()


def initialize_database() -> None:
    """
    Initialize the database with required tables.
    
    Creates employees, attendance, and payroll tables if they don't exist.
    """
    with get_db_connection() as conn:
        with get_db_cursor(conn) as cursor:
            # Create employees table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    emp_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    designation TEXT,
                    department TEXT,
                    basic_salary REAL NOT NULL,
                    bank_acc TEXT,
                    pf_enabled INTEGER DEFAULT 1,
                    tax_percent REAL DEFAULT 0,
                    email TEXT,
                    dob TEXT,
                    photo_path TEXT
                )
            """)
            
            # Create attendance table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    emp_id TEXT NOT NULL,
                    date TEXT NOT NULL,
                    status TEXT NOT NULL,
                    FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
                )
            """)
            
            # Create payroll table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS payroll (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    emp_id TEXT NOT NULL,
                    month TEXT NOT NULL,
                    basic_salary REAL,
                    hra REAL,
                    gross_salary REAL,
                    pf_deduction REAL,
                    tax_deduction REAL,
                    leave_deduction REAL,
                    net_salary REAL,
                    generated_on TEXT,
                    FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
                )
            """)


# ==================== Employee Operations ====================

def add_employee(
    emp_id: str,
    name: str,
    designation: str,
    department: str,
    basic_salary: float,
    bank_acc: str,
    pf_enabled: int,
    tax_percent: float,
    email: str,
    dob: str,
    photo_path: str
) -> bool:
    """
    Add a new employee to the database.
    
    Args:
        emp_id: Unique employee ID.
        name: Employee's full name.
        designation: Job designation/title.
        department: Department name.
        basic_salary: Basic salary amount.
        bank_acc: Bank account number.
        pf_enabled: PF enrollment status (1=enabled, 0=disabled).
        tax_percent: Tax percentage applicable.
        email: Email address.
        dob: Date of birth (YYYY-MM-DD format).
        photo_path: Path to employee photo.
        
    Returns:
        bool: True if employee added successfully, False otherwise.
        
    Raises:
        Exception: If employee ID already exists or database error occurs.
    """
    try:
        with get_db_connection() as conn:
            with get_db_cursor(conn) as cursor:
                cursor.execute("""
                    INSERT INTO employees 
                    (emp_id, name, designation, department, basic_salary, 
                     bank_acc, pf_enabled, tax_percent, email, dob, photo_path)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (emp_id, name, designation, department, basic_salary,
                      bank_acc, pf_enabled, tax_percent, email, dob, photo_path))
        return True
    except sqlite3.IntegrityError:
        raise Exception(f"Employee ID '{emp_id}' already exists.")
    except Exception as e:
        raise Exception(f"Failed to add employee: {e}")


def update_employee(
    emp_id: str,
    name: str,
    designation: str,
    department: str,
    basic_salary: float,
    bank_acc: str,
    pf_enabled: int,
    tax_percent: float,
    email: str,
    dob: str,
    photo_path: str
) -> bool:
    """
    Update an existing employee's information.
    
    Args:
        emp_id: Employee ID to update.
        name: Updated employee name.
        designation: Updated designation.
        department: Updated department.
        basic_salary: Updated basic salary.
        bank_acc: Updated bank account.
        pf_enabled: Updated PF status.
        tax_percent: Updated tax percentage.
        email: Updated email.
        dob: Updated date of birth.
        photo_path: Updated photo path.
        
    Returns:
        bool: True if update successful, False if employee not found.
    """
    try:
        with get_db_connection() as conn:
            with get_db_cursor(conn) as cursor:
                cursor.execute("""
                    UPDATE employees SET
                        name = ?, designation = ?, department = ?,
                        basic_salary = ?, bank_acc = ?, pf_enabled = ?,
                        tax_percent = ?, email = ?, dob = ?, photo_path = ?
                    WHERE emp_id = ?
                """, (name, designation, department, basic_salary, bank_acc,
                      pf_enabled, tax_percent, email, dob, photo_path, emp_id))
                return cursor.rowcount > 0
    except Exception as e:
        raise Exception(f"Failed to update employee: {e}")


def delete_employee(emp_id: str) -> bool:
    """
    Delete an employee and their related records.
    
    Args:
        emp_id: Employee ID to delete.
        
    Returns:
        bool: True if deletion successful, False if employee not found.
    """
    try:
        with get_db_connection() as conn:
            with get_db_cursor(conn) as cursor:
                # Delete related attendance records
                cursor.execute("DELETE FROM attendance WHERE emp_id = ?", (emp_id,))
                # Delete related payroll records
                cursor.execute("DELETE FROM payroll WHERE emp_id = ?", (emp_id,))
                # Delete employee
                cursor.execute("DELETE FROM employees WHERE emp_id = ?", (emp_id,))
                return cursor.rowcount > 0
    except Exception as e:
        raise Exception(f"Failed to delete employee: {e}")


def get_employee(emp_id: str) -> Optional[sqlite3.Row]:
    """
    Retrieve a single employee by ID.
    
    Args:
        emp_id: Employee ID to retrieve.
        
    Returns:
        sqlite3.Row: Employee record or None if not found.
    """
    try:
        with get_db_connection() as conn:
            with get_db_cursor(conn) as cursor:
                cursor.execute("SELECT * FROM employees WHERE emp_id = ?", (emp_id,))
                return cursor.fetchone()
    except Exception as e:
        raise Exception(f"Failed to retrieve employee: {e}")


def get_all_employees() -> List[sqlite3.Row]:
    """
    Retrieve all employees from the database.
    
    Returns:
        List[sqlite3.Row]: List of all employee records.
    """
    try:
        with get_db_connection() as conn:
            with get_db_cursor(conn) as cursor:
                cursor.execute("SELECT * FROM employees ORDER BY name")
                return cursor.fetchall()
    except Exception as e:
        raise Exception(f"Failed to retrieve employees: {e}")


def employee_exists(emp_id: str) -> bool:
    """
    Check if an employee exists in the database.
    
    Args:
        emp_id: Employee ID to check.
        
    Returns:
        bool: True if employee exists, False otherwise.
    """
    try:
        with get_db_connection() as conn:
            with get_db_cursor(conn) as cursor:
                cursor.execute(
                    "SELECT 1 FROM employees WHERE emp_id = ?", (emp_id,)
                )
                return cursor.fetchone() is not None
    except Exception as e:
        raise Exception(f"Failed to check employee existence: {e}")


def search_employees(search_term: str) -> List[sqlite3.Row]:
    """
    Search employees by ID, name, or department.
    
    Args:
        search_term: Term to search for.
        
    Returns:
        List[sqlite3.Row]: Matching employee records.
    """
    try:
        with get_db_connection() as conn:
            with get_db_cursor(conn) as cursor:
                search_pattern = f"%{search_term}%"
                cursor.execute("""
                    SELECT * FROM employees 
                    WHERE emp_id LIKE ? OR name LIKE ? OR department LIKE ?
                    ORDER BY name
                """, (search_pattern, search_pattern, search_pattern))
                return cursor.fetchall()
    except Exception as e:
        raise Exception(f"Failed to search employees: {e}")


# ==================== Attendance Operations ====================

def mark_attendance(emp_id: str, attendance_date: str, status: str) -> bool:
    """
    Mark attendance for an employee.
    
    Args:
        emp_id: Employee ID.
        attendance_date: Date of attendance (YYYY-MM-DD format).
        status: Attendance status ('Present', 'Absent', 'Half-Day', 'Leave').
        
    Returns:
        bool: True if attendance marked successfully.
        
    Raises:
        Exception: If employee doesn't exist or database error occurs.
    """
    if not employee_exists(emp_id):
        raise Exception(f"Employee ID '{emp_id}' does not exist.")
    
    try:
        with get_db_connection() as conn:
            with get_db_cursor(conn) as cursor:
                # Check if attendance already exists for this date
                cursor.execute("""
                    SELECT id FROM attendance 
                    WHERE emp_id = ? AND date = ?
                """, (emp_id, attendance_date))
                existing = cursor.fetchone()
                
                if existing:
                    # Update existing attendance
                    cursor.execute("""
                        UPDATE attendance SET status = ?
                        WHERE emp_id = ? AND date = ?
                    """, (status, emp_id, attendance_date))
                else:
                    # Insert new attendance
                    cursor.execute("""
                        INSERT INTO attendance (emp_id, date, status)
                        VALUES (?, ?, ?)
                    """, (emp_id, attendance_date, status))
        return True
    except Exception as e:
        raise Exception(f"Failed to mark attendance: {e}")


def get_attendance_by_employee(emp_id: str, month: Optional[str] = None) -> List[sqlite3.Row]:
    """
    Get attendance records for an employee.
    
    Args:
        emp_id: Employee ID.
        month: Optional month filter (YYYY-MM format).
        
    Returns:
        List[sqlite3.Row]: Attendance records.
    """
    try:
        with get_db_connection() as conn:
            with get_db_cursor(conn) as cursor:
                if month:
                    cursor.execute("""
                        SELECT * FROM attendance 
                        WHERE emp_id = ? AND date LIKE ?
                        ORDER BY date DESC
                    """, (emp_id, f"{month}%"))
                else:
                    cursor.execute("""
                        SELECT * FROM attendance 
                        WHERE emp_id = ?
                        ORDER BY date DESC
                    """, (emp_id,))
                return cursor.fetchall()
    except Exception as e:
        raise Exception(f"Failed to retrieve attendance: {e}")


def get_attendance_summary(emp_id: str, month: str) -> dict:
    """
    Get attendance summary for an employee for a specific month.
    
    Args:
        emp_id: Employee ID.
        month: Month to summarize (YYYY-MM format).
        
    Returns:
        dict: Summary with present, absent, half_day, leave counts.
    """
    try:
        with get_db_connection() as conn:
            with get_db_cursor(conn) as cursor:
                cursor.execute("""
                    SELECT status, COUNT(*) as count FROM attendance
                    WHERE emp_id = ? AND date LIKE ?
                    GROUP BY status
                """, (emp_id, f"{month}%"))
                
                summary = {
                    'present': 0,
                    'absent': 0,
                    'half_day': 0,
                    'leave': 0
                }
                
                for row in cursor.fetchall():
                    status = row['status'].lower().replace('-', '_')
                    if status in summary:
                        summary[status] = row['count']
                
                return summary
    except Exception as e:
        raise Exception(f"Failed to get attendance summary: {e}")


def get_all_attendance(month: Optional[str] = None) -> List[sqlite3.Row]:
    """
    Get all attendance records, optionally filtered by month.
    
    Args:
        month: Optional month filter (YYYY-MM format).
        
    Returns:
        List[sqlite3.Row]: All attendance records.
    """
    try:
        with get_db_connection() as conn:
            with get_db_cursor(conn) as cursor:
                if month:
                    cursor.execute("""
                        SELECT a.*, e.name 
                        FROM attendance a
                        JOIN employees e ON a.emp_id = e.emp_id
                        WHERE a.date LIKE ?
                        ORDER BY a.date DESC, e.name
                    """, (f"{month}%",))
                else:
                    cursor.execute("""
                        SELECT a.*, e.name 
                        FROM attendance a
                        JOIN employees e ON a.emp_id = e.emp_id
                        ORDER BY a.date DESC, e.name
                    """)
                return cursor.fetchall()
    except Exception as e:
        raise Exception(f"Failed to retrieve attendance records: {e}")


# ==================== Payroll Operations ====================

def calculate_payroll(emp_id: str, month: str) -> dict:
    """
    Calculate payroll for an employee for a specific month.
    
    Calculation Rules:
        - HRA = 20% of Basic Salary
        - Gross Salary = Basic Salary + HRA
        - PF Deduction = 12% of Basic Salary (only if pf_enabled = 1)
        - Tax Deduction = (tax_percent / 100) * Gross Salary
        - Leave Deduction = (Basic Salary / 30) * Number of Absent Days
        - Net Salary = Gross - PF - Tax - Leave Deduction
    
    Args:
        emp_id: Employee ID.
        month: Month for payroll calculation (YYYY-MM format).
        
    Returns:
        dict: Payroll breakdown with all components.
        
    Raises:
        Exception: If employee doesn't exist.
    """
    employee = get_employee(emp_id)
    if not employee:
        raise Exception(f"Employee ID '{emp_id}' does not exist.")
    
    basic_salary = float(employee['basic_salary'])
    pf_enabled = int(employee['pf_enabled'])
    tax_percent = float(employee['tax_percent'])
    
    # Get attendance summary for the month
    attendance = get_attendance_summary(emp_id, month)
    absent_days = attendance['absent']
    half_days = attendance['half_day']
    
    # Calculate absent days (half-days count as 0.5 absent)
    total_absent = absent_days + (half_days * 0.5)
    
    # Calculate salary components
    hra = basic_salary * 0.20
    gross_salary = basic_salary + hra
    
    # PF Deduction (12% of basic salary, only if enabled)
    pf_deduction = basic_salary * 0.12 if pf_enabled else 0.0
    
    # Tax Deduction
    tax_deduction = (tax_percent / 100) * gross_salary
    
    # Leave Deduction
    leave_deduction = (basic_salary / 30) * total_absent
    
    # Net Salary
    net_salary = gross_salary - pf_deduction - tax_deduction - leave_deduction
    
    return {
        'emp_id': emp_id,
        'employee_name': employee['name'],
        'month': month,
        'basic_salary': round(basic_salary, 2),
        'hra': round(hra, 2),
        'gross_salary': round(gross_salary, 2),
        'pf_deduction': round(pf_deduction, 2),
        'tax_deduction': round(tax_deduction, 2),
        'leave_deduction': round(leave_deduction, 2),
        'net_salary': round(net_salary, 2),
        'absent_days': total_absent,
        'pf_enabled': pf_enabled,
        'tax_percent': tax_percent
    }


def save_payroll(payroll_data: dict) -> bool:
    """
    Save calculated payroll to the database.
    
    Args:
        payroll_data: Payroll calculation results.
        
    Returns:
        bool: True if saved successfully.
    """
    try:
        with get_db_connection() as conn:
            with get_db_cursor(conn) as cursor:
                generated_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Check if payroll exists for this month
                cursor.execute("""
                    SELECT id FROM payroll 
                    WHERE emp_id = ? AND month = ?
                """, (payroll_data['emp_id'], payroll_data['month']))
                existing = cursor.fetchone()
                
                if existing:
                    # Update existing payroll
                    cursor.execute("""
                        UPDATE payroll SET
                            basic_salary = ?, hra = ?, gross_salary = ?,
                            pf_deduction = ?, tax_deduction = ?, leave_deduction = ?,
                            net_salary = ?, generated_on = ?
                        WHERE emp_id = ? AND month = ?
                    """, (
                        payroll_data['basic_salary'], payroll_data['hra'],
                        payroll_data['gross_salary'], payroll_data['pf_deduction'],
                        payroll_data['tax_deduction'], payroll_data['leave_deduction'],
                        payroll_data['net_salary'], generated_on,
                        payroll_data['emp_id'], payroll_data['month']
                    ))
                else:
                    # Insert new payroll
                    cursor.execute("""
                        INSERT INTO payroll 
                        (emp_id, month, basic_salary, hra, gross_salary,
                         pf_deduction, tax_deduction, leave_deduction, net_salary, generated_on)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        payroll_data['emp_id'], payroll_data['month'],
                        payroll_data['basic_salary'], payroll_data['hra'],
                        payroll_data['gross_salary'], payroll_data['pf_deduction'],
                        payroll_data['tax_deduction'], payroll_data['leave_deduction'],
                        payroll_data['net_salary'], generated_on
                    ))
        return True
    except Exception as e:
        raise Exception(f"Failed to save payroll: {e}")


def get_payroll_history(emp_id: Optional[str] = None) -> List[sqlite3.Row]:
    """
    Get payroll history, optionally filtered by employee.
    
    Args:
        emp_id: Optional employee ID filter.
        
    Returns:
        List[sqlite3.Row]: Payroll records.
    """
    try:
        with get_db_connection() as conn:
            with get_db_cursor(conn) as cursor:
                if emp_id:
                    cursor.execute("""
                        SELECT p.*, e.name 
                        FROM payroll p
                        JOIN employees e ON p.emp_id = e.emp_id
                        WHERE p.emp_id = ?
                        ORDER BY p.month DESC
                    """, (emp_id,))
                else:
                    cursor.execute("""
                        SELECT p.*, e.name 
                        FROM payroll p
                        JOIN employees e ON p.emp_id = e.emp_id
                        ORDER BY p.month DESC, e.name
                    """)
                return cursor.fetchall()
    except Exception as e:
        raise Exception(f"Failed to retrieve payroll history: {e}")


def get_payroll_for_month(month: str) -> List[sqlite3.Row]:
    """
    Get all payroll records for a specific month.
    
    Args:
        month: Month to retrieve (YYYY-MM format).
        
    Returns:
        List[sqlite3.Row]: Payroll records for the month.
    """
    try:
        with get_db_connection() as conn:
            with get_db_cursor(conn) as cursor:
                cursor.execute("""
                    SELECT p.*, e.name, e.department, e.designation
                    FROM payroll p
                    JOIN employees e ON p.emp_id = e.emp_id
                    WHERE p.month = ?
                    ORDER BY e.name
                """, (month,))
                return cursor.fetchall()
    except Exception as e:
        raise Exception(f"Failed to retrieve payroll for month: {e}")


# ==================== Utility Functions ====================

def get_departments() -> List[str]:
    """
    Get list of unique departments.
    
    Returns:
        List[str]: List of department names.
    """
    try:
        with get_db_connection() as conn:
            with get_db_cursor(conn) as cursor:
                cursor.execute("""
                    SELECT DISTINCT department FROM employees 
                    WHERE department IS NOT NULL AND department != ''
                    ORDER BY department
                """)
                return [row['department'] for row in cursor.fetchall()]
    except Exception as e:
        raise Exception(f"Failed to retrieve departments: {e}")


def get_employee_count() -> int:
    """
    Get total number of employees.
    
    Returns:
        int: Total employee count.
    """
    try:
        with get_db_connection() as conn:
            with get_db_cursor(conn) as cursor:
                cursor.execute("SELECT COUNT(*) as count FROM employees")
                return cursor.fetchone()['count']
    except Exception as e:
        raise Exception(f"Failed to get employee count: {e}")


def bulk_add_sample_employees() -> int:
    """
    Add sample employees for testing purposes.
    
    Returns:
        int: Number of employees added.
    """
    sample_employees = [
        ("EMP001", "John Smith", "Software Engineer", "Engineering", 75000, 
         "1234567890", 1, 10, "john.smith@company.com", "1990-05-15", ""),
        ("EMP002", "Jane Doe", "Project Manager", "Management", 85000,
         "0987654321", 1, 12, "jane.doe@company.com", "1988-03-22", ""),
        ("EMP003", "Mike Johnson", "Data Analyst", "Analytics", 65000,
         "1122334455", 1, 8, "mike.johnson@company.com", "1992-08-10", ""),
        ("EMP004", "Sarah Williams", "HR Manager", "Human Resources", 70000,
         "5566778899", 1, 10, "sarah.williams@company.com", "1985-11-28", ""),
        ("EMP005", "David Brown", "Sales Executive", "Sales", 55000,
         "9988776655", 0, 5, "david.brown@company.com", "1993-07-03", ""),
        ("EMP006", "Emily Davis", "Marketing Lead", "Marketing", 72000,
         "1357924680", 1, 10, "emily.davis@company.com", "1991-01-19", ""),
        ("EMP007", "Robert Wilson", "DevOps Engineer", "Engineering", 80000,
         "2468013579", 1, 12, "robert.wilson@company.com", "1989-09-25", ""),
        ("EMP008", "Lisa Anderson", "Financial Analyst", "Finance", 68000,
         "3692581470", 1, 10, "lisa.anderson@company.com", "1994-04-12", ""),
        ("EMP009", "James Taylor", "QA Engineer", "Engineering", 62000,
         "7418529630", 1, 8, "james.taylor@company.com", "1995-02-08", ""),
        ("EMP010", "Amanda Martinez", "UX Designer", "Design", 67000,
         "8529637410", 1, 9, "amanda.martinez@company.com", "1992-12-30", ""),
    ]
    
    added_count = 0
    for emp in sample_employees:
        try:
            add_employee(*emp)
            added_count += 1
        except Exception:
            # Skip if employee already exists
            pass
    
    return added_count


# Initialize database when module is imported
if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully!")
