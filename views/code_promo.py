import datetime

from sqlalchemy.orm import sessionmaker, scoped_session
from flask import request, jsonify
from marshmallow import ValidationError
from ..models import CodePromo, Admin
from ..db import engine
from ..schemas import CodePromoSchema

from environs import Env

env = Env()
env.read_env()

session = scoped_session(sessionmaker(bind=engine), scopefunc=request)


def index(current_admin: Admin):
    code_promos = session.query(CodePromo)\
        .filter(CodePromo.deleted_at == None)\
        .order_by(CodePromo.created_at.desc()).all()
    result = [row.toDict() for row in code_promos]
    response_data = {
        'success': True,
        'code_promos': result
    }

    session.close()

    return jsonify(response_data), 200


def store(current_admin: Admin):
    request_data = request.json
    code_promos_schema = CodePromoSchema()

    try:
        validated_data = code_promos_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        code_promo = CodePromo(
            code = validated_data.code,
            pourcentage = validated_data.pourcentage,
        )

        session.add(code_promo)
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
        'code_promo': request_data
    }

    return jsonify(response_data), 200


def update(current_admin: Admin, id: int):
    request_data = request.json
    code_promos_schema = CodePromoSchema()

    try:
        validated_data = code_promos_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        code_promo: CodePromo = session.query(CodePromo).get(id)

        code_promo.code = validated_data.code
        code_promo.pourcentage = validated_data.pourcentage

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
        'code_promo': request_data
    }

    return jsonify(response_data), 200


def delete(current_admin: Admin, id: int):    
    try:
        code_promo: CodePromo = session.query(CodePromo).get(id)

        code_promo.deleted_at = datetime.datetime.utcnow()

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

