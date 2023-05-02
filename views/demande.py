import datetime
import json

from sqlalchemy.orm import sessionmaker, scoped_session
from flask import request, jsonify
from marshmallow import ValidationError
from ..models import Demande, Dossier, TypeDemande, EtatDemande, EtapeTraitement,\
     Admin, Paiement, TypePaiement, Demande, MoyenPaiement, Document, EtatDocument,\
    TypeDocument, Observation, TypeDocument, Piece, TypePiece, StatusEtatTraitement
from ..db import engine
from ..schemas import DemandeSchema, UpdateDemandeEtapeTraitementSchema, ChampsQuestionnaireSchema
from ..utils import status_response, generate_pdf, mail, data

from environs import Env

env = Env()
env.read_env()

session = scoped_session(sessionmaker(bind=engine), scopefunc=request)


def index(current_admin: Admin):
    pays_id  = request.args.get('pays_id')
    demandes = session.query(Demande)\
        .join(Dossier, TypeDemande, EtatDemande)
    
    if (pays_id is not None):
        demandes = demandes.filter(Demande.pays_id == pays_id)

    demandes = data.paginate(demandes.filter(Demande.deleted_at == None)\
        .order_by(Demande.updated_at.desc()), page=request.args.get('page'))
    result = list()

    for demande in demandes['result']:
        user_dict = demande.dossier.user.toDict()
        type_demande_dict = demande.type_demande.toDict()
        etat_demande_dict = demande.etat_demande.toDict()
        demande_dict = demande.toDict()

        demande_dict['user'] = user_dict
        demande_dict['type_demande'] = type_demande_dict
        demande_dict['etat_demande'] = etat_demande_dict

        result.append(demande_dict)

    response_data = {
        'success': True,
        'demandes': result,
        'current_page': demandes['page'],
        'size': demandes['pagesize'],
        'total': demandes['total']
    }

    session.close()

    return jsonify(response_data), 200


def get_paiements(current_admin: Admin, id: int):
    paiements = session.query(Paiement )\
        .join(TypePaiement, MoyenPaiement, Demande)\
        .filter(Paiement.deleted_at == None, Paiement.demande_id == id)\
        .order_by(Paiement.created_at.desc()).all()
    result = list()

    for paiement in paiements:
        type_paiement_dict = paiement.type_paiement.toDict()
        moyen_paiement_dict = paiement.moyen_paiement.toDict()
        paiement_dict = paiement.toDict()

        paiement_dict['type_paiement'] = type_paiement_dict
        paiement_dict['moyen_paiement'] = moyen_paiement_dict

        result.append(paiement_dict)

    response_data = {
        'success': True,
        'paiements': result
    }

    session.close()

    return jsonify(response_data), 200


def get_pieces(current_admin: Admin, id: int):
    pieces = session.query(Piece)\
        .join(TypePiece)\
        .filter(Piece.deleted_at == None, 
        Piece.demande_id == id)\
        .order_by(Piece.created_at.desc()).all()
    result = list()

    for piece in pieces:
        piece_dict = piece.toDict()
        type_piece_dict = piece.type_piece.toDict()

        piece_dict['type_piece'] = type_piece_dict

        result.append(piece_dict)  

    response_data = {
        "success": True,
        "pieces": result
    }

    session.close()

    return jsonify(response_data)


def get_documents(current_admin: Admin, id: int):
    documents = session.query(Document)\
        .join(TypeDocument, EtatDocument, Demande)\
        .filter(Document.deleted_at == None, Document.demande_id == id)\
        .order_by(Document.created_at.desc()).all()
    
    etape_traitement_id  = request.args.get('etape_traitement_id')
    documents = session.query(Document)\
        .join(TypeDocument, EtatDocument, Demande)

    if etape_traitement_id is not None:
        documents = documents.filter(
            Document.etape_traitement_id == etape_traitement_id)

    documents = documents.filter(Document.demande_id == id, 
                                 Document.deleted_at == None)\
                                    .order_by(Document.created_at.desc()).all()
    result = list()

    for document in documents:
        type_document_dict = document.type_document.toDict()
        etat_document_dict = document.etat_document.toDict()
        document_dict = document.toDict()

        document_dict['type_document'] = type_document_dict
        document_dict['etat_document'] = etat_document_dict

        result.append(document_dict)

    response_data = {
        'success': True,
        'documents': result
    }

    session.close()

    return jsonify(response_data), 200


