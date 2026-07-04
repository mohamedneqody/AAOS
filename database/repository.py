from sqlalchemy.orm import Session
from .models import Task, TaskState, Cost

class Repository:
    def __init__(self, session: Session):
        self.session = session
        
    def add_task(self, task: Task):
        self.session.add(task)
        self.session.commit()
        
    def get_task(self, task_id: str) -> Task:
        return self.session.query(Task).filter(Task.id == task_id).first()
