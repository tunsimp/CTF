import sqlite3

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS users''')
    # Create users table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    password TEXT,
                    email TEXT,
                    bio TEXT,
                    uid TEXT
                 )''')
    conn.commit()
    conn.close()


def insert_user(username, password, user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''INSERT INTO users (username, password, uid) 
                 VALUES (?, ?, ?)''', (username, password, user_id))
    conn.commit()
    conn.close()


def get_user(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM users WHERE username = ?''', (username,))
    user = c.fetchone()
    conn.close()
    return user


def get_user_id(uid):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM users WHERE uid = ?''', (uid,))
    user = c.fetchone()
    conn.close()
    return user


def update_user(username, email, bio):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''UPDATE users SET email = ?, bio = ? WHERE username = ?''', (email, bio, username))
    conn.commit()
    conn.close()
