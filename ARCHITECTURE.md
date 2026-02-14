# System Architecture

## Employee Payroll Management System - Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    PAYROLL MANAGEMENT SYSTEM                     │
│                     (payroll_system.py)                          │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │
        ┌───────────────────────┴───────────────────────┐
        │                                               │
        ▼                                               ▼
┌──────────────────┐                          ┌──────────────────┐
│   GUI LAYER      │                          │  DATABASE LAYER  │
│   (Tkinter)      │                          │   (SQLite3)      │
└──────────────────┘                          └──────────────────┘
        │                                               │
        │                                               │
   ┌────┴────┐                                    ┌────┴─────┐
   │         │                                    │          │
   ▼         ▼                                    ▼          ▼
┌─────┐  ┌────────┐                         ┌──────────┐ ┌─────────┐
│ Emp │  │Payroll │                         │Employees │ │ Payroll │
│ Tab │  │  Tab   │                         │  Table   │ │  Table  │
└─────┘  └────────┘                         └──────────┘ └─────────┘
```

## Component Details

### 1. GUI Layer (Tkinter)

#### Main Application Window
```
┌────────────────────────────────────────────────────────────┐
│  Employee Payroll Management System                         │
│  Manage employees and process payroll efficiently          │
├────────────────────────────────────────────────────────────┤
│  ┌─────────────────────┬──────────────────────┐           │
│  │ Employee Management │ Payroll Management   │  ← Tabs   │
│  └─────────────────────┴──────────────────────┘           │
│  ┌──────────────────────────────────────────────────────┐ │
│  │                                                       │ │
│  │              Tab Content Area                        │ │
│  │                                                       │ │
│  └──────────────────────────────────────────────────────┘ │
├────────────────────────────────────────────────────────────┤
│  Status: Ready                                             │
└────────────────────────────────────────────────────────────┘
```

#### Employee Management Tab Layout
```
┌─────────────────────────────────────────────────────────────┐
│ ┌───────────────────┐  ┌────────────────────────────────┐  │
│ │ Employee Form     │  │ Employee List                  │  │
│ │                   │  │                                │  │
│ │ Name:      [____] │  │ ┌────┬──────┬──────┬────────┐ │  │
│ │ Email:     [____] │  │ │ ID │ Name │Email │ Rate   │ │  │
│ │ Phone:     [____] │  │ ├────┼──────┼──────┼────────┤ │  │
│ │ Department:[____] │  │ │ 1  │ John │ j@.. │ $50.00 │ │  │
│ │ Position:  [____] │  │ │ 2  │ Jane │ ja.. │ $45.00 │ │  │
│ │ Rate:      [____] │  │ └────┴──────┴──────┴────────┘ │  │
│ │ Hire Date: [____] │  │                                │  │
│ │                   │  │                                │  │
│ │ [Add] [Update]    │  │                                │  │
│ │ [Delete] [Clear]  │  │                                │  │
│ └───────────────────┘  └────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

#### Payroll Management Tab Layout
```
┌─────────────────────────────────────────────────────────────┐
│ ┌───────────────────────────────────────────────────────┐   │
│ │ Process Payroll                                       │   │
│ │                                                       │   │
│ │ Employee: [John Doe ▼]     Rate: $50.00             │   │
│ │                                                       │   │
│ │ Regular Hours: [160]       Tax Rate: [15]%          │   │
│ │ Overtime:      [10]        Insurance: [$50]          │   │
│ │                            Period: [Feb 2026]        │   │
│ │                                                       │   │
│ │ [Calculate] [Process Payment] [Clear]                │   │
│ │                                                       │   │
│ │ ┌───────────────────────────────────────────────┐    │   │
│ │ │ CALCULATION SUMMARY                           │    │   │
│ │ │ Regular Pay:              $8,000.00          │    │   │
│ │ │ Overtime Pay:             $  750.00          │    │   │
│ │ │ Gross Salary:             $8,750.00          │    │   │
│ │ │ Tax:                      $1,312.50          │    │   │
│ │ │ NET SALARY:               $7,387.50          │    │   │
│ │ └───────────────────────────────────────────────┘    │   │
│ └───────────────────────────────────────────────────────┘   │
│                                                             │
│ ┌───────────────────────────────────────────────────────┐   │
│ │ Payroll History                                       │   │
│ │ ┌────┬──────┬─────┬────┬───────┬─────┬──────────┐    │   │
│ │ │ ID │ Name │ Hrs │ OT │ Gross │ Tax │   Net    │    │   │
│ │ ├────┼──────┼─────┼────┼───────┼─────┼──────────┤    │   │
│ │ │ 1  │ John │ 160 │ 10 │ 8750  │1313 │ 7387.50  │    │   │
│ │ └────┴──────┴─────┴────┴───────┴─────┴──────────┘    │   │
│ └───────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 2. Database Layer (SQLite)

#### Database Schema
```
┌──────────────────────────────────────┐
│          EMPLOYEES TABLE              │
├──────────────────────────────────────┤
│ emp_id (PK)      INTEGER             │
│ name             TEXT                │
│ email            TEXT (UNIQUE)       │
│ phone            TEXT                │
│ department       TEXT                │
│ position         TEXT                │
│ hourly_rate      REAL                │
│ hire_date        TEXT                │
│ status           TEXT                │
└──────────────────────────────────────┘
         │
         │ 1:N relationship
         │
         ▼
