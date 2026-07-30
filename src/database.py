import sqlite3
from pathlib import Path

# Database Path
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "student.db"


def connect():
    """Connect to SQLite Database"""
    return sqlite3.connect(DB_PATH)


def create_table():
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT UNIQUE NOT NULL,
            course TEXT NOT NULL,
            email TEXT,
            phone TEXT
        )
    """)

    connection.commit()
    connection.close()


def add_student(name, roll_no, course, email, phone):
    connection = connect()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO students(name, roll_no, course, email, phone)
            VALUES (?, ?, ?, ?, ?)
        """, (name, roll_no, course, email, phone))

        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()


def get_students():
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    connection.close()

    return students
def search_students(keyword):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM students
        WHERE name LIKE ?
        OR roll_no LIKE ?
        OR course LIKE ?
    """, (
        f"%{keyword}%",
        f"%{keyword}%",
        f"%{keyword}%"
    ))

    students = cursor.fetchall()

    connection.close()

    return students
def search_students(keyword):

    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM students
        WHERE name LIKE ?
        OR roll_no LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%"))

    students = cursor.fetchall()

    connection.close()

    return students


create_table()
def update_student(student_id, name, roll_no, course, email, phone):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE students
        SET name=?, roll_no=?, course=?, email=?, phone=?
        WHERE id=?
    """, (name, roll_no, course, email, phone, student_id))

    connection.commit()
    connection.close()
def delete_student(student_id):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (student_id,)
    )

    connection.commit()
    connection.close()

create_table()