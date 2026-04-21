from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QLineEdit, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt

import database

class ThemeManager:
    LIGHT_THEME = """
    QMainWindow { background-color: #f5f5f5; }
    QTableWidget { background-color: #ffffff; color: #333333; gridline-color: #e0e0e0; }
    QHeaderView::section { background-color: #e0e0e0; padding: 4px; font-weight: bold; border: 1px solid #d0d0d0; }
    QPushButton { background-color: #2196F3; color: white; border: none; padding: 8px 16px; border-radius: 4px; }
    QPushButton:hover { background-color: #1976D2; }
    QLineEdit { padding: 6px; border: 1px solid #ccc; border-radius: 4px; background-color: white; color: black; }
    QLabel { color: #333333; }
    """

    DARK_THEME = """
    QMainWindow { background-color: #1e1e1e; }
    QTableWidget { background-color: #2d2d2d; color: #e0e0e0; gridline-color: #404040; border: 1px solid #404040; }
    QHeaderView::section { background-color: #333333; color: #e0e0e0; padding: 4px; font-weight: bold; border: 1px solid #404040; }
    QPushButton { background-color: #0d47a1; color: white; border: none; padding: 8px 16px; border-radius: 4px; }
    QPushButton:hover { background-color: #1565c0; }
    QLineEdit { padding: 6px; border: 1px solid #555; border-radius: 4px; background-color: #333333; color: white; }
    QLabel { color: #e0e0e0; }
    QMessageBox { background-color: #2d2d2d; color: #e0e0e0; }
    """

class InputPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.name_entry = QLineEdit()
        self.name_entry.setPlaceholderText("Name")
        
        self.major_entry = QLineEdit()
        self.major_entry.setPlaceholderText("Major")
        
        self.gpa_entry = QLineEdit()
        self.gpa_entry.setPlaceholderText("GPA")
        self.gpa_entry.setMaximumWidth(80)

        self.btn_add = QPushButton("Add/Update Student")

        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_entry)
        layout.addWidget(QLabel("Major:"))
        layout.addWidget(self.major_entry)
        layout.addWidget(QLabel("GPA:"))
        layout.addWidget(self.gpa_entry)
        layout.addWidget(self.btn_add)

    def get_data(self):
        return self.name_entry.text().strip(), self.major_entry.text().strip(), self.gpa_entry.text().strip()

    def clear_inputs(self):
        self.name_entry.clear()
        self.major_entry.clear()
        self.gpa_entry.clear()


class ActionPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.btn_load = QPushButton("Load All")
        self.btn_filter = QPushButton("Filter GPA > 3.0")
        self.btn_update = QPushButton("Update Random")
        self.btn_delete = QPushButton("Delete GPA < 2.0")

        layout.addWidget(self.btn_load)
        layout.addWidget(self.btn_filter)
        layout.addWidget(self.btn_update)
        layout.addWidget(self.btn_delete)


class TablePanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Major", "GPA"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        layout.addWidget(self.table)

    def display_records(self, records):
        self.table.setRowCount(0)
        for row_idx, row_data in enumerate(records):
            self.table.insertRow(row_idx)
            for col_idx, col_data in enumerate(row_data):
                val = f"{col_data:.2f}" if isinstance(col_data, float) else str(col_data)
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter if col_idx == 0 or col_idx == 3 else Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(row_idx, col_idx, item)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management")
        self.resize(750, 550)
        
        self.is_dark_mode = False

        self.init_ui()
        self.connect_signals()
        self.apply_theme()
        
        self.load_all()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        self.action_panel = ActionPanel()
        self.input_panel = InputPanel()
        self.table_panel = TablePanel()
        
        self.btn_toggle_theme = QPushButton("Toggle Dark/Light Mode")
        theme_layout = QHBoxLayout()
        theme_layout.addStretch()
        theme_layout.addWidget(self.btn_toggle_theme)

        main_layout.addLayout(theme_layout)
        main_layout.addWidget(self.action_panel)
        main_layout.addWidget(self.input_panel)
        main_layout.addWidget(self.table_panel)

    def apply_theme(self):
        if self.is_dark_mode:
            self.setStyleSheet(ThemeManager.DARK_THEME)
        else:
            self.setStyleSheet(ThemeManager.LIGHT_THEME)

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()

    def connect_signals(self):
        self.btn_toggle_theme.clicked.connect(self.toggle_theme)
        self.action_panel.btn_load.clicked.connect(self.load_all)
        self.action_panel.btn_filter.clicked.connect(self.filter_high_gpa)
        self.action_panel.btn_update.clicked.connect(self.update_random)
        self.action_panel.btn_delete.clicked.connect(self.delete_low_gpa)
        self.input_panel.btn_add.clicked.connect(self.add_student)

    def load_all(self):
        records = database.get_all_students()
        self.table_panel.display_records(records)

    def filter_high_gpa(self):
        records = database.get_high_gpa_students(3.0)
        self.table_panel.display_records(records)

    def update_random(self):
        reply = QMessageBox.question(
            self, 'Confirm Update',
            "Are you sure you want to update a random student's GPA?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            database.update_random_student_gpa()
            self.load_all()

    def delete_low_gpa(self):
        reply = QMessageBox.question(
            self, 'Confirm Delete',
            'Are you sure you want to delete all students with GPA < 2.0?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            database.delete_low_gpa_students(2.0)
            self.load_all()

    def add_student(self):
        name, major, gpa_str = self.input_panel.get_data()

        if not name or not major or not gpa_str:
            QMessageBox.warning(self, "Input Error", "Please fill all fields")
            return

        try:
            gpa = float(gpa_str)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "GPA must be a valid number")
            return

        existing_student = database.get_student_by_name(name)
        if existing_student:
            reply = QMessageBox.question(
                self, 'Student Exists',
                f"Student '{name}' already exists. Do you want to update their data?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                database.update_student(existing_student[0], name, major, gpa)
                self.load_all()
                self.input_panel.clear_inputs()
        else:
            reply = QMessageBox.question(
                self, 'Confirm Add',
                f"Are you sure you want to add student '{name}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                database.add_student(name, major, gpa)
                self.load_all()
                self.input_panel.clear_inputs()
