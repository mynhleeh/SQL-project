import sqlite3
import random

DB_NAME = "university.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                major TEXT,
                gpa REAL
            )
        ''')
        cursor.execute("SELECT COUNT(*) FROM students")
        if cursor.fetchone()[0] == 0:
            sample_data = [
                ("Alice Smith", "Computer Science", 3.8),
                ("Bob Jones", "Mathematics", 2.9),
                ("Charlie Brown", "Physics", 1.5),
                ("Diana Prince", "Engineering", 4.0),
                ("Evan Wright", "History", 2.5)
            ]
            cursor.executemany("INSERT INTO students (name, major, gpa) VALUES (?, ?, ?)", sample_data)
        conn.commit()

def fetch_records(query, params=()):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

def get_all_students():
    return fetch_records("SELECT * FROM students")

def get_high_gpa_students(min_gpa=3.0):
    return fetch_records("SELECT * FROM students WHERE gpa > ?", (min_gpa,))

def update_random_student_gpa():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM students")
        ids = [row[0] for row in cursor.fetchall()]
        if ids:
            target_id = random.choice(ids)
            new_gpa = round(random.uniform(1.0, 4.0), 2)
            cursor.execute("UPDATE students SET gpa = ? WHERE id = ?", (new_gpa, target_id))
            conn.commit()

def delete_low_gpa_students(max_gpa=2.0):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE gpa < ?", (max_gpa,))
        conn.commit()

def get_student_by_name(name):
    records = fetch_records("SELECT * FROM students WHERE name = ?", (name,))
    return records[0] if records else None

def add_student(name, major, gpa):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, major, gpa) VALUES (?, ?, ?)", (name, major, gpa))
        conn.commit()

def update_student(student_id, name, major, gpa):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE students SET name = ?, major = ?, gpa = ? WHERE id = ?", (name, major, gpa, student_id))
        conn.commit()
