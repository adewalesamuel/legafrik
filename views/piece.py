import datetime

from sqlalchemy.orm import sessionmaker, scoped_session
from flask import request, jsonify
from marshmallow import ValidationError
from ..models import Piece, Demande, TypePiece, Admin
from ..db import engine
from ..schemas import PieceSchema

from environs import Env

env = Env()
env.read_env()

session = scoped_session(sessionmaker(bind=engine), scopefunc=request)


def index(current_admin: Admin):
    pieces: Piece = session.query(Piece)\
        .join(Demande, TypePiece)\
        .filter(Piece.deleted_at == None)\
        .order_by(Piece.created_at.desc()).all()
    result = list()

    for piece in pieces:
        demande_dict = piece.demande.toDict()
        piece_dict = piece.toDict()
        type_piece_dict = piece.type_piece.toDict()

        piece_dict['demande'] = demande_dict
        piece_dict['type_piece'] = type_piece_dict

        result.append(piece_dict)

    response_data = {
        'success': True,
        'pieces': result
    }

    session.close()

    return jsonify(response_data), 200


def store(current_admin: Admin):
    request_data = request.json
    pieces_schema = PieceSchema()

    try:
        validated_data = pieces_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        piece = Piece(
            demande_id = validated_data.demande_id,
            type_piece_id = validated_data.type_piece_id,
            piece_url = validated_data.piece_url,
        )

        session.add(piece)
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
        'piece': request_data
    }

    return jsonify(response_data), 200


def update(current_admin: Admin, id: int):
    request_data = request.json
    pieces_schema = PieceSchema()

    try:
        validated_data = pieces_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        piece: Piece = session.query(Piece).get(id)

        piece.demande_id = validated_data.demande_id
        piece.type_piece_id = validated_data.type_piece_id,
        piece.piece_url = validated_data.piece_url,

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
        'piece': request_data
    }

    return jsonify(response_data), 200


def delete(current_admin: Admin, id: int):    
    try:
        piece: Piece = session.query(Piece).get(id)

        piece.deleted_at = datetime.datetime.utcnow()

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

