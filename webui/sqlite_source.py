import sqlite3

conn = sqlite3.connect('datameta.db')

cur = conn.cursor()
cur.execute(
    """
    CREATE TABLE COMPANY
       (ID INT PRIMARY KEY     NOT NULL,
       NAME           TEXT    NOT NULL,
       AGE            INT     NOT NULL,
       ADDRESS        CHAR(50),
       SALARY         REAL);
    """
)