┌──────────────────────────────────────┐
│           PAYROLL TABLE               │
├──────────────────────────────────────┤
│ payroll_id (PK)  INTEGER             │
│ emp_id (FK)      INTEGER             │
│ hours_worked     REAL                │
│ overtime_hours   REAL                │
│ gross_salary     REAL                │
│ tax_deduction    REAL                │
│ insurance        REAL                │
│ net_salary       REAL                │
│ payment_date     TEXT                │
│ payment_period   TEXT                │
└──────────────────────────────────────┘
```

## Data Flow

### Adding an Employee
```
User Input → Validation → Database Insert → Update UI List
```

### Processing Payroll
```
1. Select Employee
2. Enter Hours & Deductions
3. Calculate:
   - Regular Pay = Hours × Rate
   - Overtime Pay = OT Hours × Rate × 1.5
   - Gross = Regular + Overtime
   - Tax = Gross × Tax%
   - Net = Gross - Tax - Insurance
4. Display Summary
5. Save to Database
6. Update History List
```

## Class Hierarchy

```
PayrollManagementSystem (Main Application)
    │
    ├─── PayrollDatabase
    │       └─── SQLite Operations
    │
    ├─── EmployeeManagementTab
    │       ├─── Form Widgets
    │       ├─── Employee List (Treeview)
    │       └─── CRUD Operations
    │
    └─── PayrollManagementTab
            ├─── Calculation Form
            ├─── Payroll History (Treeview)
            └─── Payroll Processing
```

## Key Features

### 1. Employee Management
- ✓ Add new employees
- ✓ View all employees
- ✓ Update employee information
- ✓ Delete employees
- ✓ Unique email validation
- ✓ Data persistence

### 2. Payroll Processing
- ✓ Calculate regular pay
- ✓ Calculate overtime (1.5x rate)
- ✓ Tax deduction calculation
- ✓ Insurance deduction
- ✓ Net salary computation
- ✓ Payment tracking
- ✓ Historical records

### 3. Data Validation
- ✓ Required field validation
- ✓ Email format validation
- ✓ Email uniqueness check
- ✓ Numeric validation
- ✓ Positive value validation

### 4. User Interface
- ✓ Tabbed navigation
- ✓ Form-based input
- ✓ Table view for lists
- ✓ Confirmation dialogs
- ✓ Error messages
- ✓ Success notifications

## Technology Stack

```
┌─────────────────────────┐
│   Python 3.6+           │
├─────────────────────────┤
│ • Tkinter (GUI)         │
│ • SQLite3 (Database)    │
│ • datetime (Dates)      │
└─────────────────────────┘
```

## File Structure

```
-employee-payroll-system/
│
├── payroll_system.py          # Main application
├── demo.py                    # Demo script
├── test_payroll_standalone.py # Test suite
├── requirements.txt           # Dependencies
├── README.md                  # Documentation
├── USER_GUIDE.md             # User manual
├── ARCHITECTURE.md           # This file
├── .gitignore                # Git ignore rules
│
└── payroll.db                # Database (created at runtime)
```

## Security Considerations

1. **SQL Injection Prevention**: Uses parameterized queries
2. **Data Validation**: Input validation on all fields
3. **Email Uniqueness**: Database constraint
4. **Error Handling**: Try-catch blocks for all operations
5. **Data Integrity**: Foreign key constraints

## Future Enhancements (Possible)

- [ ] User authentication and roles
- [ ] Password-protected database
- [ ] Export to Excel/CSV
- [ ] Email notifications
- [ ] Backup automation
- [ ] Multiple pay rates
- [ ] Benefits tracking
- [ ] Time off management
- [ ] Reports and analytics
- [ ] Multi-currency support
