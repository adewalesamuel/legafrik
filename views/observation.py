import datetime

from sqlalchemy.orm import sessionmaker, scoped_session
from flask import request, jsonify
from marshmallow import ValidationError
from ..models import Observation, Admin, TypeDocument
from ..db import engine
from ..schemas import ObservationSchema

from environs import Env

env = Env()
env.read_env()

session = scoped_session(sessionmaker(bind=engine), scopefunc=request)


def index(currebt_admin: Admin):
    observations = session.query(Observation)\
        .join(TypeDocument).filter(Observation.deleted_at == None)\
        .order_by(Observation.created_at.desc()).all()
    result = list()
    
    for observation in observations:
        observation_dict = observation.toDict()
        observation_dict['type_document'] = observation.type_document.toDict()

        result.append(observation_dict)

    response_data = {
        'success': True,
        'observations': result
    }

    session.close()

    return jsonify(response_data), 200


def show(current_admin: Admin, id: int):
    observation: Observation = session.query(Observation)\
        .join(TypeDocument).filter(Observation.id == id, 
        Observation.deleted_at == None).first()

    if observation is None:
        response_data = {
            "error": True,
            "message": "observation not found"
        }
        session.close()

        return jsonify(response_data), 200


    observation_dict = observation.toDict()
    observation_dict['type_document'] = observation.type_document.toDict()

    response_data = {
        "success": True,
        "etape_traiement": observation_dict
    }
    session.close()

    return jsonify(response_data), 200


def store(currebt_admin: Admin):
    request_data = request.json
    observations_schema = ObservationSchema()

    try:
        validated_data = observations_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        observation = Observation(
            demande_id = validated_data.demande_id,
            type_document_id = validated_data.type_document_id,
            content = validated_data.content,
            document_url = validated_data.document_url
        )

        session.add(observation)
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
        'observation': request_data
    }

    return jsonify(response_data), 200


def update(current_admin: Admin, id: int):
    request_data = request.json
    observations_schema = ObservationSchema()

    try:
        validated_data = observations_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        observation: Observation = session.query(Observation).get(id)

        observation.demande_id = validated_data.demande_id
        observation.type_document_id = validated_data.type_document_id
        observation.content = validated_data.content
        observation.document_url = validated_data.document_url

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
        'observation': request_data
    }

    return jsonify(response_data), 200


def delete(current_admin: Admin, id: int):    
    try:
        observation: Observation = session.query(Observation).get(id)

        observation.deleted_at = datetime.datetime.utcnow()

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

