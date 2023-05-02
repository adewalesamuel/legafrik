import datetime

from sqlalchemy.orm import sessionmaker, scoped_session
from flask import request, jsonify
from marshmallow import ValidationError
from ..models import Demande, Admin, Attribution
from ..db import engine
from ..schemas import AttributionSchema

from environs import Env

env = Env()
env.read_env()

session = scoped_session(sessionmaker(bind=engine), scopefunc=request)


def index(current_admin: Admin):
    attributions = session.query(Attribution)\
        .filter(Attribution.deleted_at == None)\
        .order_by(Attribution.created_at.desc()).all()
    result = [row.toDict() for row in attributions]
    response_data = {
        'success': True,
        'attributions': result
    }

    session.close()

    return jsonify(response_data), 200


def show(current_admin: Admin, id: int):
    attribution = session.query(Attribution)\
        .join(Demande).filter(Attribution.deleted_at == None,
        Attribution.id == id).first()
    
    result = attribution.toDict()
    commercial = session.query(Admin).filter(
        Admin.id == attribution.commercial_id, 
        Admin.deleted_at == None).first()
    juriste = session.query(Admin).filter(
        Admin.id == attribution.juriste_id, 
        Admin.deleted_at == None).first()
    formaliste = session.query(Admin).filter(
        Admin.id == attribution.formaliste_id, 
        Admin.deleted_at == None).first()
    
    result['demande'] = attribution.demande.toDict()

    if (commercial is not None):
        result['commercial'] = commercial.toDict()
    if (juriste is not None):
        result['juriste'] = juriste.toDict()
    if (formaliste is not None):
        result['formaliste'] = formaliste.toDict()
    
    response_data = {
        "success": True,
        "attribution": result
    }

    session.close()

    return jsonify(response_data), 200


def store(current_admin: Admin):
    request_data = request.json
    attributiona = AttributionSchema()

    try:
        validated_data = attributiona.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400

    
    try:
        attribution = Attribution(
            formaliste_id = validated_data.formaliste_id,
            commercial_id = validated_data.commercial_id,
            juriste_id = validated_data.juriste_id,
            demande_id = validated_data.demande_id
        )

        session.add(attribution)
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
        'attribution': request_data
    }

    return jsonify(response_data), 200


def update(current_admin: Admin, id: int):
    request_data = request.json
    attributiona = AttributionSchema()

    try:
        validated_data = attributiona.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        attribution: Attribution = session.query(Attribution).get(id)

        attribution.formaliste_id = validated_data.formaliste_id,
        attribution.commercial_id = validated_data.commercial_id,
        attribution.juriste_id = validated_data.juriste_id,
        attribution.demande_id = validated_data.demande_id

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
        'attribution': request_data
    }

    return jsonify(response_data), 200


def delete(current_admin: Admin, id: int):    
    try:
        attribution: Attribution = session.query(Attribution).get(id)

        attribution.deleted_at = datetime.datetime.utcnow()

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

