# Employee Payroll Management System

A comprehensive desktop application for managing employee information, attendance, and payroll calculations built with Python and Tkinter.

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue?style=for-the-badge&logo=github)](https://github.com/dhanshree200504/-employee-payroll-system)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Stars](https://img.shields.io/github/stars/dhanshree200504/-employee-payroll-system?style=for-the-badge)](https://github.com/dhanshree200504/-employee-payroll-system/stargazers)

---

## 🔗 Quick Links

| Resource | Link |
|----------|------|
| 📦 **GitHub Repository** | [https://github.com/dhanshree200504/-employee-payroll-system](https://github.com/dhanshree200504/-employee-payroll-system) |
| 📥 **Download Project** | [Download ZIP](https://github.com/dhanshree200504/-employee-payroll-system/archive/refs/heads/main.zip) |
| 📖 **Documentation** | [Read Full Docs](https://github.com/dhanshree200504/-employee-payroll-system#readme) |
| 🐛 **Report Bug** | [Create Issue](https://github.com/dhanshree200504/-employee-payroll-system/issues) |
| ✨ **Request Feature** | [Create Issue](https://github.com/dhanshree200504/-employee-payroll-system/issues) |

---

## 📋 Features

### Employee Management
- ✅ Add, view, update, and delete employee records
- ✅ Store comprehensive employee information (personal, contact, professional)
- ✅ Upload and display employee ID card photos
- ✅ Generate employee ID cards with photos
- ✅ Search and filter employees by various criteria

### Attendance Tracking
- ✅ Record daily attendance (Present/Absent/Half Day/Leave)
- ✅ View attendance history for each employee
- ✅ Monthly attendance summary
- ✅ Calculate working days automatically

### Payroll Processing
- ✅ Automatic salary calculation based on attendance
- ✅ Support for multiple salary components (Basic, HRA, DA, etc.)
- ✅ Deductions management (PF, Tax, Insurance)
- ✅ Monthly payroll generation
- ✅ Payroll history tracking

### Reporting
- ✅ Employee-wise salary reports
- ✅ Department-wise analysis
- ✅ Attendance reports
- ✅ Export capabilities

## 🖥️ Screenshots

### Main Dashboard
The application features a clean, intuitive tabbed interface for easy navigation between different modules.

### Employee Management
Comprehensive form for adding and editing employee information with photo upload support.

### ID Card Generation
Automatically generate professional employee ID cards with employee photos and information.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

**Option 1: Clone with Git**
```bash
git clone https://github.com/dhanshree200504/-employee-payroll-system.git
cd -employee-payroll-system
pip install -r requirements.txt
python payroll_app.py
```

**Option 2: Download ZIP**
1. [Download ZIP file](https://github.com/dhanshree200504/-employee-payroll-system/archive/refs/heads/main.zip)
2. Extract the ZIP file
3. Open terminal/command prompt in the extracted folder
4. Run the following commands:
```bash
pip install -r requirements.txt
python payroll_app.py
```

## 📦 Dependencies

- **tkinter** - GUI framework (usually comes with Python)
- **Pillow (PIL)** - Image processing for ID cards
- **sqlite3** - Database (included in Python standard library)

Install all dependencies:
```bash
pip install -r requirements.txt
```

## 💾 Database Structure

The application uses SQLite database with the following tables:

### Employees Table
Stores all employee information including personal details, contact information, professional details, and bank information.

### Attendance Table
Records daily attendance for each employee with date, status, and remarks.

### Payroll Table
Maintains salary payment records with all components and deductions.

## 📖 Usage Guide

### Adding a New Employee

1. Navigate to the "Employee Management" tab
2. Fill in all required employee information
3. Upload an employee photo (optional)
4. Click "Add Employee" to save

### Recording Attendance

1. Go to the "Attendance" tab
2. Select employee from dropdown
3. Choose date and attendance status
4. Add remarks if needed
5. Click "Mark Attendance"

### Generating Payroll

1. Open the "Payroll" tab
2. Select employee and month/year
3. Enter salary components and deductions
4. System automatically calculates net salary based on attendance
5. Click "Generate Payroll" to save

### Generating ID Cards

1. Select an employee from the employee list
2. Click "Generate ID Card"
3. ID card will be created with employee photo and details

## 🔧 Configuration

### Database Location
By default, the database file `payroll.db` is created in the application directory.

### ID Card Images
Employee photos are stored in the database as BLOB data and can be exported as needed.

## 🛣️ Roadmap

See [IMPROVEMENTS.md](IMPROVEMENTS.md) for a detailed list of planned features and enhancements.

### Upcoming Features (v1.1)
- PDF payslip generation
- Enhanced reporting dashboard
- Date picker widgets
- Improved error handling and validation

### Future Enhancements (v2.0+)
- User authentication and role-based access
- Multi-user support with MySQL/PostgreSQL
- Leave management system
- Email notifications
- REST API for mobile integration

## 🐛 Known Limitations

- Single-user application (no concurrent access)
- SQLite database (not suitable for large-scale deployment)
- No built-in backup mechanism
- Limited to local deployment

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Dhanshree Porwal**
- GitHub: [@dhanshree200504](https://github.com/dhanshree200504)
- Project Link: [https://github.com/dhanshree200504/-employee-payroll-system](https://github.com/dhanshree200504/-employee-payroll-system)

## 🙏 Acknowledgments

- Built with Python and Tkinter
- Database management with SQLite
- Image processing with Pillow

## 📞 Support

If you encounter any issues or have questions:
- **Open an issue**: [Create Issue](https://github.com/dhanshree200504/-employee-payroll-system/issues)
- **Email**: dhanshree200504@github.com

## ⭐ Show Your Support

If you find this project useful, please consider giving it a star! ⭐

[![GitHub stars](https://img.shields.io/github/stars/dhanshree200504/-employee-payroll-system?style=social)](https://github.com/dhanshree200504/-employee-payroll-system/stargazers)

---

## 📥 Quick Actions

**📦 [View on GitHub](https://github.com/dhanshree200504/-employee-payroll-system)** | **⬇️ [Download ZIP](https://github.com/dhanshree200504/-employee-payroll-system/archive/refs/heads/main.zip)** | **🐛 [Report Bug](https://github.com/dhanshree200504/-employee-payroll-system/issues)** | **✨ [Request Feature](https://github.com/dhanshree200504/-employee-payroll-system/issues)**

---

*Last Updated: February 2026*
*Developed by Dhanshree Porwal*
