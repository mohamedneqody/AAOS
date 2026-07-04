import psycopg2
conn = psycopg2.connect('postgresql://acb_user:acb_pass@postgres:5432/acb_db')
cur = conn.cursor()
cur.execute('SELECT * FROM workflow_entity;')
cols = [desc[0] for desc in cur.description]
rows = cur.fetchall()
for row in rows:
    print(f"--- Workflow: {row[1]} ---")
    for col, val in zip(cols, row):
        print(f"{col}: {val}")
