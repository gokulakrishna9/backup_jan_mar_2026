"""Test the exact SQL that R2DBC generates."""
import mysql.connector
conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='password', database='job_portal')
cur = conn.cursor()

# Exact R2DBC query
cur.execute("SELECT education_level.* FROM education_level WHERE education_level.education_level_id = %s LIMIT 2", (4,))
rows = cur.fetchall()
print(f"R2DBC query result: {len(rows)} rows")
for r in rows:
    print(f"  {r}")

# Simple query
cur.execute("SELECT * FROM education_level")
rows = cur.fetchall()
print(f"\nAll rows: {len(rows)}")
for r in rows:
    print(f"  {r}")

# Check column names
cur.execute("DESCRIBE education_level")
print(f"\nColumns:")
for r in cur.fetchall():
    print(f"  {r[0]}: {r[1]}")

conn.close()
