import datetime

from sqlalchemy.orm import sessionmaker, scoped_session
from flask import request, jsonify
from marshmallow import ValidationError
from ..models import CategorieUser, Admin
from ..db import engine
from ..schemas import CategorieUserSchema

from environs import Env

env = Env()
env.read_env()

session = scoped_session(sessionmaker(bind=engine), scopefunc=request)


def index(current_admin: Admin):
    categorie_users = session.query(CategorieUser)\
        .filter(CategorieUser.deleted_at == None)\
        .order_by(CategorieUser.created_at.desc()).all()
    result = [row.toDict() for row in categorie_users]
    response_data = {
        'success': True,
        'categorie_users': result
    }

    session.close()

    return jsonify(response_data), 200


def store(current_admin: Admin):
    request_data = request.json
    categorie_users_schema = CategorieUserSchema()

    try:
        validated_data = categorie_users_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        categorie_user = CategorieUser(
            libelle = validated_data.libelle,
        )

        session.add(categorie_user)
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
        'success': True,
        'categorie_user': request_data
    }

    return jsonify(response_data), 200


def update(current_admin: Admin, id: int):
    request_data = request.json
    categorie_users_schema = CategorieUserSchema()

    try:
        validated_data = categorie_users_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        categorie_user: CategorieUser = session.query(CategorieUser).get(id)

        categorie_user.libelle = validated_data.libelle

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
        'success': True,
        'categorie_user': request_data
    }

    return jsonify(response_data), 200


def delete(current_admin: Admin, id: int):    
    try:
        categorie_user: CategorieUser = session.query(CategorieUser).get(id)

        categorie_user.deleted_at = datetime.datetime.utcnow()

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

