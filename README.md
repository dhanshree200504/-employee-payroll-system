# Employee Payroll Management System

A comprehensive Employee Payroll Management System built with Python and Tkinter. This application provides a complete solution for managing employees and processing payroll with an intuitive graphical user interface.

## Features

### Employee Management
- **Add Employees**: Register new employees with complete information
- **View Employees**: Browse all employees in an organized table view
- **Update Employees**: Modify employee information easily
- **Delete Employees**: Remove employees from the system
- **Employee Details**: Track name, email, phone, department, position, hourly rate, and hire date

### Payroll Management
- **Calculate Payroll**: Automatically calculate salaries based on hours worked
- **Overtime Support**: Handle overtime hours with 1.5x rate
- **Tax Deductions**: Calculate tax deductions based on configurable tax rates
- **Insurance Deductions**: Include insurance and other deductions
- **Payment Processing**: Save and track payroll records
- **Payroll History**: View complete payment history for all employees
- **Detailed Reports**: Generate comprehensive payroll calculation summaries

## Technology Stack

- **Language**: Python 3.6+
- **GUI Framework**: Tkinter (Python standard library)
- **Database**: SQLite3 (Python standard library)
- **Date/Time**: datetime module

## Installation

### Prerequisites
- Python 3.6 or higher

### Setup
1. Clone the repository:
```bash
git clone https://github.com/dhanshree200504/-employee-payroll-system.git
cd -employee-payroll-system
```

2. No additional dependencies required - the application uses only Python standard library modules.

## Usage

### Running the Application
```bash
python payroll_system.py
```

or on some systems:
```bash
python3 payroll_system.py
```

### Using the Application

#### Employee Management Tab
1. **Adding an Employee**:
   - Fill in all required fields (Name, Email, Department, Position, Hourly Rate)
   - Optional: Add phone number
   - Click "Add Employee"

2. **Updating an Employee**:
   - Select an employee from the list
   - Modify the fields as needed
   - Click "Update Employee"

3. **Deleting an Employee**:
   - Select an employee from the list
   - Click "Delete Employee"
   - Confirm the deletion

#### Payroll Management Tab
1. **Processing Payroll**:
   - Select an employee from the dropdown
   - Enter regular hours worked (default: 160 hours/month)
   - Enter overtime hours if applicable
   - Set tax rate percentage (default: 15%)
   - Set insurance amount (default: $50)
   - Click "Calculate Payroll" to see the breakdown
   - Click "Process Payment" to save the payroll record

2. **Viewing Payroll History**:
   - All processed payroll records appear in the bottom table
   - View details including gross salary, deductions, and net salary

## Database Schema

The application uses SQLite database (`payroll.db`) with two main tables:

### Employees Table
- `emp_id`: Primary key (auto-increment)
- `name`: Employee name
- `email`: Unique email address
- `phone`: Contact phone number
- `department`: Department name
- `position`: Job position
- `hourly_rate`: Hourly wage rate
- `hire_date`: Date of hire
- `status`: Active/Inactive status

### Payroll Table
- `payroll_id`: Primary key (auto-increment)
- `emp_id`: Foreign key to employees
- `hours_worked`: Regular hours worked
- `overtime_hours`: Overtime hours
- `gross_salary`: Total salary before deductions
- `tax_deduction`: Tax amount deducted
- `insurance`: Insurance deduction
- `net_salary`: Final salary after deductions
- `payment_date`: Date of payment
- `payment_period`: Payment period (e.g., "January 2024")

## Features in Detail

### Automatic Calculations
- **Regular Pay**: Hours × Hourly Rate
- **Overtime Pay**: Overtime Hours × Hourly Rate × 1.5
- **Gross Salary**: Regular Pay + Overtime Pay
- **Tax Deduction**: Gross Salary × Tax Rate %
- **Net Salary**: Gross Salary - Tax - Insurance

### Data Validation
- Required field validation
- Email uniqueness validation
- Numeric input validation
- Positive value validation for rates and hours

### User Interface
- Clean, modern interface using Tkinter
- Tabbed navigation for different functions
- Tree view for browsing employees and payroll records
- Form-based data entry
- Confirmation dialogs for destructive operations
- Status messages for user feedback

## Screenshots

The application features a two-tab interface:
1. **Employee Management Tab**: Manage all employee information
2. **Payroll Management Tab**: Process payroll and view history

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available for educational purposes.

## Author

Created by Dhanshree

## Support

For issues, questions, or contributions, please visit the GitHub repository.