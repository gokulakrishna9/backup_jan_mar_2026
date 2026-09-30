"""Check auth table structures."""
import mysql.connector
conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='password', database='job_portal')
cur = conn.cursor()

for table in ['user_role', 'auth_user', 'record_owner', 'query_group', 'query_group_member']:
    try:
        cur.execute(f"DESCRIBE {table}")
        print(f"\n=== {table} ===")
        for row in cur.fetchall():
            print(f"  {row[0]}: {row[1]} {'PK' if row[3]=='PRI' else ''}")
    except Exception as e:
        print(f"\n=== {table}: {e} ===")

# Check if there's any data
for table in ['user_role', 'auth_user']:
    cur.execute(f"SELECT COUNT(*) FROM {table}")
    count = cur.fetchone()[0]
    print(f"\n{table} rows: {count}")
    if count > 0 and count < 10:
        cur.execute(f"SELECT * FROM {table}")
        for row in cur.fetchall():
            print(f"  {row}")

conn.close()
