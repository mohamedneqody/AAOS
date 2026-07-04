SELECT id, "startedAt", "stoppedAt", status, data->'resultData'->'runData' as runData FROM execution_entity ORDER BY "startedAt" DESC LIMIT 1;
