import datetime
import json

from sqlalchemy.orm import sessionmaker, scoped_session
from flask import request, jsonify
from marshmallow import ValidationError
from ..models import StatusEtatTraitement, Admin, EtatEtapeTraitement, EtapeTraitement, Demande, Pays, User, Dossier
from ..db import engine
from ..schemas import StatusEtatTraitementSchema
from ..utils import mail, status_response
from environs import Env

env = Env()
env.read_env()

session = scoped_session(sessionmaker(bind=engine), scopefunc=request)


def index(current_admin: Admin):
    status_etat_traitements = session.query(StatusEtatTraitement)\
        .filter(StatusEtatTraitement.deleted_at == None)\
        .order_by(StatusEtatTraitement.created_at.desc()).all()
    result = [row.toDict() for row in status_etat_traitements]
    response_data = {
        'success': True,
        'status_etat_traitements': result
    }

    session.close()

    return jsonify(response_data), 200


def store(current_admin: Admin):
    request_data = request.json
    status_etat_traitements_schema = StatusEtatTraitementSchema()

    try:
        validated_data = status_etat_traitements_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    try:
        status_etat_traitement = session.query(StatusEtatTraitement)\
            .filter(StatusEtatTraitement.deleted_at == None,
            StatusEtatTraitement.demande_id == validated_data.demande_id,
            StatusEtatTraitement.etape_traitement_id == validated_data.etape_traitement_id,)\
            .first()
        
        if (status_etat_traitement is not None):
            raise Exception('status etat traitement exists')
            
        status_etat_traitement = StatusEtatTraitement(
            demande_id = validated_data.demande_id,
            etape_traitement_id = validated_data.etape_traitement_id,
            etat_etape_traitement_id = validated_data.etat_etape_traitement_id,
            temps_estime = validated_data.temps_estime,
            description = validated_data.description
        )

        session.add(status_etat_traitement)
        session.commit()

        try:
            etat_etape_traitement: EtatEtapeTraitement = session.query(EtatEtapeTraitement).get(validated_data.etat_etape_traitement_id)
            if(etat_etape_traitement.is_mail):
                etape_traitement: EtapeTraitement = session.query(EtapeTraitement).get(validated_data.etape_traitement_id)
                try:
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

                    mail.all_mail_data(etat_etape_traitement.chemin_mail, etape_traitement.libelle+' - '+etat_etape_traitement.libelle+' ('+json_objet['nom-entreprise']+')', [user['email']], data)
                except Exception as e:
                    print(e)
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
        'status_etat_traitement': request_data
    }

    return jsonify(response_data), 200


def update(current_admin: Admin, id: int):
    request_data = request.json
    status_etat_traitements_schema = StatusEtatTraitementSchema()

    try:
        validated_data = status_etat_traitements_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        status_etat_traitement: StatusEtatTraitement = session.query(StatusEtatTraitement).get(id)

        status_etat_traitement.demande_id = validated_data.demande_id,
        status_etat_traitement.etape_traitement_id = validated_data.etape_traitement_id,
        status_etat_traitement.etat_etape_traitement_id = validated_data.etat_etape_traitement_id,
        status_etat_traitement.temps_estime = validated_data.temps_estime
        status_etat_traitement.description = validated_data.description

        session.commit()


        etat_etape_traitement: EtatEtapeTraitement = session.query(EtatEtapeTraitement).get(validated_data.etat_etape_traitement_id)
        if(etat_etape_traitement.is_mail):
            etape_traitement: EtapeTraitement = session.query(EtapeTraitement).get(validated_data.etape_traitement_id)
            try:
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

                mail.all_mail_data(etat_etape_traitement.chemin_mail, etape_traitement.libelle+' - '+etat_etape_traitement.libelle+' ('+json_objet['nom-entreprise']+')', [user['email']], data)
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
        'status_etat_traitement': request_data
    }

    return jsonify(response_data), 200


def delete(current_admin: Admin, id: int):    
    try:
        status_etat_traitement: StatusEtatTraitement = session.query(StatusEtatTraitement).get(id)

        status_etat_traitement.deleted_at = datetime.datetime.utcnow()

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



def etat_mail(demande_id: int, etape_traitement_id: int, etat_etape_traitement_id: int):

    demande = session.query(Demande)\
        .join(Pays, Dossier)\
        .filter(Demande.deleted_at == None, Demande.id == demande_id).first()
    etape_traitement = session.query(EtapeTraitement)\
        .filter(EtapeTraitement.deleted_at == None, EtapeTraitement.id == etape_traitement_id).first()
    etat_etape_traitement = session.query(EtatEtapeTraitement)\
        .filter(EtatEtapeTraitement.deleted_at == None, EtatEtapeTraitement.id == etat_etape_traitement_id).first()
    
    demande_rep = demande.toDict()
    demande_rep['user'] = demande.dossier.user.toDict()
    
    if(etat_etape_traitement.libelle == 'Terminé' and etape_traitement.libelle == 'Redaction documents'):
        route_template =  "mails/ci/doc_redige.html"
    elif(etat_etape_traitement.libelle == 'En cours' and etape_traitement.libelle == "Formalités d\'immatriculation"):
        route_template =  "mails/ci/doc_trans_cepici.html"
    elif(etat_etape_traitement.libelle == 'Terminé' and etape_traitement.libelle == "Formalités d\'immatriculation"):
        #route_template =  "mails/ci/doc_redige.html"
        print("")
    elif(etat_etape_traitement.libelle == 'En cours' and etape_traitement.libelle == "Formalités d\'immatriculation"):
        route_template =  "mails/ci/doc_trans_cepici.html"
    elif(etat_etape_traitement.libelle == 'Terminé' and etape_traitement.libelle == "Formalités d\'immatriculation"):
        route_template =  "mails/ci/doc_redige.html"
    
    #print(demande) #
    #print(etape_traitement) # Finalisée -  En cours - Initiée
    #print(etat_etape_traitement)

        data = {
            "object": route_template,
            "chemin": etape_traitement.libelle,
            "email": demande_rep['user']['email'],
            "user": demande_rep['user']
        }

    return data


