# Employee Payroll Management System - User Guide

## Overview
This guide provides detailed instructions on how to use the Employee Payroll Management System.

## System Requirements
- Python 3.6 or higher
- Tkinter (usually comes pre-installed with Python)
- SQLite3 (part of Python standard library)

## Quick Start

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/dhanshree200504/-employee-payroll-system.git
cd -employee-payroll-system

# Run the application
python payroll_system.py
```

### 2. First Launch
When you launch the application, you'll see:
- A header with the application title
- Two main tabs: "Employee Management" and "Payroll Management"
- A status bar at the bottom

## Employee Management Tab

### Adding a New Employee

1. Navigate to the "Employee Management" tab
2. Fill in the employee information form on the left:
   - **Name**: Employee's full name (required)
   - **Email**: Unique email address (required)
   - **Phone**: Contact phone number (optional)
   - **Department**: Department name (required)
   - **Position**: Job title/position (required)
   - **Hourly Rate**: Pay rate per hour in dollars (required)
   - **Hire Date**: Date of hire (auto-filled with current date)

3. Click "Add Employee" button
4. The employee will appear in the list on the right

**Example:**
```
Name: John Smith
Email: john.smith@company.com
Phone: 555-1234
Department: Engineering
Position: Software Engineer
Hourly Rate: 50.00
Hire Date: 2026-02-14
```

### Viewing Employees

The right panel displays all employees in a table with columns:
- ID
- Name
- Email
- Department
- Position
- Hourly Rate
- Status (Active/Inactive)

You can scroll through the list to view all employees.

### Updating an Employee

1. Click on an employee in the list (right panel)
2. The employee's information will load into the form (left panel)
3. Modify any fields you want to update
4. Click "Update Employee" button
5. Confirm the changes

**Note:** You cannot change the hire date when updating an employee.

### Deleting an Employee

1. Select an employee from the list
2. Click "Delete Employee" button
3. Confirm the deletion in the dialog box

**Warning:** This action cannot be undone. Ensure you want to delete the employee before confirming.

### Clearing the Form

Click "Clear Form" to reset all fields and deselect any employee.

## Payroll Management Tab

### Processing Payroll

1. Navigate to the "Payroll Management" tab
2. Select an employee from the dropdown menu
3. The hourly rate will be displayed automatically
4. Enter payroll information:
   - **Regular Hours**: Standard hours worked (default: 160 hours/month)
   - **Overtime Hours**: Additional hours worked (default: 0)
   - **Insurance**: Insurance deduction amount (default: $50)
   - **Tax Rate**: Tax percentage to deduct (default: 15%)
   - **Payment Period**: Description of payment period (e.g., "February 2026")

5. Click "Calculate Payroll" to see the calculation summary
6. Review the detailed breakdown in the summary box
7. Click "Process Payment" to save the payroll record

### Understanding the Payroll Calculation

The system calculates payroll as follows:

```
Regular Pay = Regular Hours × Hourly Rate
Overtime Pay = Overtime Hours × Hourly Rate × 1.5
Gross Salary = Regular Pay + Overtime Pay
Tax Deduction = Gross Salary × Tax Rate %
Total Deductions = Tax + Insurance
Net Salary = Gross Salary - Total Deductions
```

**Example Calculation:**
```
Employee: John Smith
Hourly Rate: $50.00
Regular Hours: 160 @ $50.00/hr
Overtime Hours: 10 @ $75.00/hr (1.5x rate)

Regular Pay:                            $8,000.00
Overtime Pay:                           $  750.00
                                        ----------
GROSS SALARY:                           $8,750.00

Tax Deduction (15%):                    $1,312.50
Insurance:                              $   50.00
                                        ----------
Total Deductions:                       $1,362.50

