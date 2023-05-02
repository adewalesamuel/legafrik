import datetime

from sqlalchemy.orm import sessionmaker, scoped_session
from flask import request, jsonify
from marshmallow import ValidationError
from ..models import TypePiece, Admin
from ..db import engine
from ..schemas import TypePieceSchema

from environs import Env

env = Env()
env.read_env()

session = scoped_session(sessionmaker(bind=engine), scopefunc=request)


def index(current_admin: Admin):
    type_pieces = session.query(TypePiece)\
        .filter(TypePiece.deleted_at == None)\
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
    type_pieces_schema = TypePieceSchema()

    try:
        validated_data = type_pieces_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        type_piece = TypePiece(
            libelle = validated_data.libelle,
            type_demande_id = validated_data.type_demande_id,
            is_particulier = validated_data.is_particulier
        )

        session.add(type_piece)
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
        'type_piece': request_data
    }

    return jsonify(response_data), 200


def update(current_admin: Admin, id: int):
    request_data = request.json
    type_pieces_schema = TypePieceSchema()

    try:
        validated_data = type_pieces_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        type_piece: TypePiece = session.query(TypePiece).get(id)

        type_piece.libelle = validated_data.libelle
        type_piece.type_demande_id = validated_data.type_demande_id,
        type_piece.is_particulier = validated_data.is_particulier

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
        'type_piece': request_data
    }

    return jsonify(response_data), 200


def delete(current_admin: Admin, id: int):    
    try:
        type_piece: TypePiece = session.query(TypePiece).get(id)

        type_piece.deleted_at = datetime.datetime.utcnow()

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

