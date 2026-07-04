import psycopg2

conn = psycopg2.connect('postgresql://acb_user:acb_pass@postgres:5432/acb_db')
cur = conn.cursor()

# Clear data
cur.execute("DELETE FROM execution_entity;")
cur.execute("DELETE FROM execution_data;")
cur.execute("DELETE FROM event_queue;")
cur.execute("DELETE FROM task_states;")
cur.execute("DELETE FROM tasks;")
cur.execute("DELETE FROM logs;")
conn.commit()

print("Database cleared for clean test.")
