# from typing import Optional
# from pydantic import BaseModel
# from sqlalchemy import Column, String, Integer, Boolean, DateTime, TIMESTAMP, ForeignKey
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql import func
# from User_fast_api.database import Base
#
#
# class AccountCreate(BaseModel):
#     plateFormName: str
#     directUrl: str
#
#     class Config:
#         from_attributes = True
#
#
# class UpdateUser(BaseModel):
#     name: Optional[str] = None
#     email: Optional[str] = None
#     mobile: Optional[int] = None
#
#
# class SocialAccount(Base):
#     __tablename__ = "socialAccount"
#     account_id = Column(Integer, primary_key=True, autoincrement=True)
#     plateFormName = Column(String(255))
#     user_id = Column(Integer, ForeignKey('users.user_id'))
#     directUrl = Column(String(255))
#     is_deleted = Column(Boolean, server_default='0', nullable=False)
#     created_at = Column(DateTime, default=func.now())
#     updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
#     deleted_on = Column(DateTime)
#
#     account_creator = relationship("Users", backref="account_creator",
#                            uselist=False, primaryjoin="SocialAccount.user_id==Users.user_id")
