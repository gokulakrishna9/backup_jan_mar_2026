"""Check what columns exist on user_profile and if record_owner table exists."""
import mysql.connector

conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='password', database='job_portal')
cur = conn.cursor()

# Check user_profile columns
cur.execute("DESCRIBE user_profile")
print("=== user_profile columns ===")
for row in cur.fetchall():
    print(f"  {row[0]}: {row[1]}")

# Check if record_owner exists
cur.execute("SHOW TABLES LIKE 'record_owner'")
result = cur.fetchall()
print(f"\n=== record_owner exists: {len(result) > 0} ===")
if result:
    cur.execute("DESCRIBE record_owner")
    for row in cur.fetchall():
        print(f"  {row[0]}: {row[1]}")

# Check if deleted_at column exists
cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='job_portal' AND TABLE_NAME='user_profile' AND COLUMN_NAME IN ('deleted_at', 'is_deleted')")
print(f"\n=== soft-delete column: {[r[0] for r in cur.fetchall()]} ===")

conn.close()
