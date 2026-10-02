import sqlite3


# =========================================================
# DATABASE
# =========================================================

DATABASE_NAME = "school.db"


def connect_db():
    return sqlite3.connect(DATABASE_NAME)


# =========================================================
# CREATE TABLE
# =========================================================

def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    sql = """
    CREATE TABLE IF NOT EXISTS Student (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        major TEXT NOT NULL
    )
    """

    cursor.execute(sql)

    conn.commit()
    conn.close()


# =========================================================
# ADD STUDENT
# =========================================================

def add_student():
    print()
    print("=" * 50)
    print("ADD STUDENT")
    print("=" * 50)

    name = input("Enter name: ")
    age = int(input("Enter age: "))
    major = input("Enter major: ")

    conn = connect_db()
    cursor = conn.cursor()

    sql = """
    INSERT INTO Student (name, age, major)
    VALUES (?, ?, ?)
    """

    cursor.execute(sql, (name, age, major))

    conn.commit()
    conn.close()

    print("Student added successfully!")


# =========================================================
# SHOW ALL STUDENTS
# =========================================================

def show_all_students():
    print()
    print("=" * 70)
    print("STUDENT LIST")
    print("=" * 70)

    conn = connect_db()
    cursor = conn.cursor()

    sql = """
    SELECT id, name, age, major
    FROM Student
    ORDER BY id
    """

    cursor.execute(sql)

    students = cursor.fetchall()

    conn.close()

    if len(students) == 0:
        print("No students found.")
        return

    print(f"{'ID':<5}{'NAME':<25}{'AGE':<10}{'MAJOR':<15}")
    print("-" * 70)

    for student in students:
        student_id = student[0]
        name = student[1]
        age = student[2]
        major = student[3]

        print(
            f"{student_id:<5}"
            f"{name:<25}"
            f"{age:<10}"
            f"{major:<15}"
        )

    print("-" * 70)


# =========================================================
# FIND STUDENT BY ID
# =========================================================

def find_student():
    print()
    print("=" * 50)
    print("FIND STUDENT")
    print("=" * 50)

    student_id = int(input("Enter student ID: "))

    conn = connect_db()
    cursor = conn.cursor()

    sql = """
    SELECT id, name, age, major
    FROM Student
    WHERE id = ?
    """

    cursor.execute(sql, (student_id,))

    student = cursor.fetchone()

    conn.close()

    if student is None:
        print("Student not found!")
        return

    print()
    print("Student information:")
    print("ID    :", student[0])
    print("Name  :", student[1])
    print("Age   :", student[2])
    print("Major :", student[3])


# =========================================================
# FIND STUDENT BY NAME
# =========================================================

def find_by_name():
    print()
    print("=" * 50)
    print("FIND STUDENT BY NAME")
    print("=" * 50)

    name = input("Enter name: ")

    conn = connect_db()
    cursor = conn.cursor()

    sql = """
    SELECT id, name, age, major
    FROM Student
    WHERE name LIKE ?
    ORDER BY id
    """

    cursor.execute(sql, ("%" + name + "%",))

    students = cursor.fetchall()

    conn.close()

    if len(students) == 0:
        print("No student found.")
        return

    print()
    print(f"{'ID':<5}{'NAME':<25}{'AGE':<10}{'MAJOR':<15}")
    print("-" * 70)

    for student in students:
        print(
            f"{student[0]:<5}"
            f"{student[1]:<25}"
            f"{student[2]:<10}"
            f"{student[3]:<15}"
        )


# =========================================================
# UPDATE STUDENT
# =========================================================

def update_student():
    print()
    print("=" * 50)
    print("UPDATE STUDENT")
    print("=" * 50)

    student_id = int(input("Enter student ID: "))

    conn = connect_db()
    cursor = conn.cursor()

    # Check student
    sql_check = """
    SELECT id, name, age, major
    FROM Student
    WHERE id = ?
    """

    cursor.execute(sql_check, (student_id,))

    student = cursor.fetchone()

    if student is None:
        print("Student not found!")
        conn.close()
        return

    print()
    print("Current information:")
    print("Name  :", student[1])
    print("Age   :", student[2])
    print("Major :", student[3])

    print()
    print("Enter new information:")

    name = input("New name: ")
    age = int(input("New age: "))
    major = input("New major: ")

    sql_update = """
    UPDATE Student
    SET name = ?,
        age = ?,
        major = ?
    WHERE id = ?
    """

    cursor.execute(
        sql_update,
        (name, age, major, student_id)
    )

    conn.commit()
    conn.close()

    print("Student updated successfully!")


# =========================================================
# DELETE STUDENT
# =========================================================

def delete_student():
    print()
    print("=" * 50)
    print("DELETE STUDENT")
    print("=" * 50)

    student_id = int(input("Enter student ID: "))

    conn = connect_db()
    cursor = conn.cursor()

    # Check student
    sql_check = """
    SELECT id, name, age, major
    FROM Student
    WHERE id = ?
    """

    cursor.execute(sql_check, (student_id,))

    student = cursor.fetchone()

    if student is None:
        print("Student not found!")
        conn.close()
        return

    print()
    print("Student to delete:")
    print("ID    :", student[0])
    print("Name  :", student[1])
    print("Age   :", student[2])
    print("Major :", student[3])

    confirm = input("Are you sure? (y/n): ")

    if confirm.lower() != "y":
        print("Delete cancelled.")
        conn.close()
        return

    sql_delete = """
    DELETE FROM Student
    WHERE id = ?
    """

    cursor.execute(sql_delete, (student_id,))

    conn.commit()
    conn.close()

    print("Student deleted successfully!")


# =========================================================
# DELETE ALL STUDENTS
# =========================================================

def delete_all_students():
    print()
    print("=" * 50)
    print("DELETE ALL STUDENTS")
    print("=" * 50)

    confirm = input(
        "Are you sure you want to delete ALL students? (y/n): "
    )

    if confirm.lower() != "y":
        print("Delete cancelled.")
        return

    conn = connect_db()
    cursor = conn.cursor()

    sql = "DELETE FROM Student"

    cursor.execute(sql)

    conn.commit()
    conn.close()

    print("All students deleted successfully!")


# =========================================================
# MENU
# =========================================================

def show_menu():
    print()
    print("=" * 50)
    print("       STUDENT MANAGEMENT")
    print("=" * 50)

    print("1. Add Student")
    print("2. Show All Students")
    print("3. Find Student by ID")
    print("4. Find Student by Name")
    print("5. Update Student")
    print("6. Delete Student")
    print("7. Delete All Students")
    print("0. Exit")

    print("=" * 50)


# =========================================================
# MAIN
# =========================================================

def main():

    # Create database table
    create_table()

    while True:

        show_menu()

        choice = input("Enter your choice: ")

        if choice == "1":
            add_student()

        elif choice == "2":
            show_all_students()

        elif choice == "3":
            find_student()

        elif choice == "4":
            find_by_name()

        elif choice == "5":
            update_student()

        elif choice == "6":
            delete_student()

        elif choice == "7":
            delete_all_students()

        elif choice == "0":
            print()
            print("Goodbye!")
            break

        else:
            print("Invalid choice!")


# =========================================================
# PROGRAM START
# =========================================================

if __name__ == "__main__":
    main()