def get_observations(currebt_admin: Admin, id: int):
    observations = session.query(Observation)\
        .join(TypeDocument).filter(Observation.deleted_at == None,
        Observation.demande_id == id)\
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
    try: 
        demande = session.query(Demande)\
            .join(Dossier, TypeDemande, EtatDemande)\
            .filter(Demande.deleted_at == None, Demande.id == id).first()
        
        if demande is None:
            raise Exception('demande not found')
        
        typeDocument = session.query(TypeDocument)\
                .filter(TypeDocument.libelle == 'Document récapitulatif du questionnaire demande')\
                .first()
        
        document = session.query(Document).filter(Document.demande_id == demande.id, Document.type_document_id == typeDocument.id).first()
        if document is None:
            document = 'NULL'
        else:
            document = document.toDict()

        demande_dict = demande.toDict()
        demande_dict['user'] = demande.dossier.user.toDict()
        demande_dict['type_demande'] = demande.type_demande.toDict()
        demande_dict['etat_demande'] = demande.etat_demande.toDict()
        demande_dict['pays'] = demande.pays.toDict()
        # demande_dict['etape_traitement'] = demande.etape_traitement.toDict()
        demande_dict['document'] = document
    except Exception as err:
        session.close()

        response_data = {
            "error": True,
            "message": str(err)
        }

        return jsonify(response_data), 500

    response_data = {
        "success": True,
        "demande": demande_dict
    }

    session.close()

    return jsonify(response_data), 200

def show_status_etat_traitement(current_admin: Admin, 
                                demande_id: int, etape_traitement_id: int):
    try:
        demande = session.query(Demande).filter(
            Demande.id == demande_id, Demande.deleted_at == None).first()

        if demande is None: 
            raise Exception("demande not found")

        status_etat_traitement = session.query(StatusEtatTraitement)\
            .filter(StatusEtatTraitement.demande_id == demande_id,
            StatusEtatTraitement.etape_traitement_id == etape_traitement_id, 
            StatusEtatTraitement.deleted_at == None).first()

        if status_etat_traitement is None:
            raise Exception("status etat traitement not found")
    except Exception as err:
        session.close()

        response_data = {
            "error": True,
            "message": str(err)
        }

        return jsonify(response_data), 404

    response_data = {
        'success': True,
        'status_etat_traitement': status_etat_traitement.toDict()
    }

    session.close()

    return jsonify(response_data), 200


def store(current_admin: Admin):
    request_data = request.json
    demandes_schema = DemandeSchema()

    try:
        validated_data = demandes_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        demande = Demande(
            dossier_id = validated_data.dossier_id,
            champs_demande = validated_data.champs_demande,
            type_demande_id = validated_data.type_demande_id,
            etape_traitement_id = validated_data.etape_traitement_id,
            pays_id = validated_data.pays_id,
            etat_demande_id = validated_data.etat_demande_id,
            numero_demande = validated_data.numero_demande,
            montant_total = validated_data.montant_total
        )

        session.add(demande)
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
        'demande': request_data
    }

    return jsonify(response_data), 200


def update(current_admin: Admin, id: int):
    request_data = request.json
    demandes_schema = DemandeSchema()

    try:
        validated_data = demandes_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        demande: Demande = session.query(Demande).get(id)

        demande.dossier_id = validated_data.dossier_id
        demande.champs_demande = validated_data.champs_demande
        demande.type_demande_id = validated_data.type_demande_id
        demande.etape_traitement_id = validated_data.etape_traitement_id
        demande.pays_id = validated_data.pays_id
        demande.etat_demande_id = validated_data.etat_demande_id
        demande.numero_demande = validated_data.numero_demande

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
        'demande': request_data
    }

    return jsonify(response_data), 200

