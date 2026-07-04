import psycopg2

try:
    conn = psycopg2.connect(host="postgres", database="acb_db", user="acb_user", password="acb_pass")
    cur = conn.cursor()
    cur.execute("TRUNCATE TABLE tasks, task_states, event_queue, logs CASCADE;")
    conn.commit()
    print("Database cleared for testing.")
except Exception as e:
    print("Failed to clear db:", e)
