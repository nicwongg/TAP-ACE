import sqlite3

conn = sqlite3.connect('championsleague.db')

with open('schema.sql') as f:
    conn.executescript(f.read())

cur = conn.cursor()

conn.commit()
conn.close()
