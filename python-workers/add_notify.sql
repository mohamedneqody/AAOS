CREATE OR REPLACE FUNCTION notify_event_queue() RETURNS trigger AS $$
BEGIN
  PERFORM pg_notify('event_queue_channel', row_to_json(NEW)::text);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS event_queue_notify_trigger ON event_queue;
CREATE TRIGGER event_queue_notify_trigger
AFTER INSERT ON event_queue
FOR EACH ROW EXECUTE FUNCTION notify_event_queue();
