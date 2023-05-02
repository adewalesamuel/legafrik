import datetime

from sqlalchemy.orm import sessionmaker, scoped_session
from flask import request, jsonify
from marshmallow import ValidationError
from ..models import EtatEtapeTraitement, EtapeTraitement, Admin
from ..db import engine
from ..schemas import EtatEtapeTraitementSchema
from ..utils import mail, status_response

from environs import Env

env = Env()
env.read_env()

session = scoped_session(sessionmaker(bind=engine), scopefunc=request)


def index(current_admin: Admin):
    etat_etape_traitements = session.query(EtatEtapeTraitement)\
        .filter(EtatEtapeTraitement.deleted_at == None)\
        .order_by(EtatEtapeTraitement.created_at.desc()).all()
    result = [row.toDict() for row in etat_etape_traitements]
    response_data = {
        'success': True,
        'etat_etape_traitements': result
    }

    session.close()

    return jsonify(response_data), 200


def store(current_admin: Admin):
    request_data = request.json
    etat_etape_traitements_schema = EtatEtapeTraitementSchema()

    try:
        validated_data = etat_etape_traitements_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    try:
        etat_etape_traitement = EtatEtapeTraitement(
            libelle = validated_data.libelle,
            etape_traitement_id = validated_data.etape_traitement_id,
            is_default = validated_data.is_default
        )

        session.add(etat_etape_traitement)
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
        'etat_etape_traitement': request_data
    }

    return jsonify(response_data), 200


def update(current_admin: Admin, id: int):
    request_data = request.json
    etat_etape_traitements_schema = EtatEtapeTraitementSchema()

    try:
        validated_data = etat_etape_traitements_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        etat_etape_traitement: EtatEtapeTraitement = session.query(EtatEtapeTraitement).get(id)

        etat_etape_traitement.libelle = validated_data.libelle
        etat_etape_traitement.etape_traitement_id = validated_data.etape_traitement_id,
        etat_etape_traitement.is_default = validated_data.is_default

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
        'etat_etape_traitement': request_data
    }

    return jsonify(response_data), 200


def delete(current_admin: Admin, id: int):    
    try:
        etat_etape_traitement: EtatEtapeTraitement = session.query(EtatEtapeTraitement).get(id)

        etat_etape_traitement.deleted_at = datetime.datetime.utcnow()

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

