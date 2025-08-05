import sqlite3

# Connect to the database
conn = sqlite3.connect('library_db.sqlite3')
cursor = conn.cursor()

# Get the schema for the book table
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='book';")
schema = cursor.fetchone()

if schema:
    print("Book table schema:")
    print(schema[0])
else:
    print("Book table not found")

# Check if category column exists
cursor.execute("PRAGMA table_info(book);")
columns = cursor.fetchall()
print("\nBook table columns:")
for column in columns:
    print(f"- {column[1]} ({column[2]})")

conn.close()