NET SALARY:                             $7,387.50
```

### Viewing Payroll History

The bottom panel shows all processed payroll records with:
- Payroll ID
- Employee Name
- Regular Hours
- Overtime Hours
- Gross Salary
- Tax Deduction
- Insurance
- Net Salary
- Payment Date
- Payment Period

Records are sorted by date (most recent first).

## Common Workflows

### Monthly Payroll Processing

1. Go to "Payroll Management" tab
2. For each employee:
   - Select employee
   - Enter actual hours worked
   - Enter overtime hours
   - Verify/adjust insurance amount
   - Click "Calculate Payroll"
   - Review calculation
   - Click "Process Payment"
3. Review payroll history to ensure all employees are processed

### Hiring a New Employee

1. Go to "Employee Management" tab
2. Fill in all employee details
3. Click "Add Employee"
4. Verify employee appears in the list

### Giving a Raise

1. Go to "Employee Management" tab
2. Select the employee from the list
3. Update the "Hourly Rate" field
4. Click "Update Employee"

### Year-End Review

1. Go to "Payroll Management" tab
2. Review payroll history for the entire year
3. Export data if needed (future feature)

## Tips and Best Practices

### Data Entry
- **Email addresses must be unique** - each employee needs a different email
- **Use consistent date format** - YYYY-MM-DD (e.g., 2026-02-14)
- **Verify calculations** - Always review the calculation summary before processing
- **Keep insurance amounts updated** - Adjust as needed for each employee

### Regular Tasks
- **Backup database regularly** - Copy the `payroll.db` file to a safe location
- **Process payroll on time** - Maintain a consistent payment schedule
- **Update employee information** - Keep contact details and rates current

### Error Prevention
- **Double-check before deleting** - Deleted employees cannot be recovered
- **Review payroll before processing** - Ensure hours and rates are correct
- **Verify email addresses** - Must be in valid email format

## Database Information

The application uses SQLite database (`payroll.db`) stored in the same directory as the application.

### Database Location
```
-employee-payroll-system/
  └── payroll.db  (created automatically on first run)
```

### Backup Procedure
1. Close the application
2. Copy `payroll.db` to a backup location
3. Restore by replacing `payroll.db` with the backup

## Troubleshooting

### Problem: Application won't start
**Solution:** 
- Ensure Python 3.6+ is installed
- Check that Tkinter is available: `python -c "import tkinter"`
- Try: `python3 payroll_system.py`

### Problem: "Email already exists" error
**Solution:** Each employee must have a unique email address. Use a different email or add a number (e.g., john.smith2@company.com)

### Problem: Calculation seems wrong
**Solution:** 
- Verify hourly rate is correct
- Check regular hours and overtime hours
- Remember: overtime is calculated at 1.5x the hourly rate
- Tax is calculated on gross salary (before deductions)

### Problem: Can't update employee
**Solution:**
- Make sure an employee is selected from the list
- Check that the email isn't already used by another employee
- Verify all required fields are filled

### Problem: Database file locked
**Solution:**
- Close any other instances of the application
- Ensure no other program is accessing payroll.db

## Keyboard Shortcuts

- **Tab**: Move to next field
- **Shift+Tab**: Move to previous field
- **Enter**: Submit form (when in text field)
- **Escape**: Close dialog boxes

## Data Export

Currently, payroll data is stored in SQLite database. To export:

1. Use SQLite browser tools (e.g., DB Browser for SQLite)
2. Or write a custom export script
3. Access database at: `payroll.db`

## Security Notes

- **Database is not encrypted** - Keep in a secure location
- **No user authentication** - Anyone who can run the app can access all data
- **Backup regularly** - Protect against data loss
- **Email validation** - System enforces unique emails
- **No SQL injection vulnerabilities** - Uses parameterized queries

## Support and Contact

For issues or questions:
- Check the README.md file
- Visit the GitHub repository
- Run the demo.py script to see examples

## Version History

**Version 1.0** (February 2026)
- Initial release
- Employee management (CRUD)
- Payroll calculation and processing
- SQLite database
- Tkinter GUI
- Comprehensive validation

---

*For developers: See README.md for technical documentation and API details.*