def update_etape_traitement(current_admin: Admin, id: int):
    request_data = request.json
    demande_schema = UpdateDemandeEtapeTraitementSchema()

    try:
        validated_data = demande_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400

    try:
        # TODO get wherer not deleted
        demande: Demande = session.query(Demande).get(id)

        if demande is None:
            raise Exception("demande not found")

        etape_traitement: EtapeTraitement = session.query(EtapeTraitement).filter(
            EtapeTraitement.id == validated_data.etape_traitement_id, 
            EtapeTraitement.type_demande_id == demande.type_demande_id,
            EtapeTraitement.deleted_at == None).first()

        if etape_traitement is None:
            raise Exception("etape traitement not found")

        demande.etape_traitement_id = etape_traitement.id

        session.commit()
        session.refresh(demande)
        #print(current_user.toDict())

        demandet = session.query(Demande)\
        .join(Dossier)\
        .filter(Demande.deleted_at == None, Demande.id == id).first()

        #demande_dict = demande.toDict()
        user = demandet.dossier.user.toDict()
        data = {
            "demande_id": id,
            "username": user['username']
        }
        string = demandet.champs_demande
        json_objet = json.loads(string)
        if(etape_traitement.libelle == "Formalités d'immatriculation"):
            try:
                mail.all_mail_data('mails/ci/doc_rattachement_fiscale.html', 'Votre entreprise '+json_objet['nom-entreprise']+' est en cours d\'immatriculation', user['email'], data)
            except Exception as e:
                print(e)
        elif(etape_traitement.libelle == 'XXX'):
            try:
                mail.all_mail_data('mails/admins/notif_ajout_document.html', 'Notification ajout de document de '+json_objet['nom-entreprise'], ['d.lemec93@gmail.com','contact@legafrik.com'], data)
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
        "success": True,
        "demande": demande.toDict()
    }

    return jsonify(response_data), 200


def update_questionnaire(current_admin: Admin, id: int):
    request_data = request.json
    champs_questionnaire_schema = ChampsQuestionnaireSchema()

    try:
        validated_data = champs_questionnaire_schema.load(
            request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400

    try:
        demande: Demande = session.query(Demande).get(id)

        demande.champs_questionnaire = validated_data.champs_questionnaire

        session.commit()
        session.refresh(demande)
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
        'demande': demande.toDict() 
    }

    return jsonify(response_data), 200


def delete(current_admin: Admin, id: int):    
    try:
        demande: Demande = session.query(Demande).get(id)

        demande.deleted_at = datetime.datetime.utcnow()

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


def gen_recap_demande_pdf(current_admin: Admin, id: int):

    #return jsonify(current_admin.toDict()), 200
    try:
        demande = session.query(Demande)\
            .join(Dossier, TypeDemande, EtatDemande)\
            .filter(Demande.deleted_at == None, Demande.id == id).first()
        
        if demande is None:
            raise Exception('demande not found')
        
        demande_dict = demande.toDict()
        demande_dict['user'] = demande.dossier.user.toDict()
        demande_dict['type_demande'] = demande.type_demande.toDict()
        demande_dict['etat_demande'] = demande.etat_demande.toDict()
        demande_dict['pays'] = demande.pays.toDict()
        # demande_dict['etape_traitement'] = demande.etape_traitement.toDict()
    except Exception as err:
        session.close()

        response_data = {
            "error": True,
            "message": str(err)
        }

        return jsonify(response_data), 200


    typeDemande = session.query(TypeDocument)\
            .filter(TypeDocument.libelle == 'Document récapitulatif du questionnaire demande')\
            .first()
    
    etatDemande = session.query(EtatDocument)\
            .filter(EtatDocument.libelle == 'Terminé')\
            .first()
    
    document = session.query(Document)\
        .filter(Document.demande_id == demande.id, Document.type_document_id == typeDemande.id).first()
            
    if document is None:
        data_s3 = generate_pdf.gen_recap_demande_new_pdf(generate_pdf.optionsPortraitA4, demande_dict)
        
        document = Document(
            type_document_id = typeDemande.id,
            etat_document_id = etatDemande.id,
            demande_id = demande.id,
            champs_document = "Document récapitulatif du questionnaire demande",
            document_url = data_s3,
            #etape_traitement_id = validated_data.etape_traitement_id,
        )
        session.add(document)
        session.commit()

    
    response_data = {
        "success": True,
        "demande": document.toDict()
    }

    session.close()

    return jsonify(response_data), 200