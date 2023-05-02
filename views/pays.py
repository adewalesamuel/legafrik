import datetime

from sqlalchemy.orm import sessionmaker, scoped_session
from flask import request, jsonify
from marshmallow import ValidationError
from ..models import Pays, Admin, TypeDemande
from ..db import engine
from ..schemas import PaysSchema

from environs import Env

env = Env()
env.read_env()

session = scoped_session(sessionmaker(bind=engine), scopefunc=request)


def index(current_admin: Admin):
    pays = session.query(Pays)\
        .filter(Pays.deleted_at == None)\
        .order_by(Pays.created_at.desc()).all()
    result = [row.toDict() for row in pays]
    response_data = {
        'success': True,
        'pays': result
    }

    session.close()

    return jsonify(response_data), 200


def get_type_demandes(id: int):
    type_demandes = session.query(TypeDemande)\
        .filter(TypeDemande.pays_id == id, TypeDemande.deleted_at == None)\
        .order_by(TypeDemande.created_at.desc()).all()
    result = [row.toDict() for row in type_demandes]
    response_data = {
        'success': True,
        'type_demandes': result
    }

    session.close()

    return jsonify(response_data), 200


def store(current_admin: Admin):
    request_data = request.json
    payss_schema = PaysSchema()

    try:
        validated_data = payss_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        pays = Pays(
            libelle = validated_data.libelle,
            code = validated_data.code,
            monnaie = validated_data.monnaie,
        )

        session.add(pays)
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
        'pays': request_data
    }

    return jsonify(response_data), 200


def update(current_admin: Admin, id: int):
    request_data = request.json
    payss_schema = PaysSchema()

    try:
        validated_data = payss_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        pays: Pays = session.query(Pays).get(id)

        pays.libelle = validated_data.libelle
        pays.code = validated_data.code
        pays.monnaie = validated_data.monnaie

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
        'pays': request_data
    }

    return jsonify(response_data), 200


def delete(current_admin: Admin, id: int):    
    try:
        pays: Pays = session.query(Pays).get(id)

        pays.deleted_at = datetime.datetime.utcnow()

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

