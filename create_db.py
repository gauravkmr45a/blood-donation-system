import sqlite3

con = sqlite3.connect('users.db')
cur = con.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    age INTEGER,
    gender TEXT,
    blood_group TEXT,
    phone TEXT,
    email TEXT,
    city TEXT,
    role TEXT,
    password TEXT
)
''')

con.commit()
con.close()
