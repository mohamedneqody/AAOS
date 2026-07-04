import json
import logging
from .db import get_connection, release_connection
import psycopg2.extras

logger = logging.getLogger("QueueDispatcher")

class QueueDispatcher:
    
    @staticmethod
    def publish(queue_name: str, payload: dict):
        """
        Publishes a message to the specified queue.
        """
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO event_queue (queue_name, payload, status) VALUES (%s, %s, 'QUEUED') RETURNING id;",
                    (queue_name, json.dumps(payload))
                )
                event_id = cur.fetchone()[0]
                conn.commit()
                logger.info(f"Published event {event_id} to queue {queue_name}")
                return event_id
        except Exception as e:
            conn.rollback()
            logger.error(f"Failed to publish to {queue_name}: {e}")
            raise
        finally:
            release_connection(conn)

    @staticmethod
    def consume(queue_name: str, lock_id: str):
        """
        Fetches a single message from the queue using SKIP LOCKED.
        """
        conn = get_connection()
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(
                    """
                    UPDATE event_queue
                    SET status = 'RUNNING', locked_by = %s, locked_at = NOW()
                    WHERE id = (
                        SELECT id FROM event_queue
                        WHERE queue_name = %s AND status = 'QUEUED'
                        ORDER BY created_at ASC
                        FOR UPDATE SKIP LOCKED
                        LIMIT 1
                    )
                    RETURNING id, payload;
                    """,
                    (lock_id, queue_name)
                )
                row = cur.fetchone()
                conn.commit()
                if row:
                    return {"id": row['id'], "payload": row['payload']}
                return None
        except Exception as e:
            conn.rollback()
            logger.error(f"Error consuming from {queue_name}: {e}")
            raise
        finally:
            release_connection(conn)

    @staticmethod
    def complete(event_id: str, success: bool, max_retries: int = 3):
        """
        Marks an event as COMPLETED or sends to DLQ if max retries exceeded.
        """
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                if success:
                    cur.execute("UPDATE event_queue SET status = 'COMPLETED' WHERE id = %s", (event_id,))
                else:
                    cur.execute("UPDATE event_queue SET status = 'FAILED' WHERE id = %s RETURNING payload, queue_name", (event_id,))
                    row = cur.fetchone()
                    if row:
                        payload, original_queue = row[0], row[1]
                        cur.execute(
                            "INSERT INTO event_queue (queue_name, payload, status) VALUES (%s, %s, 'QUEUED')",
                            ("q_dead_letter", json.dumps({"original_queue": original_queue, "payload": payload}))
                        )
                conn.commit()
        finally:
            release_connection(conn)
