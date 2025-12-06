#!/usr/bin/env python
import sqlite3

conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()

# Check table schema first
cur.execute("PRAGMA table_info(core_user)")
columns = cur.fetchall()
print("Table columns:")
for col in columns:
    print(f"  {col[1]} ({col[2]})")

# Check existing users
cur.execute('SELECT username FROM core_user')
existing = cur.fetchall()
print(f"\nExisting users: {len(existing)}")
for user in existing:
    print(f"  - {user[0]}")

conn.close()
