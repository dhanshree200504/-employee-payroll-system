#!/usr/bin/env python3
"""
Test script for Employee Payroll Management System
Tests core database and calculation functions
"""

import os
import sys
from datetime import datetime

# Import the PayrollDatabase class
sys.path.insert(0, os.path.dirname(__file__))
from payroll_system import PayrollDatabase

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
    
    success, msg = db.add_payroll(
        1,  # emp_id
        hours,
        overtime,
        gross,
        tax,
        insurance,
        net,
        datetime.now().strftime("%Y-%m-%d"),
        "Test Period"
    )
    assert success, f"Failed to add payroll: {msg}"
    print(f"✓ {msg}")
    
    # Test 6: Get payroll records
    print("\nTest 6: Retrieving payroll records")
    payroll_records = db.get_payroll_by_employee(1)
    assert len(payroll_records) == 1, "Expected 1 payroll record"
    print(f"✓ Retrieved {len(payroll_records)} payroll record(s)")
    
    # Test 7: Verify calculations
    print("\nTest 7: Verifying payroll calculations")
    record = payroll_records[0]
    print(f"  Regular Pay: ${regular_pay:.2f}")
    print(f"  Overtime Pay: ${overtime_pay:.2f}")
    print(f"  Gross Salary: ${gross:.2f}")
    print(f"  Tax (15%): ${tax:.2f}")
    print(f"  Insurance: ${insurance:.2f}")
    print(f"  Net Salary: ${net:.2f}")
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
        sys.exit(0)
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
