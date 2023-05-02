import datetime

from sqlalchemy import or_
from sqlalchemy.orm import sessionmaker, scoped_session
from flask import request, jsonify
from marshmallow import ValidationError
from ..models import Message, Admin
from ..db import engine
from ..schemas import MessageSchema

from environs import Env

env = Env()
env.read_env()

session = scoped_session(sessionmaker(bind=engine), scopefunc=request)


def index(current_admin: Admin):
    admins = session.query(Admin).filter(Admin.deleted_at == None).all()
    admins_ids = [row.id for row in admins]
    messages = session.query(Message)\
        .filter(Message.deleted_at == None, 
        Message.type_message == request.args.get('type_message'), 
        or_(Message.receiver_id.in_(admins_ids), 
        Message.receiver_id == None))\
        .order_by(Message.created_at.desc()).all()
    result = [row.toDict() for row in messages]

    response_data = {
        'success': True,
        'messages': result
    }

    session.close()

    return jsonify(response_data), 200


def store(current_admin: Admin):
    request_data = request.json
    messages_schema = MessageSchema()

    try:
        validated_data = messages_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        message = Message(
            sender_id = current_admin.id,
            receiver_id = validated_data.receiver_id,
            type_message = validated_data.type_message,
            content = validated_data.content,
        )

        session.add(message)
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
        'message': request_data
    }

    return jsonify(response_data), 200


def mark_as_read(current_admin: Admin, id: int):
    request_data = request.json

    try:
        message: Message = session.query(Message).get(id)

        message.read_at = datetime.datetime.utcnow()

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
        'message': request_data
    }

    return jsonify(response_data), 200


def delete(current_admin: Admin, id: int):    
    try:
        message: Message = session.query(Message).get(id)

        message.deleted_at = datetime.datetime.utcnow()

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

