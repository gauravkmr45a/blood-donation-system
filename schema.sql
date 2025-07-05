CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    blood_group TEXT,
    phone TEXT UNIQUE,
    email TEXT UNIQUE,
    city TEXT,
    role TEXT,
    password TEXT
);
