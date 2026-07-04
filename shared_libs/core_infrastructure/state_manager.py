import logging
from .db import get_connection, release_connection

logger = logging.getLogger("StateManager")

class StateManager:
    @staticmethod
    def transition(task_id: str, new_state: str, owner: str = None, correlation_id: str = None):
        """
        Transitions a task to a new state and updates history.
        """
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE task_states 
                    SET previous_state = current_state,
                        current_state = %s,
                        owner = COALESCE(%s, owner),
                        correlation_id = COALESCE(%s, correlation_id),
                        updated_at = NOW()
                    WHERE task_id = %s
                    RETURNING current_state;
                    """,
                    (new_state, owner, correlation_id, task_id)
                )
                res = cur.fetchone()
                
                # Also update the tasks table status
                cur.execute(
                    "UPDATE tasks SET status = %s, updated_at = NOW() WHERE id = %s",
                    (new_state, task_id)
                )
                
                conn.commit()
                logger.info(f"Task {task_id} transitioned to {new_state}")
                return res[0] if res else None
        except Exception as e:
            conn.rollback()
            logger.error(f"Failed to transition state for {task_id}: {e}")
            raise
        finally:
            release_connection(conn)
