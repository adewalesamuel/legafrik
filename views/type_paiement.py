import datetime

from sqlalchemy.orm import sessionmaker, scoped_session
from flask import request, jsonify
from marshmallow import ValidationError
from ..models import TypePaiement, Admin
from ..db import engine
from ..schemas import TypePaiementSchema

from environs import Env

env = Env()
env.read_env()

session = scoped_session(sessionmaker(bind=engine), scopefunc=request)


def index(current_admin: Admin):
    type_paiements = session.query(TypePaiement)\
        .filter(TypePaiement.deleted_at == None)\
        .order_by(TypePaiement.created_at.desc()).all()
    result = [row.toDict() for row in type_paiements]
    response_data = {
        'success': True,
        'type_paiements': result
    }

    session.close()

    return jsonify(response_data), 200


def store(current_admin: Admin):
    request_data = request.json
    type_paiements_schema = TypePaiementSchema()

    try:
        validated_data = type_paiements_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        type_paiement = TypePaiement(
            libelle = validated_data.libelle,
        )

        session.add(type_paiement)
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
        'type_paiement': request_data
    }

    return jsonify(response_data), 200


def update(current_admin: Admin, id: int):
    request_data = request.json
    type_paiements_schema = TypePaiementSchema()

    try:
        validated_data = type_paiements_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        type_paiement: TypePaiement = session.query(TypePaiement).get(id)

        type_paiement.libelle = validated_data.libelle

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
        'type_paiement': request_data
    }

    return jsonify(response_data), 200


def delete(current_admin: Admin, id: int):    
    try:
        type_paiement: TypePaiement = session.query(TypePaiement).get(id)

        type_paiement.deleted_at = datetime.datetime.utcnow()

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

