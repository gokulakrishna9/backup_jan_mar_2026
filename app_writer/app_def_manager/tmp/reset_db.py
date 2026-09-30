"""Reset job_portal database and run all schemas."""
import mysql.connector

conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='password')
cur = conn.cursor()

# Drop and recreate
cur.execute('DROP DATABASE IF EXISTS job_portal')
cur.execute('CREATE DATABASE job_portal')
cur.execute('USE job_portal')
print("Database recreated")

# Run schema files
for schema_file in [
    'generated_application/job_portal/schema.sql',
    'generated_application/job_portal/webflux_app/auth-schema.sql',
    'generated_application/job_portal/webflux_app/activity-tracking-schema.sql',
]:
    with open(schema_file, 'r', encoding='utf-8') as f:
        sql = f.read()
    stmts = [s.strip() for s in sql.split(';') if s.strip()]
    count = 0
    for stmt in stmts:
        try:
            cur.execute(stmt)
            count += 1
        except Exception as e:
            print(f"  Warning: {e}")
    print(f"  {schema_file}: {count} statements")

conn.commit()
conn.close()
print("Done!")
