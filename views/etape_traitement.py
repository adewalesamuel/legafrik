import datetime

from sqlalchemy.orm import sessionmaker, scoped_session
from flask import request, jsonify
from marshmallow import ValidationError
from ..models import EtapeTraitement, Admin, EtatEtapeTraitement, TypeDemande
from ..db import engine
from ..schemas import EtapeTraitementSchema

from environs import Env

env = Env()
env.read_env()

session = scoped_session(sessionmaker(bind=engine), scopefunc=request)


def index(currebt_admin: Admin):
    etape_traitements = session.query(EtapeTraitement)\
        .filter(EtapeTraitement.deleted_at == None)\
        .order_by(EtapeTraitement.created_at.desc()).all()
    result = [row.toDict() for row in etape_traitements]
    response_data = {
        'success': True,
        'etape_traitements': result
    }

    session.close()

    return jsonify(response_data), 200


def show(current_admin: Admin, id: int):
    etape_traitement: EtapeTraitement = session.query(EtapeTraitement)\
        .join(TypeDemande).filter(EtapeTraitement.id == id, 
        EtapeTraitement.deleted_at == None).first()

    if etape_traitement is None:
        response_data = {
            "error": True,
            "message": "etape traitement not found"
        }

        return jsonify(response_data), 200


    etape_traitement_dict = etape_traitement.toDict()
    etape_traitement_dict['type_demande'] = etape_traitement.type_demande.toDict()

    response_data = {
        "success": True,
        "etape_traiement": etape_traitement_dict
    }

    return jsonify(response_data), 200


def get_etat_etape_traitements(current_admin: Admin, id: int):
    etat_etape_traitements = session.query(EtatEtapeTraitement)\
        .filter(EtatEtapeTraitement.deleted_at == None, 
        EtatEtapeTraitement.etape_traitement_id == id)\
        .order_by(EtatEtapeTraitement.created_at.asc()).all()
    result = [row.toDict() for row in etat_etape_traitements]
    response_data = {
        'success': True,
        'etat_etape_traitements': result
    }

    session.close()

    return jsonify(response_data), 200


def store(currebt_admin: Admin):
    request_data = request.json
    etape_traitements_schema = EtapeTraitementSchema()

    try:
        validated_data = etape_traitements_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        etape_traitement = EtapeTraitement(
            libelle = validated_data.libelle,
            type_demande_id = validated_data.type_demande_id,
            is_default = validated_data.is_default,
            faq = validated_data.faq
        )

        session.add(etape_traitement)
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
        'etape_traitement': request_data
    }

    return jsonify(response_data), 200


def update(current_admin: Admin, id: int):
    request_data = request.json
    etape_traitements_schema = EtapeTraitementSchema()

    try:
        validated_data = etape_traitements_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        etape_traitement: EtapeTraitement = session.query(EtapeTraitement).get(id)

        etape_traitement.libelle = validated_data.libelle
        etape_traitement.type_demande_id = validated_data.type_demande_id
        etape_traitement.is_default = validated_data.is_default
        etape_traitement.faq = validated_data.faq

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
        'etape_traitement': request_data
    }

    return jsonify(response_data), 200


def delete(current_admin: Admin, id: int):    
    try:
        etape_traitement: EtapeTraitement = session.query(EtapeTraitement).get(id)

        etape_traitement.deleted_at = datetime.datetime.utcnow()

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

