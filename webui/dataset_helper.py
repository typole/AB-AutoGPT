import sqlite3

# c.execute("""
# CREATE TABLE students (
#             name TEXT,
#             age INTEGER,
#             height REAL)
# """)


if __name__ == '__main__':
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    all_students = [
        ('john', 21, 1.8),
        ('david', 35, 1.7),
        ('michael', 19, 1.83),
    ]
    c.executemany("INSERT INTO students VALUES (?, ?, ?)", all_students)
    c.execute("SELECT * FROM students")
    print(c.fetchall())
    conn.commit()
    conn.close()
