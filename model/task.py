from datetime import datetime
from fastapi import HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Boolean, DateTime, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship, Session
from sqlalchemy.sql import func
from database import Base, Sessionlocal
from my_config import get_db


class TaskCreate(BaseModel):
    taskTitle: str
    taskStatus: str
    type: str
    uuid: str
    name: str
    rewardType: str
    reward: int
    description: str
    platform: str
    lastCompletion: datetime
    isCompleted: bool
    user_id: int
    task_url: str

    class Config:
        from_attributes = True


class Task(Base):
    __tablename__ = "task"
    task_id = Column(Integer, primary_key=True, autoincrement=True)
    taskTitle = Column(String(255))
    taskStatus = Column(String(255))
    type = Column(String(255))
    uuid = Column(String(255), unique=True)
    name = Column(String(255))
    rewardType = Column(String(255))
    reward = Column(Integer)
    description = Column(String(255))
    platform = Column(String(255))
    lastCompletion = Column(DateTime)
    isCompleted = Column(Boolean)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    task_url = Column(String(255))
    is_deleted = Column(Boolean, server_default='0', nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
    deleted_on = Column(DateTime)

    task_creator = relationship("Users", backref="task_creator",
                                uselist=False, primaryjoin="Task.user_id==Users.user_id")

    @staticmethod
    def task_insert(data: dict, db: Session):
        try:
            task_ = Task(**data)
            task_.created_at = datetime.now()
            db.add(task_)
            db.commit()
            db.refresh(task_)

            response = {
                'task_id': task_.task_id,
                'taskTitle': task_.taskTitle,
                'taskStatus': task_.taskStatus,
                'type_': task_.type,
                'uuid': task_.uuid,
                'name': task_.name,
                'rewardType': task_.rewardType,
                'reward': task_.reward,
                'description': task_.description,
                'platform': task_.platform,
                'lastCompletion': task_.lastCompletion,
                'isCompleted': task_.isCompleted,
                'user_id': task_.user_id,
                'task_url': task_.task_url,
                'is_deleted': task_.is_deleted,
                'created_at': task_.created_at,
                'updated_at': task_.updated_at,
                'deleted_on': task_.deleted_on,
            }
            return {
                'status': True,
                'data': response,
                'message': 'Successful'
            }
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

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
