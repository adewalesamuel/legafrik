import datetime

from sqlalchemy.orm import sessionmaker, scoped_session
from flask import request, jsonify
from marshmallow import ValidationError
from ..models import Dossier, User, Admin, Demande, TypeDemande, EtatDemande,\
    EtapeTraitement
from ..db import engine
from ..schemas import DossierSchema

from environs import Env

env = Env()
env.read_env()

session = scoped_session(sessionmaker(bind=engine), scopefunc=request)


def index(current_admin: Admin):
    dossiers: Dossier = session.query(Dossier)\
        .join(User)\
        .filter(Dossier.deleted_at == None)\
        .order_by(Dossier.created_at.desc()).all()
    result = list()

    for dossier in dossiers:
        user_dict = dossier.user.toDict()
        dossier_dict = dossier.toDict()
        dossier_dict['user'] = user_dict

        result.append(dossier_dict)

    response_data = {
        'success': True,
        'dossiers': result
    }

    session.close()

    return jsonify(response_data), 200


def store(current_admin: Admin):
    request_data = request.json
    dossiers_schema = DossierSchema()

    try:
        validated_data = dossiers_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        dossier = Dossier(
            user_id = validated_data.user_id,
            numero_dossier = validated_data.numero_dossier,
        )

        session.add(dossier)
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
        'dossier': request_data
    }

    return jsonify(response_data), 200


def update(current_admin: Admin, id: int):
    request_data = request.json
    dossiers_schema = DossierSchema()

    try:
        validated_data = dossiers_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        dossier: Dossier = session.query(Dossier).get(id)

        dossier.user_id = validated_data.user_id
        dossier.numero_dossier = validated_data.numero_dossier

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
        'dossier': request_data
    }

    return jsonify(response_data), 200


def delete(current_admin: Admin, id: int):    
    try:
        dossier: Dossier = session.query(Dossier).get(id)

        dossier.deleted_at = datetime.datetime.utcnow()

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


def get_demandes(current_admin: Admin, id: int):
    demandes = session.query(Demande)\
        .join(Dossier, TypeDemande, EtatDemande)\
        .filter(Demande.deleted_at == None, Demande.dossier_id == id)\
        .order_by(Demande.created_at.desc()).all()
    result = list()

    for demande in demandes:
        type_demande_dict = demande.type_demande.toDict()
        etat_demande_dict = demande.etat_demande.toDict()
        demande_dict = demande.toDict()

        demande_dict['type_demande'] = type_demande_dict
        demande_dict['etat_demande'] = etat_demande_dict

        result.append(demande_dict)

    response_data = {
        'success': True,
        'demandes': result
    }

    session.close()

    return jsonify(response_data), 200