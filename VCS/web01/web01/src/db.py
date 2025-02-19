import sqlite3
import os
import hashlib


def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""DROP TABLE IF EXISTS users""")
    c.execute("""DROP TABLE IF EXISTS memes""")

    c.execute(
        """CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS memes (id TEXT PRIMARY KEY, title TEXT, filename TEXT)"""
    )

    c.execute(
        f"""Insert INTO users (username, password) VALUES ("admin", "{hashlib.md5(os.urandom(128).hex().encode()).hexdigest()}")"""
    )
    c.execute(
        """Insert INTO memes (id, title, filename) VALUES ("623da5cb-cb53-4621-9b22-910f3a612b15", "memememe", "exploits_of_a_mom.png")"""
    )
    conn.commit()
    conn.close()


def get_meme(id: str):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute(f'''SELECT filename FROM memes WHERE id="{id}"''')
    res = c.fetchone()
    conn.close()
    return res


def get_user(username: str):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute(f"""SELECT * FROM users WHERE username=("{username}")""")
    res = c.fetchone()
    conn.close()
    return res


def add_meme(title: str, filename: str, id):
    try:
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            f"""INSERT INTO memes (id, title, filename) VALUES ("{id}", "{title}", "{filename}")"""
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return str(e)
