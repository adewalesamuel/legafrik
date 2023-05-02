import datetime

from sqlalchemy.orm import sessionmaker, scoped_session
from flask import request, jsonify
from marshmallow import ValidationError
from ..models import EtatDemande, Admin
from ..db import engine
from ..schemas import EtatDemandeSchema

from environs import Env

env = Env()
env.read_env()

session = scoped_session(sessionmaker(bind=engine), scopefunc=request)


def index(current_admin: Admin):
    etat_demandes = session.query(EtatDemande)\
        .filter(EtatDemande.deleted_at == None)\
        .order_by(EtatDemande.created_at.asc()).all()
    result = [row.toDict() for row in etat_demandes]
    response_data = {
        'success': True,
        'etat_demandes': result
    }

    session.close()

    return jsonify(response_data), 200


def store(current_admin: Admin):
    request_data = request.json
    etat_demandes_schema = EtatDemandeSchema()

    try:
        validated_data = etat_demandes_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        etat_demande = EtatDemande(
            libelle = validated_data.libelle,
        )

        session.add(etat_demande)
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
        'etat_demande': request_data
    }

    return jsonify(response_data), 200


def update(current_admin: Admin, id: int):
    request_data = request.json
    etat_demandes_schema = EtatDemandeSchema()

    try:
        validated_data = etat_demandes_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        etat_demande: EtatDemande = session.query(EtatDemande).get(id)

        etat_demande.libelle = validated_data.libelle

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
        'etat_demande': request_data
    }

    return jsonify(response_data), 200


def delete(current_admin: Admin, id: int):    
    try:
        etat_demande: EtatDemande = session.query(EtatDemande).get(id)

        etat_demande.deleted_at = datetime.datetime.utcnow()

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

