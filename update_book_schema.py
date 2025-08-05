import sqlite3

# Connect to the database
conn = sqlite3.connect('library_db.sqlite3')
cursor = conn.cursor()

# Add columns to the book table
try:
    cursor.execute("ALTER TABLE book ADD COLUMN category VARCHAR(100)")
    print("Added category column")
except sqlite3.OperationalError as e:
    print(f"Category column: {e}")

try:
    cursor.execute("ALTER TABLE book ADD COLUMN total_quantity INTEGER DEFAULT 1")
    print("Added total_quantity column")
except sqlite3.OperationalError as e:
    print(f"total_quantity column: {e}")

try:
    cursor.execute("ALTER TABLE book ADD COLUMN available_quantity INTEGER DEFAULT 1")
    print("Added available_quantity column")
except sqlite3.OperationalError as e:
    print(f"available_quantity column: {e}")

try:
    cursor.execute("ALTER TABLE book ADD COLUMN description TEXT")
    print("Added description column")
except sqlite3.OperationalError as e:
    print(f"description column: {e}")

# Commit changes and close connection
conn.commit()
conn.close()

print("Database schema update completed")
