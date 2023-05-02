from os import environ

from passlib import hash
from flask import request, jsonify
from functools import wraps
import jwt
from sqlalchemy.orm import sessionmaker, scoped_session
from ..db import engine
from ..models import User, Admin, Role

from environs import Env

env = Env()
env.read_env()

def hash_password(password: str) -> str:
    return hash.sha256_crypt.encrypt(password)


def is_password(password: str, hashed_password: str) -> bool:
    return hash.sha256_crypt.verify(password, hashed_password)


def user_token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        session = sessionmaker(bind=engine)()
        token = None

        if 'authorization' in request.headers:
            token = request.headers['authorization'].split('Bearer ')[1]

        try:
            if not token:
                raise Exception("token is invalid")

            data = jwt.decode(token, environ['JWT_SECRET_KEY'], algorithms=["HS256"])
            current_user =  session.query(User).filter(User.id == data['user_id']).first()

            if current_user is None: raise Exception()

            session.close()
        except Exception as err:
            session.close()
            response_data = {
                'error': True,
                'message': str(err)
            }
            return jsonify(response_data), 401 

        return f(current_user, *args, **kwargs)
    return decorator


def admin_token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        session = sessionmaker(bind=engine)()
        token = None

        if 'authorization' in request.headers:
            token = request.headers['authorization'].split('Bearer ')[1]

        try:
            if not token:
                raise Exception("token is invalid")

            data = jwt.decode(token, environ['JWT_SECRET_KEY'], algorithms=["HS256"])
            current_admin =  session.query(Admin).join(Role)\
                .filter(Admin.id == data['admin_id']).first()

            if current_admin is None: raise Exception()

            session.close()
        except Exception as err:
            session.close()
            response_data = {
                'error': True,
                'message': str(err)
            }
            return jsonify(response_data), 401
        
        return f(current_admin, *args, **kwargs)
    return decorator


def can(permission):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                session = sessionmaker(bind=engine)()
                current_admin: Admin = args[0]
                admin_role = session.query(Role).filter(Role.id == current_admin.role_id,
                                                        Role.deleted_at == None).first()
                permissions = eval(str(admin_role.permissions))
                
                if permission not in permissions:
                    raise Exception('forbidden')
                
                session.close()
            except Exception as err:
                session.close()
                response_data = {
                    'error': True,
                    'message': str(err)
                }
                return jsonify(response_data), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator
