from os import environ
import datetime

from sqlalchemy.orm import sessionmaker, scoped_session
from flask import request, jsonify
from marshmallow import ValidationError
import jwt
from ..models import Admin, Role
from ..db import engine
from ..schemas import AdminSchema, LoginSchema, UpdateAdminSchema, \
    UpdatePasswordSchema
from ..utils import auth

from environs import Env

env = Env()
env.read_env()

session = scoped_session(sessionmaker(bind=engine), scopefunc=request)

def index(current_admin: Admin):
    pays_id  = request.args.get('pays_id')
    admins = session.query(Admin).join(Role)

    if (pays_id is not None):
        admins = admins.filter(Admin.pays_id == pays_id)

    admins = admins.filter(Admin.deleted_at == None)\
        .order_by(Admin.created_at.desc()).all()
    result = list()

    for admin in admins:
        role_dict = admin.role.toDict()
        admin_dict = admin.toDict()

        admin_dict['role'] = role_dict

        result.append(admin_dict)
    
    response_data = {
        'success': True,
        'admins': result
    }

    session.close()

    return jsonify(response_data), 200


def store(current_admin: Admin):
    request_data = request.json
    admin_schema = AdminSchema()

    try:
        validated_data = admin_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400

    try:        
        user = Admin(
            username = validated_data.username,
            email = validated_data.email,
            password = auth.hash_password(validated_data.password),
            profile_url = validated_data.profile_url,
            role_id = validated_data.role_id,
            pays_id = validated_data.pays_id
        )

        session.add(user)
        session.commit()
    except Exception as e:
        session.rollback()
        session.close()

        response_data = {
            'error': True,
            'message': str(e)
        }

        return jsonify(response_data), 500
    finally:
        session.close()

    response_data = {
        'success': True,
        'admin': request_data
    }

    return jsonify(response_data), 200


def update(current_admin: Admin, id: int):
    request_data = request.json
    admin_schema = UpdateAdminSchema()

    try:
        validated_data = admin_schema.load(request_data)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        admin: Admin = session.query(Admin).get(id)

        admin.username = validated_data['username']
        admin.email = validated_data['email']
        admin.profile_url = validated_data['profile_url']
        admin.role_id = validated_data['role_id']
        admin.pays_id = validated_data['pays_id']

        session.commit()
    except Exception as err:
        session.rollback()
        session.close()

        response_data = {
            'error': True,
            'message': err.messages
        }

        return jsonify(response_data), 500
    finally:
        session.close()
    
    response_data = {
        'success': True,
        'admin': request_data
    }

    return jsonify(response_data), 200


def delete(current_admin: Admin, id: int):    
    try:
        admin: Admin = session.query(Admin).get(id)
        admin.deleted_at = datetime.datetime.utcnow()

        session.commit()
    except Exception as err:
        session.rollback()
        session.close()

        response_data = {
            'error': True,
            'message': str(err)
        }

        return jsonify(response_data), 500
    finally:
        session.close()
    
    response_data = {
        'success': True
    }

    return jsonify(response_data), 200


def login():
    request_data = request.json
    login_schema = LoginSchema()
    token = ''

    try:
        validated_data = login_schema.load(request_data)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400

    try:        
        admin = session.query(Admin).filter(
            Admin.email == validated_data['email']).first()

        if (admin is None):
            raise Exception("email or password incorrect")

        if (auth.is_password(validated_data['password'], admin.password) is False):  
            raise Exception("email or password incorrect")   

        token = jwt.encode(
            {'admin_id' : admin.id, 
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=3)}, 
            environ['JWT_SECRET_KEY'], "HS256")   

    except Exception as e:
        session.close()
        response_data = {
            'error': True,
            'message': str(e)
        }

        return jsonify(response_data), 500
    finally:
        session.close()

    response_data = {
        'success': True,
        'admin': admin.toDict(),
        'token': token
    }

    return jsonify(response_data), 200


def logout():
    pass


def current_admin(current_admin: Admin):
    session.close()
    return jsonify({
        "success": True,
        "admin": current_admin.toDict()
    })


def update_profile(current_admin: Admin):
    request_data = request.json
    admin_schema = UpdateAdminSchema()

    try:
        validated_data = admin_schema.load(request_data)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        admin: Admin = session.query(Admin).get(current_admin.id)

        admin.username = validated_data['username']
        admin.email = validated_data['email']
        admin.profile_url = validated_data['profile_url']
        admin.pays_id = validated_data['pays_id']
        admin.role_id = validated_data['role_id']

        session.commit()
    except ValidationError as err:
        session.rollback()

        response_data = {
            'error': True,
            'message': err.messages
        }

        return jsonify(response_data), 500
    finally:
        session.close()
    
    response_data = {
        'success': True,
        'admin': request_data
    }

    return jsonify(response_data), 200


def update_password(current_admin: Admin):
    request_data = request.json
    admin_schema = UpdatePasswordSchema()

    try:
        validated_data = admin_schema.load(request_data)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        user: Admin = session.query(Admin).get(current_admin.id)
        
        user.password = auth.hash_password(validated_data['password'])

        session.commit()
    except ValidationError as err:
        session.rollback()

        response_data = {
            'error': True,
            'message': err.messages
        }

        return jsonify(response_data), 500
    finally:
        session.close()
    
    response_data = {
        'success': True,
        'admin': request_data
    }

    return jsonify(response_data), 200


def init_password(current_admin: Admin):
    request_data = request.json
    admin_schema = UpdatePasswordSchema()

    try:
        validated_data = admin_schema.load(request_data)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        user: Admin = session.query(Admin).get(current_admin.id)
        
        user.password = auth.hash_password(validated_data['password'])

        session.commit()
    except ValidationError as err:
        session.rollback()

        response_data = {
            'error': True,
            'message': err.messages
        }

        return jsonify(response_data), 500
    finally:
        session.close()
    
    response_data = {
        'success': True,
        'admin': request_data
    }

    return jsonify(response_data), 200