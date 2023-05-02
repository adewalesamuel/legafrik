import datetime
import json

from sqlalchemy.orm import sessionmaker, scoped_session
from flask import request, jsonify
from marshmallow import ValidationError
from ..models import Document, TypeDocument, EtatDocument, Demande,\
    Admin, Dossier, EtapeTraitement, EtatEtapeTraitement
from ..db import engine
from ..schemas import DocumentSchema
from ..utils import mail, status_response

from environs import Env

env = Env()
env.read_env()

session = scoped_session(sessionmaker(bind=engine), scopefunc=request)


def index(current_admin: Admin):
    etape_traitement_id  = request.args.get('etape_traitement_id')
    documents = session.query(Document)\
        .join(TypeDocument, EtatDocument, Demande)

    if etape_traitement_id is not None:
        documents = documents.filter(
            Document.etape_traitement_id == etape_traitement_id)

    documents = documents.filter(Document.deleted_at == None)\
        .order_by(Document.created_at.desc()).all()
    result = list()

    for document in documents:
        type_document_dict = document.type_document.toDict()
        etat_document_dict = document.etat_document.toDict()
        demande_dict = document.demande.toDict()
        document_dict = document.toDict()

        document_dict['type_document'] = type_document_dict
        document_dict['etat_document'] = etat_document_dict
        document_dict['demande'] = demande_dict

        result.append(document_dict)

    response_data = {
        'success': True,
        'documents': result
    }

    session.close()

    return jsonify(response_data), 200


def store(current_admin: Admin):
    request_data = request.json
    documents_schema = DocumentSchema()

    try:
        validated_data = documents_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        document = Document(
            type_document_id = validated_data.type_document_id,
            etat_document_id = validated_data.etat_document_id,
            demande_id = validated_data.demande_id,
            champs_document = validated_data.champs_document,
            document_url = validated_data.document_url,
            etape_traitement_id = validated_data.etape_traitement_id,
        )

        session.add(document)
        session.commit()
        
        try:
            #etat_etape_traitement: EtatEtapeTraitement = session.query(EtatEtapeTraitement).get(validated_data.etat_etape_traitement_id)    
            etape_traitement: EtapeTraitement = session.query(EtapeTraitement).get(validated_data.etape_traitement_id)
            demande = session.query(Demande)\
            .join(Dossier)\
            .filter(Demande.deleted_at == None, Demande.id == validated_data.demande_id,).first()

            #demande_dict = demande.toDict()
            user = demande.dossier.user.toDict()
            data = {
                "demande_id": validated_data.demande_id,
                "username": user['username']
            }
            string = demande.champs_demande
            json_objet = json.loads(string)
            if(validated_data.etape_traitement_id == 12 or validated_data.etape_traitement_id == 24 or validated_data.etape_traitement_id == 30 or validated_data.etape_traitement_id == 37):
                mail.all_mail_data('mails/ci/rccm_dispo.html', etape_traitement.libelle+' - ('+json_objet['nom-entreprise']+')', [user['email']], data)
            elif(validated_data.etape_traitement_id == 14 or validated_data.etape_traitement_id == 121):
                mail.all_mail_data('mails/ci/doc_dfe_dispo.html', etape_traitement.libelle+' - ('+json_objet['nom-entreprise']+')', [user['email']], data)
            

        except Exception as e:
            print(e)
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
        'document': request_data
    }

    return jsonify(response_data), 200


def update(current_admin: Admin, id: int):
    request_data = request.json
    documents_schema = DocumentSchema()

    try:
        validated_data = documents_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        document: Document = session.query(Document).get(id)

        document.type_document_id = validated_data.type_document_id
        document.etat_document_id = validated_data.etat_document_id
        document.demande_id = validated_data.demande_id
        document.champs_document = validated_data.champs_document
        document.document_url = validated_data.document_url,
        document.etape_traitement_id = validated_data.etape_traitement_id,

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
        'document': request_data
    }

    return jsonify(response_data), 200


def delete(current_admin: Admin, id: int):    
    try:
        document: Document = session.query(Document).get(id)
        document.deleted_at = datetime.datetime.utcnow()

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



def send_document_sup_mail():
    request_data = request.json
    #print(request_data.get("subject"))
    response = mail.send_document_sup_mail(request_data.get("subject"), request_data.get("receivers"), request_data.get("datas"))
    return status_response.success_response('Mail Test', {
        'success': response,
        'role': 'file.name'
    })