# Student Management System

A desktop application for managing student records, built with **Python**, **PyQt6**, and **SQLite**. This project implements a clean separation of concerns between the graphical user interface and database operations, fulfilling core CRUD (Create, Read, Update, Delete) requirements.

## 🌟 Features

- **Local Database Management**: Data is stored locally using SQLite3. The application automatically initializes the database and populates it with sample data on the first run.
- **Modern Graphical Interface**: Built using PyQt6, featuring an intuitive layout with a data table, input forms, and action buttons.
- **Dynamic Theme Support**: Automatic detection of the system's dark/light mode, alongside a manual theme toggle button for customized viewing.
- **Smart Search (Fuzzy Matching)**: Utilizes Python's `difflib` for error-tolerant searching when selecting a student to update.
- **Data Filtering & Bulk Actions**:
  - Filter and view students with a **GPA > 3.0**.
  - Bulk delete students with a **GPA < 2.0** with a confirmation dialog.
  - Add new students or update existing student records with built-in input validation.

## 📂 Project Structure

| File / Directory | Description |
| :--- | :--- |
| `main.py` | Application entry point |
| `gui.py` | PyQt6 user interface, layouts, and ThemeManager |
| `database.py` | SQLite database connection and CRUD queries |
| `problem.md` | Original task requirements |
| `README.md` | Project documentation |

*(Note: `university.db` is automatically generated in the root directory upon first execution.)*

## 🛠️ Technologies Used

- **Language**: Python 3
- **GUI Framework**: PyQt6
- **Database**: SQLite3 (Standard Library)
- **Utilities**: `difflib` (Standard Library)

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3 installed on your system. You will need to install the `PyQt6` dependency:

```bash
pip install PyQt6
```

### Running the Application

1. Clone this repository or navigate to the project directory.
2. Execute the main script:

```bash
python main.py
```

## 📝 Implemented Database Operations

The codebase was developed to fulfill the following core SQL requirements:
1. **Initialize**: Creates `university.db` and the `students` table (`id`, `name`, `major`, `gpa`).
2. **Insert**: Adds at least 5 sample students to the database automatically.
3. **Query**: Fetches all students or filters for high-performing students (`GPA > 3.0`).
4. **Update**: Modifies the GPA and details of any selected student.
5. **Delete**: Cleans up the database by removing records of students with low GPAs (`GPA < 2.0`).