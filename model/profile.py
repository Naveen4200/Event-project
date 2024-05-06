# from datetime import datetime, timedelta
# from typing import Optional
# import bcrypt
# import jwt
# from fastapi import HTTPException, Depends
# from pydantic import BaseModel
# from sqlalchemy import Column, String, Integer, Boolean, DateTime, TIMESTAMP, BIGINT, ForeignKey
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql import func
# from User_fast_api.auth.auth_handler import signJWT
# from User_fast_api.database import Base, Sessionlocal
# from User_fast_api.my_config import api_response, get_db
#
#
# class ProfileCreate(BaseModel):
#     user_id: int
#     userCoin: int
#     diamond: int
#     userSocialProfile_id: int
#
#     class Config:
#         from_attributes = True
#
#
# class UpdateProfile(BaseModel):
#     name: Optional[str] = None
#     email: Optional[str] = None
#     mobile: Optional[int] = None
#
#
# class Profile(Base):
#     __tablename__ = "profile"
#     profile_id = Column(Integer, primary_key=True, autoincrement=True)
#     # userName = Column(String(255), ForeignKey('users.name'))
#     # userMobNo = Column(BIGINT, ForeignKey('users.mobNumber'))
#     user_id = Column(Integer, ForeignKey('users.user_id'))
#     userCoin = Column(Integer)
#     diamond = Column(Integer)
#     # deviceInfo = Column(String(255), ForeignKey('users.deviceInfo'))
#     userSocialProfile_id = Column(Integer, ForeignKey('socialAccount.account_id'))
#     is_deleted = Column(Boolean, server_default='0', nullable=False)
#     created_at = Column(DateTime, default=func.now())
#     updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
#     deleted_on = Column(DateTime)
#
#     creator = relationship("Users", backref="profile_creator",
#                            uselist=False, primaryjoin="Profile.user_id==Users.user_id")
#     socialAccount = relationship("SocialAccount", backref="account_creator",
#                                  uselist=False, primaryjoin="Profile.userSocialProfile_id==SocialAccount.account_id")
#
#     # #######################################################################################################################
#
#     @staticmethod
#     def profile_insert(data: dict, db: Sessionlocal):
#         try:
#             profile = Profile(**data)
#             profile.created_at = datetime.now()
#             db.add(profile)
#             db.commit()
#             response = api_response(200, message="profile Created successfully")
#             return response
#         except Exception as e:
#             db.rollback()
#             return HTTPException(status_code=500, detail=str(e))
#
#     # #######################################################################################################################
#
#     # @staticmethod
#     # def update_user(user_data: UpdateUser, user_id: int, db: Sessionlocal):
#     #     try:
#     #         db_user = db.query(Users).filter(Users.user_id == user_id, Users.is_deleted == 0).first()
#     #         if db_user is None:
#     #             return HTTPException(status_code=404, detail="Record not found")
#     #
#     #         if db.query(Users).filter(Users.email == user_data.email).first():
#     #             return HTTPException(status_code=400, detail="User email already exists")
#     #
#     #         if (not str(user_data.mobile).isdigit()) or (len(str(user_data.mobile)) != 10):
#     #             return HTTPException(status_code=400, detail="Invalid mobile number")
#     #
#     #         hero_data = user_data.model_dump(exclude_unset=True)
#     #         for key, value in hero_data.items():
#     #             setattr(db_user, key, value)
#     #             db.add(db_user)
#     #         db.commit()
#     #         response = api_response(200, message="User Data updated successfully")
#     #         return response
#     #     except Exception as e:
#     #         return HTTPException(status_code=500, detail=str(e))
#     #
#     # ########################################################################################################################
#
#     @staticmethod
#     def get_profile(profile_id: int = None, db: Sessionlocal = Depends(get_db)):
#         try:
#             base_query = db.query(Profile).filter(Profile.is_deleted == 0)
#             if profile_id:
#                 base_query = base_query.filter(Profile.profile_id == profile_id)
#
#             response = api_response(data=users_records, count=len(users_records), total=total_users,
#                                         status_code=200)
#
#                 return response
#             return HTTPException(status_code=404, detail="No data found")
#         except Exception as e:
#             return HTTPException(status_code=500, detail=f"Error: {str(e)}")
#
#     # ------------------------------------------------------------------------------------------------------------------------------
#     # @staticmethod
#     # def user_delete(user_id: int, db: Sessionlocal):
#     #     try:
#     #         usr = db.query(Users).filter(Users.user_id == user_id,
#     #                                      Users.is_deleted == 0).first()
#     #         if usr is None:
#     #             return HTTPException(status_code=404, detail=f"Record with id {user_id} not found")
#     #
#     #         usr.is_deleted = True
#     #         usr.deleted_on = datetime.now()
#     #
#     #         db.commit()
#     #         response = api_response(200, message="User Data deleted successfully")
#     #         return response
#     #     except Exception as e:
#     #         db.rollback()
#     #         return HTTPException(status_code=500, detail=str(e))
#     #
#     # # ###############################################################################################################
#     #
#     # @staticmethod
#     # def login(credential: LoginInput):
#     #     try:
#     #         session = Sessionlocal()
#     #         user = session.query(Users).filter(Users.mobNumber == credential.mobNumber,
#     #                                            Users.is_deleted == 0).filter().first()
#     #         if not user:
#     #             return HTTPException(status_code=404, detail="Invalid mobile number or password")
#     #
#     #         if bcrypt.checkpw(credential.password.encode('utf-8'), user.password.encode('utf-8')):
#     #             token, exp = signJWT(user.user_id)
#     #             response = {
#     #                 'token': token,
#     #                 'exp': exp,
#     #                 "user_id": user.user_id,
#     #                 "user_name": user.name,
#     #                 'mobNumber': user.mobNumber,
#     #                 "created_at": user.created_at,
#     #                 'updated_at': user.updated_at
#     #             }
#     #
#     #             return response
#     #         else:
#     #             return HTTPException(status_code=401, detail='Invalid email or password')
#     #
#     #     except Exception as e:
#     #         return HTTPException(status_code=500, detail=f"Error: {str(e)}")
#     #
#     # ###################################################################################################################
#     #
#     # @staticmethod
#     # def change_password(credential: ChangePassword, user_id: int, db: Sessionlocal):
#     #     try:
#     #         user = db.query(Users).filter(Users.user_id == user_id, Users.is_deleted == 0).first()
#     #
#     #         if not user:
#     #             return HTTPException(status_code=404, detail="user not found")
#     #
#     #         if bcrypt.checkpw(credential.current_password.encode('utf-8'), user.password.encode('utf-8')) is not True:
#     #             return {"message": "wrong password"}
#     #
#     #         if bcrypt.checkpw(credential.current_password.encode('utf-8'), user.password.encode('utf-8')):
#     #             hashed_new_password = bcrypt.hashpw(credential.new_password.encode('utf-8'), bcrypt.gensalt())
#     #
#     #             user.password = hashed_new_password
#     #             db.commit()
#     #
#     #         response = api_response(200, message="Password changed successfully")
#     #         return response
#     #
#     #     except Exception as e:
#     #         return HTTPException(status_code=500, detail=f"Error: {str(e)}")
