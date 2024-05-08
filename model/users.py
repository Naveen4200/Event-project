from datetime import datetime
from typing import Optional
import bcrypt
from fastapi import HTTPException, Request
from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Boolean, DateTime, TIMESTAMP, BIGINT
from sqlalchemy.sql import func
from auth.auth_handler import signJWT
from database import Base, Sessionlocal


class LoginInput(BaseModel):
    mobNumber: int
    password: str
    fcm_token: Optional['str']


class UserCreate(BaseModel):
    name: str
    uuid: str
    password: str
    fcmToken: str
    deviceInfo: str
    country: str
    mobNumber: int
    type: Optional['str']
    code: Optional['str']

    class Config:
        from_attributes = True


class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    uuid = Column(String(25), unique=True)
    password = Column(String(255))
    fcmToken = Column(String(255))
    deviceInfo = Column(String(255))
    ip = Column(String(255))
    ip_created_at = Column(DateTime, default=func.now())
    country = Column(String(25))
    type = Column(String(255))
    code = Column(String(255))
    mobNumber = Column(BIGINT, unique=True)
    is_deleted = Column(Boolean, server_default='0', nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
    deleted_on = Column(DateTime)

    # #######################################################################################################################

    @staticmethod
    def register(data: dict, request: Request, db: Sessionlocal):
        try:
            usr = Users(**data)
            usr.ip = request.client.host
            usr.created_at = datetime.now()
            usr.password = bcrypt.hashpw(usr.password.encode('utf-8'), bcrypt.gensalt())
            if db.query(Users).filter(Users.mobNumber == usr.mobNumber).first():
                return HTTPException(status_code=400, detail="User already exists")

            if (not str(usr.mobNumber).isdigit()) or (len(str(usr.mobNumber)) != 10):
                return HTTPException(status_code=400, detail="Invalid mobile number")
            db.add(usr)
            db.commit()

            response_data = {
                'name': usr.name,
                'password': usr.password,
                'fcmToken': usr.fcmToken,
                'deviceInfo': usr.deviceInfo,
                'country': usr.country,
                'code': usr.code,
                "user_id": usr.user_id,
                "user_name": usr.name,
                'mobNumber': usr.mobNumber,
                'uuid': usr.uuid,
                'ip': usr.ip,
                'type': usr.type,
                "created_at": usr.created_at,
                'updated_at': usr.updated_at
            }

            return response_data
        except Exception as e:
            db.rollback()
            return HTTPException(status_code=500, detail=str(e))

    # ###############################################################################################################

    @staticmethod
    def is_registered(mob_no: int):
        try:
            session = Sessionlocal()
            user = session.query(Users).filter(Users.mobNumber == mob_no, Users.is_deleted == 0).first()

            if (not str(mob_no).isdigit()) or (len(str(mob_no)) != 10):
                return {'status': False, 'data': None, 'message': 'Invalid mobile number'}

            if not user:
                return {'status': False, 'data': None, 'message': 'User not registered'}

            return {'status': True, 'data': None, 'message': 'user is already registered'}

        except Exception as e:
            # You might want to log the error instead of returning it directly
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    @staticmethod
    def login(request: Request, credential: LoginInput):
        try:
            session = Sessionlocal()
            user = session.query(Users).filter(Users.mobNumber == credential.mobNumber,
                                               Users.is_deleted == 0).filter().first()

            if not user:
                return HTTPException(status_code=404, detail="Invalid mobile number or password")

            if bcrypt.checkpw(credential.password.encode('utf-8'), user.password.encode('utf-8')):
                token, exp = signJWT(user.user_id)
                user.fcmToken = credential.fcm_token
                today = datetime.now().date()
                diff = today - user.ip_created_at.date()
                if diff.days > 30:
                    user.ip = None
                    user.ip_created_at = None
                client_ip = request.client.host
                max_ip_count = 4
                user_ip_list = user.ip.split(',') if user.ip else []
                user.ip_created_at = datetime.now()
                # Check if the IP address is already present
                if client_ip not in user_ip_list:
                    # Append the new IP address only if it's not already present
                    user_ip_list.append(client_ip)

                # Ensure that the number of IP addresses does not exceed the limit
                if len(user_ip_list) > max_ip_count:
                    # If the number exceeds the limit, remove the oldest IP addresses
                    return {
                        'status': True,
                        'data': 'login limit exceeded',
                        'message': 'successful'
                    }

                user.ip = ','.join(user_ip_list)
                session.commit()
                response = {
                    'token': token,
                    'exp': exp,
                    'name': user.name,
                    'password': user.password,
                    'fcmToken': user.fcmToken,
                    'deviceInfo': user.deviceInfo,
                    'country': user.country,
                    'code': user.code,
                    "user_id": user.user_id,
                    "user_name": user.name,
                    'mobNumber': user.mobNumber,
                    'uuid': user.uuid,
                    'ip': user.ip,
                    'type': user.type,
                    "created_at": user.created_at,
                    "ip_created_at": user.ip_created_at,
                    'updated_at': user.updated_at
                }

                return response
            else:
                return HTTPException(status_code=401, detail='Invalid mobile number or password')

        except Exception as e:
            return HTTPException(status_code=500, detail=f"Error: {str(e)}")
