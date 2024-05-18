from datetime import datetime
from fastapi import HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Boolean, DateTime, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship, Session
from sqlalchemy.sql import func
from database import Base, Sessionlocal
from my_config import get_db


class TaskCreate(BaseModel):
    task_title: str
    task_status: str
    type_: str
    uuid: str
    name: str
    reward_type: str
    reward: int
    description: str
    platform: str
    last_completion: datetime
    is_completed: bool
    user_id: int
    task_url: str

    class Config:
        from_attributes = True


class Task(Base):
    __tablename__ = "task"
    task_id = Column(Integer, primary_key=True, autoincrement=True)
    task_title = Column(String(255))
    task_status = Column(String(255))
    type_ = Column(String(255))
    uuid = Column(String(255), unique=True)
    name = Column(String(255))
    reward_type = Column(String(255))
    reward = Column(Integer)
    description = Column(String(255))
    platform = Column(String(255))
    last_completion = Column(DateTime)
    is_completed = Column(Boolean)
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
                'task_title': task_.task_title,
                'task_status': task_.task_status,
                'type_': task_.type_,
                'uuid': task_.uuid,
                'name': task_.name,
                'reward_type': task_.reward_type,
                'reward': task_.reward,
                'description': task_.description,
                'platform': task_.platform,
                'last_completion': task_.last_completion,
                'is_completed': task_.is_completed,
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
