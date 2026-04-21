from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QLineEdit, QLabel, QMessageBox, QApplication, QDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette
import difflib

import database

class ThemeManager:
    LIGHT_THEME = """
    QMainWindow { background-color: #f5f5f5; }
    QTableWidget { 
        background-color: #ffffff; 
        color: #000000; 
        gridline-color: #c0c0c0; 
        selection-background-color: #bbdefb;
        selection-color: #000000;
    }
    QHeaderView::section { 
        background-color: #e0e0e0; 
        color: #000000;
        padding: 6px; 
        font-weight: bold; 
        border: 1px solid #c0c0c0; 
    }
    QPushButton { background-color: #2196F3; color: white; border: none; padding: 10px 16px; border-radius: 4px; font-weight: bold; }
    QPushButton:hover { background-color: #1976D2; }
    QLineEdit { padding: 8px; border: 1px solid #aaa; border-radius: 4px; background-color: white; color: black; }
    QLabel { color: #000000; font-weight: bold; }
    """

    DARK_THEME = """
    QMainWindow { background-color: #121212; }
    QTableWidget { 
        background-color: #1e1e1e; 
        color: #ffffff; 
        gridline-color: #555555; 
        border: 1px solid #555555; 
        selection-background-color: #1976D2;
        selection-color: #ffffff;
    }
    QHeaderView::section { 
        background-color: #2c2c2c; 
        color: #ffffff; 
        padding: 6px; 
        font-weight: bold; 
        border: 1px solid #555555; 
    }
    QPushButton { background-color: #1976D2; color: white; border: none; padding: 10px 16px; border-radius: 4px; font-weight: bold; }
    QPushButton:hover { background-color: #1565c0; }
    QLineEdit { padding: 8px; border: 1px solid #555; border-radius: 4px; background-color: #2c2c2c; color: white; }
    QLabel { color: #ffffff; font-weight: bold; }
    QMessageBox { background-color: #1e1e1e; color: #ffffff; }
    """

class InputPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.name_entry = QLineEdit()
        self.name_entry.setPlaceholderText("Name")
        
        self.major_entry = QLineEdit()
        self.major_entry.setPlaceholderText("Major")
        
        self.gpa_entry = QLineEdit()
        self.gpa_entry.setPlaceholderText("GPA")

        self.btn_add = QPushButton("Add / Update")

        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_entry)
        layout.addWidget(QLabel("Major:"))
        layout.addWidget(self.major_entry)
        layout.addWidget(QLabel("GPA:"))
        layout.addWidget(self.gpa_entry)
        
        layout.addSpacing(5)
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
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.btn_load = QPushButton("Load All")
        self.btn_filter = QPushButton("Filter GPA > 3.0")
        self.btn_update = QPushButton("Update GPA")
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


class UpdateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Update Student GPA")
        self.resize(550, 450)
        
        layout = QVBoxLayout(self)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Major", "GPA"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.itemSelectionChanged.connect(self.on_row_selected)
        
        layout.addWidget(self.table)
        
        input_layout = QHBoxLayout()
        self.name_entry = QLineEdit()
        self.name_entry.setPlaceholderText("Name")
        self.name_entry.textChanged.connect(self.filter_students)
        
        self.gpa_entry = QLineEdit()
        self.gpa_entry.setPlaceholderText("New GPA")
        
        input_layout.addWidget(QLabel("Name:"))
        input_layout.addWidget(self.name_entry)
        input_layout.addWidget(QLabel("GPA:"))
        input_layout.addWidget(self.gpa_entry)
        
        layout.addLayout(input_layout)
        
        self.btn_save = QPushButton("Save Update")
        self.btn_save.clicked.connect(self.save_update)
        layout.addWidget(self.btn_save)
        
        self.selected_id = None
        self.selected_major = ""
        self.all_records = []
        self.load_students()

    def filter_students(self, text):
        search_term = text.lower()
        if not search_term:
            self.display_records(self.all_records)
            return

        filtered = []
        for record in self.all_records:
            name = str(record[1]).lower()
            if search_term in name:
                filtered.append(record)
            else:
                ratio = difflib.SequenceMatcher(None, search_term, name).ratio()
                if ratio > 0.5:
                    filtered.append(record)
        
        self.display_records(filtered)

    def display_records(self, records):
        self.table.setRowCount(0)
        for row_idx, row_data in enumerate(records):
            self.table.insertRow(row_idx)
            for col_idx, col_data in enumerate(row_data):
                val = f"{col_data:.2f}" if isinstance(col_data, float) else str(col_data)
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter if col_idx == 0 or col_idx == 3 else Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(row_idx, col_idx, item)

    def load_students(self):
        self.all_records = database.get_all_students()
        self.display_records(self.all_records)

    def on_row_selected(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            return
        
        row = selected_items[0].row()
        self.selected_id = int(self.table.item(row, 0).text())
        name = self.table.item(row, 1).text()
        self.selected_major = self.table.item(row, 2).text()
        gpa = self.table.item(row, 3).text()
        
        self.name_entry.blockSignals(True)
        self.name_entry.setText(name)
        self.name_entry.blockSignals(False)
        
        self.gpa_entry.setText(gpa)

    def save_update(self):
        name = self.name_entry.text().strip()
        gpa_str = self.gpa_entry.text().strip()
        
        if not name or not gpa_str:
            QMessageBox.warning(self, "Input Error", "Please fill Name and GPA.")
            return

        if self.selected_id is None:
            student = database.get_student_by_name(name)
            if student:
                self.selected_id = student[0]
                self.selected_major = student[2]
            else:
                QMessageBox.warning(self, "Warning", "Student not found. Please select from the list or check the exact name.")
                return
            
        try:
            gpa = float(gpa_str)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "GPA must be a valid number.")
            return
            
        database.update_student(self.selected_id, name, self.selected_major, gpa)
        QMessageBox.information(self, "Success", "Student updated successfully.")
        
        self.selected_id = None
        self.selected_major = ""
        self.load_students()
        
        if self.parent():
            self.parent().load_all()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management")
        self.resize(850, 600)
        
        self.is_dark_mode = self.detect_system_dark_mode()

        self.init_ui()
        self.connect_signals()
        self.apply_theme()
        
        self.load_all()

    def detect_system_dark_mode(self):
        app = QApplication.instance()
        if app:
            palette = app.palette()
            bg_color = palette.color(QPalette.ColorRole.Window)
            text_color = palette.color(QPalette.ColorRole.WindowText)
            # If text is brighter than background, system is likely in dark mode
            return text_color.lightness() > bg_color.lightness()
        return False

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout is horizontal: left panel (buttons/inputs), right panel (table)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Right Panel (Controls)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(20)

        self.btn_toggle_theme = QPushButton("Change Theme")
        
        self.input_panel = InputPanel()
        self.action_panel = ActionPanel()
        
        right_layout.addWidget(self.btn_toggle_theme)
        
        # Add a title for input area
        lbl_inputs = QLabel("Manage Student")
        lbl_inputs.setStyleSheet("font-size: 16px; font-weight: bold;")
        right_layout.addWidget(lbl_inputs)
        right_layout.addWidget(self.input_panel)
        
        right_layout.addSpacing(15)
        
        # Add a title for actions area
        lbl_actions = QLabel("Actions")
        lbl_actions.setStyleSheet("font-size: 16px; font-weight: bold;")
        right_layout.addWidget(lbl_actions)
        right_layout.addWidget(self.action_panel)
        
        right_layout.addStretch() # Push everything up
        
        right_panel.setFixedWidth(250) # Fixed width for the control panel

        # Left Panel (Table)
        self.table_panel = TablePanel()

        main_layout.addWidget(self.table_panel)
        main_layout.addWidget(right_panel)

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
        self.action_panel.btn_update.clicked.connect(self.open_update_dialog)
        self.action_panel.btn_delete.clicked.connect(self.delete_low_gpa)
        self.input_panel.btn_add.clicked.connect(self.add_student)

    def load_all(self):
        records = database.get_all_students()
        self.table_panel.display_records(records)

    def filter_high_gpa(self):
        records = database.get_high_gpa_students(3.0)
        self.table_panel.display_records(records)

    def open_update_dialog(self):
        dialog = UpdateDialog(self)
        # Apply current theme to dialog
        dialog.setStyleSheet(self.styleSheet())
        dialog.exec()

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
