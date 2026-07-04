import time
import logging
import os
import threading
from sqlalchemy import create_engine, Column, String, JSON, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import OperationalError
import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PythonWorker")

Base = declarative_base()

class EventQueue(Base):
    __tablename__ = 'event_queue'
    id = Column(String, primary_key=True)
    queue_name = Column(String)
    payload = Column(JSON)
    status = Column(String)

from shared_libs.core.config import ConfigService

def get_db_url():
    return ConfigService.get_db_url()

def init_db():
    engine = create_engine(get_db_url())
    retries = 10
    while retries > 0:
        try:
            with engine.connect() as conn:
                logger.info("Successfully connected to PostgreSQL")
            Base.metadata.create_all(engine)
            from database.models import Base as DBBase
            DBBase.metadata.create_all(engine)
            return sessionmaker(bind=engine)()
        except OperationalError:
            retries -= 1
            time.sleep(3)
    raise Exception("Could not connect to PostgreSQL")

def passive_worker_loop():
    logger.info("Starting Python Worker initialization...")
    session = init_db()
    logger.info("Listening to PostgreSQL event_queue...")
    while True:
        try:
            time.sleep(2)
        except Exception as e:
            logger.error(f"Error in worker loop: {e}")
            time.sleep(5)

try:
    from fastapi import FastAPI
    from api_planning import router as planning_router
    from api_execution import router as execution_router
    from api_intelligence import router as intelligence_router
    from api_decision import router as decision_router
    from api_publishing import router as publishing_router
    from api_auth import router as auth_router
    from api_health import router as health_router
    
    app = FastAPI(title="AAOS API", description="Lead Backend APIs for AAOS Runtimes")
    app.include_router(planning_router)
    app.include_router(execution_router)
    app.include_router(intelligence_router)
    app.include_router(decision_router)
    app.include_router(publishing_router)
    app.include_router(auth_router)
    app.include_router(health_router)
except ImportError as e:
    logger.warning(f"FastAPI dependencies missing: {e}")
    app = None

if __name__ == '__main__':
    worker_thread = threading.Thread(target=passive_worker_loop, daemon=True)
    worker_thread.start()
    
    if app:
        import uvicorn
        logger.info("Starting FastAPI server on port 8000")
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        while True:
            time.sleep(10)
