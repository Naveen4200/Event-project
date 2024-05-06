from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Boolean, DateTime, TIMESTAMP, BIGINT, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base, Sessionlocal
from my_config import api_response, get_db


class TaskCreate(BaseModel):
    task_url: str
    taskTitle: str
    taskStatus: str
    type: str
    name: str
    rewardType: str
    reward: int
    description: str
    platform: str
    uuid: str
    lastCompletion: datetime
    isCompleted: bool

    class Config:
        from_attributes = True


class Task(Base):
    __tablename__ = "task"
    task_id = Column(Integer, primary_key=True, autoincrement=True)
    taskTitle = Column(String(255))
    taskStatus = Column(String(255))
    type = Column(String(255))
    name = Column(String(255))
    rewardType = Column(String(255))
    reward = Column(Integer)
    description = Column(String(255))
    platform = Column(String(255))
    lastCompletion = Column(DateTime)
    isCompleted = Column(Boolean)
    uuid = Column(String(25), ForeignKey('users.uuid'))
    task_url = Column(String(255))
    is_deleted = Column(Boolean, server_default='0', nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
    deleted_on = Column(DateTime)

    taskCreator = relationship("Users", backref="task_creator",
                               uselist=False, primaryjoin="Task.uuid==Users.uuid")

    # #######################################################################################################################

    @staticmethod
    def task_insert(data: dict, db: Sessionlocal):
        try:
            task_ = Task(**data)
            task_.created_at = datetime.now()
            db.add(task_)
            db.commit()
            return {
                'status': True,
                'data': None,
                'message': 'Task Created'
            }
        except Exception as e:
            db.rollback()
            return HTTPException(status_code=500, detail=str(e))

# #########################################################################################################

    @staticmethod
    def task_read(uuid: str = None, db: Sessionlocal = Depends(get_db)):
        try:
            base_query = db.query(Task).filter(Task.is_deleted == 0)
            if uuid is not None:
                base_query = base_query.filter(Task.uuid == uuid)
            task = base_query.all()

            return {
                'status': True,
                'data': task,
                'message': 'successful'
            }
        except Exception as e:
            return HTTPException(status_code=500, detail=f"Error: {str(e)}")
