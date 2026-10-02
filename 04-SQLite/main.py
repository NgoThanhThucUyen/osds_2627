import sqlite3


# ==========================================
# 1. KẾT NỐI DATABASE
# ==========================================

conn = sqlite3.connect("school.db")

print("Connected to database successfully!")


# ==========================================
# 2. TẠO CURSOR
# ==========================================

cursor = conn.cursor()


# ==========================================
# 3. TẠO BẢNG STUDENT
# ==========================================

sql_create_table = """
CREATE TABLE IF NOT EXISTS Student (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    major TEXT
)
"""

cursor.execute(sql_create_table)

print("Student table created successfully!")


# ==========================================
# 4. THÊM DỮ LIỆU
# ==========================================

sql_insert = """
INSERT INTO Student (name, age, major)
VALUES (?, ?, ?)
"""

students = [
    ("Nguyen Van An", 20, "IT"),
    ("Tran Thi Binh", 21, "AI"),
    ("Le Van Cuong", 20, "SE"),
    ("Pham Thi Dung", 22, "DS"),
    ("Hoang Van Em", 21, "IT")
]

cursor.executemany(sql_insert, students)

print("Students inserted successfully!")


# ==========================================
# 5. LƯU THAY ĐỔI
# ==========================================

conn.commit()


# ==========================================
# 6. LẤY DỮ LIỆU
# ==========================================

sql_select = """
SELECT id, name, age, major
FROM Student
"""

cursor.execute(sql_select)

students = cursor.fetchall()


# ==========================================
# 7. HIỂN THỊ DỮ LIỆU
# ==========================================

print()
print("=" * 60)
print("STUDENT LIST")
print("=" * 60)

print(f"{'ID':<5}{'NAME':<25}{'AGE':<10}{'MAJOR':<10}")
print("-" * 60)

for student in students:
    id = student[0]
    name = student[1]
    age = student[2]
    major = student[3]

    print(f"{id:<5}{name:<25}{age:<10}{major:<10}")

print("=" * 60)


# ==========================================
# 8. ĐÓNG DATABASE
# ==========================================

conn.close()

print("Database connection closed.")
