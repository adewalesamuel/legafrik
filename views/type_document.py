import datetime

from sqlalchemy.orm import sessionmaker, scoped_session
from flask import request, jsonify
from marshmallow import ValidationError
from ..models import TypeDocument, Admin
from ..db import engine
from ..schemas import TypeDocumentSchema

from environs import Env

env = Env()
env.read_env()

session = scoped_session(sessionmaker(bind=engine), scopefunc=request)


def index(current_admin: Admin):
    type_documents = session.query(TypeDocument)\
        .filter(TypeDocument.deleted_at == None)\
        .order_by(TypeDocument.created_at.desc()).all()
    result = [row.toDict() for row in type_documents]
    response_data = {
        'success': True,
        'type_documents': result
    }

    session.close()

    return jsonify(response_data), 200


def store(current_admin: Admin):
    request_data = request.json
    type_documents_schema = TypeDocumentSchema()

    try:
        validated_data = type_documents_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        type_document = TypeDocument(
            libelle = validated_data.libelle,
            type_demande_id = validated_data.type_demande_id
        )

        session.add(type_document)
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
        'type_document': request_data
    }

    return jsonify(response_data), 200


def update(current_admin: Admin, id: int):
    request_data = request.json
    type_documents_schema = TypeDocumentSchema()

    try:
        validated_data = type_documents_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        type_document: TypeDocument = session.query(TypeDocument).get(id)

        type_document.libelle = validated_data.libelle
        type_document.type_demande_id = validated_data.type_demande_id

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
        'type_document': request_data
    }

    return jsonify(response_data), 200


def delete(current_admin: Admin, id: int):    
    try:
        type_document: TypeDocument = session.query(TypeDocument).get(id)

        type_document.deleted_at = datetime.datetime.utcnow()

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

