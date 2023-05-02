import datetime

from sqlalchemy.orm import sessionmaker, scoped_session
from flask import request, jsonify
from marshmallow import ValidationError
from ..models import MoyenPaiement, Admin
from ..db import engine
from ..schemas import MoyenPaiementSchema

from environs import Env

env = Env()
env.read_env()

session = scoped_session(sessionmaker(bind=engine), scopefunc=request)


def index(current_admin: Admin):
    is_private  = request.args.get('is_private')
    moyen_paiements = session.query(MoyenPaiement)\
        .filter(MoyenPaiement.deleted_at == None)\

    if (is_private is not None or is_private is True):
        moyen_paiements = moyen_paiements.filter(MoyenPaiement.is_private == is_private)
    else:
        moyen_paiements = moyen_paiements.filter(MoyenPaiement.is_private == None)

    moyen_paiements = moyen_paiements.order_by(MoyenPaiement.created_at.desc()).all()
    result = [row.toDict() for row in moyen_paiements]
    response_data = {
        'success': True,
        'moyen_paiements': result
    }

    session.close()

    return jsonify(response_data), 200


def store(current_admin: Admin):
    request_data = request.json
    moyen_paiements_schema = MoyenPaiementSchema()

    try:
        validated_data = moyen_paiements_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        moyen_paiement = MoyenPaiement(
            libelle = validated_data.libelle,
            is_private = validated_data.is_private
        )

        session.add(moyen_paiement)
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
        'moyen_paiement': request_data
    }

    return jsonify(response_data), 200


def update(current_admin: Admin, id: int):
    request_data = request.json
    moyen_paiements_schema = MoyenPaiementSchema()

    try:
        validated_data = moyen_paiements_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        moyen_paiement: MoyenPaiement = session.query(MoyenPaiement).get(id)

        moyen_paiement.libelle = validated_data.libelle
        moyen_paiement.is_private = validated_data.is_private

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
        'moyen_paiement': request_data
    }

    return jsonify(response_data), 200


def delete(current_admin: Admin, id: int):    
    try:
        moyen_paiement: MoyenPaiement = session.query(MoyenPaiement).get(id)

        moyen_paiement.deleted_at = datetime.datetime.utcnow()

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

