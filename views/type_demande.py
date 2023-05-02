import datetime

from sqlalchemy.orm import sessionmaker, scoped_session
from flask import request, jsonify
from marshmallow import ValidationError
from ..models import TypeDemande, Admin, EtapeTraitement, TypeDocument,\
    TypePiece, Pays
from ..db import engine
from ..schemas import TypeDemandeSchema

from environs import Env

env = Env()
env.read_env()

session = scoped_session(sessionmaker(bind=engine), scopefunc=request)


def index(current_admin: Admin):
    type_demandes = session.query(TypeDemande)\
        .filter(TypeDemande.deleted_at == None)\
        .order_by(TypeDemande.created_at.desc()).all()
    result = [row.toDict() for row in type_demandes]
    response_data = {
        'success': True,
        'type_demandes': result
    }

    session.close()

    return jsonify(response_data), 200


def show(id: int):
    type_demande = session.query(TypeDemande)\
        .join(Pays).filter(TypeDemande.deleted_at == None,
        TypeDemande.id == id).first()
    result = type_demande.toDict()
    result['pays'] = type_demande.pays.toDict()
    response_data = {
        "success": True,
        "type_demande": result
    }

    session.close()

    return jsonify(response_data), 200


def get_etape_traitements(current_admin: Admin, id: int):
    etape_traitements = session.query(EtapeTraitement)\
        .filter(EtapeTraitement.deleted_at == None, 
        EtapeTraitement.type_demande_id == id)\
        .order_by(EtapeTraitement.created_at.asc()).all()
    result = [row.toDict() for row in etape_traitements]

    response_data = {
        'success': True,
        'etape_traitements': result
    }

    session.close()

    return jsonify(response_data), 200


def get_type_documents(current_admin: Admin, id: int):
    type_documents = session.query(TypeDocument)\
        .filter(TypeDocument.deleted_at == None, 
        TypeDocument.type_demande_id == id)\
        .order_by(TypeDocument.created_at.desc()).all()
    result = [row.toDict() for row in type_documents]
    response_data = {
        'success': True,
        'type_documents': result
    }

    session.close()

    return jsonify(response_data), 200


def get_type_pieces(current_admin: Admin, id: int):
    type_pieces = session.query(TypePiece)\
        .filter(TypePiece.deleted_at == None,
        TypePiece.type_demande_id == id)\
        .order_by(TypePiece.created_at.desc()).all()
    result = [row.toDict() for row in type_pieces]
    response_data = {
        'success': True,
        'type_pieces': result
    }

    session.close()

    return jsonify(response_data), 200


def store(current_admin: Admin):
    request_data = request.json
    type_demandea = TypeDemandeSchema()

    try:
        validated_data = type_demandea.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400

    
    try:
        type_demande = TypeDemande(
            libelle = validated_data.libelle,
            tarif = validated_data.tarif,
            pays_id = validated_data.pays_id,
        )

        session.add(type_demande)
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
        'type_demande': request_data
    }

    return jsonify(response_data), 200


def update(current_admin: Admin, id: int):
    request_data = request.json
    type_demandea = TypeDemandeSchema()

    try:
        validated_data = type_demandea.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        type_demande: TypeDemande = session.query(TypeDemande).get(id)

        type_demande.libelle = validated_data.libelle
        type_demande.tarif = validated_data.tarif
        type_demande.pays_id = validated_data.pays_id,

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
        'type_demande': request_data
    }

    return jsonify(response_data), 200


def delete(current_admin: Admin, id: int):    
    try:
        type_demande: TypeDemande = session.query(TypeDemande).get(id)
        type_demande.deleted_at = datetime.datetime.utcnow()

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

