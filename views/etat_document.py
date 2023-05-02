import datetime

from sqlalchemy.orm import sessionmaker, scoped_session
from flask import request, jsonify
from marshmallow import ValidationError
from ..models import EtatDocument, Admin
from ..db import engine
from ..schemas import EtatDocumentSchema

from environs import Env

env = Env()
env.read_env()

session = scoped_session(sessionmaker(bind=engine), scopefunc=request)


def index(current_admin: Admin):
    etat_documents = session.query(EtatDocument)\
        .filter(EtatDocument.deleted_at == None)\
        .order_by(EtatDocument.created_at.desc()).all()
    result = [row.toDict() for row in etat_documents]
    response_data = {
        'success': True,
        'etat_documents': result
    }

    session.close()

    return jsonify(response_data), 200


def store(current_admin: Admin):
    request_data = request.json
    etat_documents_schema = EtatDocumentSchema()

    try:
        validated_data = etat_documents_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        etat_document = EtatDocument(
            libelle = validated_data.libelle,
        )

        session.add(etat_document)
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
        'etat_document': request_data
    }

    return jsonify(response_data), 200


def update(current_admin: Admin, id: int):
    request_data = request.json
    etat_documents_schema = EtatDocumentSchema()

    try:
        validated_data = etat_documents_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        etat_document: EtatDocument = session.query(EtatDocument).get(id)

        etat_document.libelle = validated_data.libelle

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
        'etat_document': request_data
    }

    return jsonify(response_data), 200


def delete(current_admin: Admin, id: int):    
    try:
        etat_document: EtatDocument = session.query(EtatDocument).get(id)

        etat_document.deleted_at = datetime.datetime.utcnow()

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

