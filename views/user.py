from os import environ
import datetime
import json
import jwt

from sqlalchemy import or_
from sqlalchemy.orm import sessionmaker, scoped_session, Query
from flask import request, jsonify
from marshmallow import ValidationError
from ..payment_gateways.stripe import Stripe
from ..models import User, Demande, Dossier, TypeDemande, EtatDemande,\
     EtapeTraitement, Message, Admin, Paiement, Piece, TypePiece, MoyenPaiement,\
        Pays, EtatEtapeTraitement, StatusEtatTraitement, Observation, Document,\
             EtatDocument, TypeDocument, Article
from ..db import engine
from ..schemas import UserSchema, LoginSchema, UpdateUserSchema, \
    UpdatePasswordSchema, DemandeSchema, DossierSchema, MessageSchema, \
        PieceSchema, PaiementSchema, ObservationSchema, ChampsQuestionnaireSchema,\
             UpdateDemandeEtapeTraitementSchema, ChampsEtapeTraitementSchema, InitPasswordSchema, \
                PaiementLeadSchema, ChampsDemandeCapitalSocialSchema
from ..utils import auth, mail, strings, status_response, data, hubspot

from environs import Env

env = Env()
env.read_env()

# session = scoped_session(sessionmaker(bind=engine), scopefunc=request)

session = scoped_session(sessionmaker(bind=engine), scopefunc=request)

def _get_user_dossier(user: User) -> Dossier:
    try:
        dossier: Dossier = session.query(Dossier).filter(
            Dossier.user_id == user.id, Dossier.deleted_at == None)\
                .first()

        if dossier == None:
            raise Exception('dossier not found')
        
        return dossier
    except Exception as err:
        raise Exception(str(err))

def index(current_admin: Admin):
    pays_id  = request.args.get('pays_id')
    users = session.query(User)
    
    if pays_id is not None:
        demandes = session.query(Demande).filter(
            Demande.pays_id == pays_id, Demande.deleted_at == None).all()
        dossiers_ids = [row.dossier_id for row in demandes]
        dossiers = session.query(Dossier).filter(
            Dossier.id.in_(dossiers_ids), Dossier.deleted_at == None).all()
        users_ids = [row.user_id for row in dossiers]
        users = users.filter(User.id.in_(users_ids))

    users = data.paginate(users.filter(User.deleted_at == None)\
        .order_by(User.created_at.desc()), page=request.args.get('page'))
    result = [row.toDict() for row in users['result']]

    response_data = {
        'success': True,
        'users': result,
        'current_page': users['page'],
        'size': users['pagesize'],
        'total': users['total']
    }

    session.close()

    return jsonify(response_data)


def index_attente(current_admin: Admin):
    pays_id = request.args.get('pays_id')
    users_query = session.query(User)

    if pays_id is not None:
        users_query = users_query.join(Dossier).join(Demande).filter(
            Demande.pays_id == pays_id, Demande.deleted_at == None,
            Dossier.deleted_at == None, User.deleted_at == None)

    users_query = users_query.order_by(User.created_at.desc())

    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    users = users_query.paginate(page=page, per_page=per_page).items

    result = [row.toDict() for row in users]
    response_data = {
        'success': True,
        'users': result
    }

    return jsonify(response_data)


def show(current_admin: Admin, id: int):
    user = session.query(User)\
        .filter(User.id == id).first()

    session.close()

    if (user is None):
        response_data = {
            "error": True,
            "message": "user not found"
        }

        return jsonify(response_data), 404
    
    response_data = {
        "success": True,
        "user": user.toDict()
    }

    return jsonify(response_data), 200


def store(current_admin: Admin):
    request_data = request.json
    user_schema = UserSchema()

    try:
        validated_data = user_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400

    try:        
        user = User(
            username = validated_data.username,
            email = validated_data.email,
            password = auth.hash_password(validated_data.password),
            numero_telephone = validated_data.numero_telephone,
            birthdate = validated_data.birthdate,
            sex = validated_data.sex,
            address = validated_data.address,
            profile_url = validated_data.profile_url
        )

        session.add(user)
        session.commit()
    except Exception as e:
        session.rollback()

        response_data = {
            'error': True,
            'message': e._message()
        }

        return jsonify(response_data), 500
    finally:
        session.close()

    response_data = {
        'success': True,
        'user': request_data
    }

    return jsonify(response_data), 200


def update(current_admin: Admin, id: int):
    request_data = request.json
    user_schema = UpdateUserSchema()

    try:
        validated_data = user_schema.load(request_data)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        user: User = session.query(User).get(id)

        user.username = validated_data['username']
        user.email = validated_data['email']
        user.numero_telephone = validated_data['numero_telephone']
        user.birthdate = validated_data['birthdate']
        user.sex = validated_data['sex']
        user.address = validated_data['address']
        user.profile_url = validated_data['profile_url']

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
        'user': request_data
    }

    return jsonify(response_data), 200


def delete(current_admin: Admin, id: int):
    try:
        type_paiement: User = session.query(User).get(id)

        type_paiement.deleted_at = datetime.datetime.utcnow()

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


def register():
    request_data = request.json
    user_schema = UserSchema()

    try:
        validated_data = user_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400

    try:        
        user = User(
            username = validated_data.username,
            numero_telephone = validated_data.numero_telephone,
            email = validated_data.email,
            password = auth.hash_password(validated_data.password)
        )

        session.add(user)
        session.commit()
        session.refresh(user)
        hubspot.create_contact(user)


        dossier = Dossier(
            user_id = user.id,
            numero_dossier = strings.get_random_string(),
        )

        session.add(dossier)
        session.commit()

        token = jwt.encode(
            {'user_id' : user.id, 
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=3)}, 
            environ['JWT_SECRET_KEY'], "HS256") 
        
        response_data = {
            'success': True,
            'user': user.toDict(),
            'token': token
        }

        mail.all_mail_data('mails/inscription_bo.html', 'Inscription sur votre tableau de bord', [user.email], user)
    except Exception as e:
        session.rollback()

        response_data = {
            'error': True,
            'message': e._message()
        }

        return jsonify(response_data), 500
    finally:
        session.close()


    return jsonify(response_data), 200


def login():
    request_data = request.json
    login_schema = LoginSchema()
    token = ''

    try:
        validated_data = login_schema.load(request_data)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400

    try:        
        user = session.query(User).filter(
            User.email == validated_data['email']).first()

        if (user is None):
            raise Exception("email or password incorrect")

        if (auth.is_password(validated_data['password'], user.password) is False):  
            raise Exception("email or password incorrect")   

        token = jwt.encode(
            {'user_id' : user.id, 
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=3)}, 
            environ['JWT_SECRET_KEY'], "HS256")   

    except Exception as e:
        response_data = {
            'error': True,
            'message': str(e)
        }

        return jsonify(response_data), 500
    finally:
        session.close()

    response_data = {
        'success': True,
        'user': user.toDict(),
        'token': token
    }

    return jsonify(response_data), 200


def logout():
    pass


def current_user(current_user: User):
    return jsonify({
        "success": True,
        "user": current_user.toDict()
    })


def update_profile(current_user: User):
    request_data = request.json
    user_schema = UpdateUserSchema()

    try:
        validated_data = user_schema.load(request_data)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        user: User = session.query(User).get(current_user.id)

        user.username = validated_data['username']
        user.email = validated_data['email']
        user.numero_telephone = validated_data['numero_telephone']
        user.birthdate = validated_data['birthdate']
        user.sex = validated_data['sex']
        user.address = validated_data['address']
        user.profile_url = validated_data['profile_url']

        session.commit()
    except ValidationError as err:
        session.rollback()

        response_data = {
            'error': True,
            'message': str(err)
        }

        return jsonify(response_data), 500
    finally:
        session.close()
    
    response_data = {
        'success': True,
        'user': request_data
    }

    return jsonify(response_data), 200


def update_password(current_user: User):
    request_data = request.json
    user_schema = UpdatePasswordSchema()

    try:
        validated_data = user_schema.load(request_data)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        user: User = session.query(User).get(current_user.id)
        
        user.password = auth.hash_password(validated_data['password'])

        session.commit()
    except ValidationError as err:
        session.rollback()

        response_data = {
            'error': True,
            'message': str(err)
        }

        return jsonify(response_data), 500
    finally:
        session.close()
    
    response_data = {
        'success': True,
        'user': request_data
    }

    return jsonify(response_data), 200


def get_dossier(current_user: User):
    dossier: Dossier = session.query(Dossier)\
        .filter(Dossier.deleted_at == None, 
        Dossier.user_id == current_user.id).first()

    response_data = {
        'success': True,
        'dossier': dossier.toDict()
    }

    session.close()

    return jsonify(response_data), 200


def store_dossier(current_user: User):
    request_data = request.json
    dossiers_schema = DossierSchema()

    try:
        validated_data = dossiers_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        dossier = Dossier(
            user_id = current_user.id,
            numero_dossier = validated_data.numero_dossier,
        )

        session.add(dossier)
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
        'dossier': request_data
    }

    return jsonify(response_data), 200

def get_demandes(current_user: User):
    dossier = _get_user_dossier(current_user)

    demandes = data.paginate(session.query(Demande)\
        .join(Dossier, TypeDemande, EtatDemande)\
        .filter(Demande.deleted_at == None, 
        Demande.dossier_id == dossier.id)\
        .order_by(Demande.updated_at.desc()), page=request.args.get('page'))
    result = list()


    for demande in demandes['result']:
        type_demande_dict = demande.type_demande.toDict()
        etat_demande_dict = demande.etat_demande.toDict()
        # etape_traitement_dict = demande.etape_traitement.toDict()
        demande_dict = demande.toDict()

        demande_dict['type_demande'] = type_demande_dict
        demande_dict['etat_demande'] = etat_demande_dict
        # demande_dict['etape_traitement'] = etape_traitement_dict

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


def get_etape_traitements_by_type_demande(current_user: User, id: int):
    etape_traitements = session.query(EtapeTraitement)\
        .filter(EtapeTraitement.deleted_at == None, 
        EtapeTraitement.type_demande_id == id)\
        .order_by(EtapeTraitement.created_at.asc()).all()
    result = [row.toDict() for row in etape_traitements]
    response_data = {
        'success': True,
        'etape_traitements': result
    }

    session.close()

    return jsonify(response_data), 200


def get_etat_etape_traitements_by_etape_traitement(current_user: User, id: int):
    etat_etape_traitements = session.query(EtatEtapeTraitement)\
        .filter(EtatEtapeTraitement.deleted_at == None, 
        EtatEtapeTraitement.etape_traitement_id == id)\
        .order_by(EtatEtapeTraitement.created_at.asc()).all()
    result = [row.toDict() for row in etat_etape_traitements]
    response_data = {
        'success': True,
        'etat_etape_traitements': result
    }

    session.close()

    return jsonify(response_data), 200


def show_status_etat_traitement(current_user: User, demande_id: int, etape_traitement_id: int):
    try:
        dossier = _get_user_dossier(current_user)

        demande = session.query(Demande).filter(Demande.id == demande_id,
        Demande.dossier_id == dossier.id, Demande.deleted_at == None)\
            .first()

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
    

def get_demande_documents(current_user: User, id: int):
    try:
        dossier = _get_user_dossier(current_user)
        demande = session.query(Demande).filter(Demande.id == id,
        Demande.dossier_id == dossier.id, Demande.deleted_at == None)\
            .first()


        if demande is None: 
            raise Exception("demande not found")

        etape_traitement_id  = request.args.get('etape_traitement_id')
        documents = session.query(Document)\
            .join(TypeDocument, EtatDocument, Demande)

        if etape_traitement_id is not None:
            documents = documents.filter(Document.etape_traitement_id == etape_traitement_id)

        documents = documents.filter(Document.demande_id == demande.id, 
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
    except Exception as err:
        session.close()

        response_data = {
            'success': True,
            'documents': str(err)
        }

        return jsonify(response_data), 500
    finally:
        session.close()

    response_data = {
        'success': True,
        'documents': result
    }

    return jsonify(response_data), 200


def get_type_demande_type_documents(current_user: User, id: int):
    type_documents = session.query(TypeDocument)\
        .filter(TypeDocument.deleted_at == None, 
        TypeDocument.type_demande_id == id)\
        .order_by(TypeDocument.created_at.desc()).all()
    result = [row.toDict() for row in type_documents]
    response_data = {
        'success': True,
        'type_documents': result
    }

    session.close()

    return jsonify(response_data), 200


def get_type_demande_type_pieces(current_user: User, id: int):
    type_pieces = session.query(TypePiece)\
        .filter(TypePiece.deleted_at == None,
        TypePiece.type_demande_id == id)\
        .order_by(TypePiece.created_at.desc()).all()
    result = [row.toDict() for row in type_pieces]
    response_data = {
        'success': True,
        'type_pieces': result
    }

    session.close()

    return jsonify(response_data), 200


def show_demande(current_user: User, id: int):
    try:
        dossier = _get_user_dossier(current_user)

        demande = session.query(Demande)\
            .join(Dossier, TypeDemande, EtatDemande)\
            .filter(Demande.deleted_at == None, Demande.id == id,
            Demande.dossier_id == dossier.id).first()
        
        if demande is None:
            raise Exception('demande not found')
        
        demande_dict = demande.toDict()
        demande_dict['dossier'] = demande.dossier.toDict()
        demande_dict['type_demande'] = demande.type_demande.toDict()
        demande_dict['etat_demande'] = demande.etat_demande.toDict()
        demande_dict['pays'] = demande.pays.toDict()
    except Exception as err:
        session.close()

        response_data = {
            "success": True,
            "demande": str(err)
        }

        return jsonify(response_data), 500

    response_data = {
        "success": True,
        "demande": demande_dict
    }

    session.close()

    return jsonify(response_data), 200


def show_paiements_demande(current_user: User, id: int):
    dossier = _get_user_dossier(current_user)

    demande = session.query(Demande)\
        .join(TypeDemande, Pays).filter(Demande.deleted_at == None, 
        Demande.id == id, Demande.dossier_id == dossier.id).first()
    
    if demande is None:
        response_data = {
            "error": True,
            "message": "demande not found"
        }

        session.close()

        return jsonify(response_data), 404

    paiements = session.query(Paiement).join(MoyenPaiement)\
        .filter(Paiement.demande_id == demande.id, Paiement.deleted_at == None)\
        .order_by(Paiement.created_at.asc()).all()
    result = list()

    for paiement in paiements:
        moyen_paiement_dict = paiement.moyen_paiement.toDict()
        paiement_dict = paiement.toDict()

        paiement_dict['moyen_paiement'] = moyen_paiement_dict

        result.append(paiement_dict)

    response_data = {
        "success": True,
        "paiements": result
    }

    session.close()

    return jsonify(response_data), 200


def store_demande(current_user: User):
    request_data = request.json
    demandes_schema = DemandeSchema()

    try:
        validated_data = demandes_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        etape_traitement = session.query(EtapeTraitement)\
            .filter(EtapeTraitement.deleted_at == None,
            EtapeTraitement.type_demande_id == validated_data.type_demande_id,
            EtapeTraitement.is_default == True).first()

        if (etape_traitement is None):
            raise Exception('etape de traitment not found')

        etat_demande = session.query(EtatDemande)\
            .filter(EtatDemande.deleted_at == None).first()

        if (etat_demande is None):
            raise Exception('etat demande not found')

        demande = Demande(
            dossier_id = validated_data.dossier_id,
            champs_demande = validated_data.champs_demande,
            type_demande_id = validated_data.type_demande_id,
            etape_traitement_id = etape_traitement.id,
            pays_id = validated_data.pays_id,
            etat_demande_id = etat_demande.id,
            numero_demande = strings.get_random_string(),
            montant_total = validated_data.montant_total
        )

        session.add(demande)
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


def end_demande(current_user: User, id: int):
    try:
        dossier: Dossier = _get_user_dossier(current_user)
        demande: Demande = session.query(Demande)\
            .filter(Demande.id == id,Demande.dossier_id == dossier.id,
                    Demande.deleted_at == None).first()

        if (demande is None):
            raise Exception('demande not found')
        
        search = "%{}%".format("Finalis")
        etat_demande: EtatDemande = session.query(EtatDemande)\
        .filter(EtatDemande.libelle.like(search)).first()
        demande.etat_demande_id = etat_demande.id

        session.commit()
    except Exception as err:
        session.rollback()
        session.close()

        response_data = {
            "error": True,
            "message": str(err)
        }

        return jsonify(response_data), 500
    finally:
        session.close()
    
    response_data = {
        "success": True
    }

    return jsonify(response_data), 200

def update_questionnaire(current_user: User, id: int):
    request_data = request.json
    champs_questionnaire_schema = ChampsQuestionnaireSchema()

    try:
        validated_data = champs_questionnaire_schema.load(
            request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400

    try:
        search = "%{}%".format("Ajout")
        demande: Demande = session.query(Demande).get(id)
        etape_traitement: EtapeTraitement = session.query(EtapeTraitement)\
            .filter(EtapeTraitement.libelle.like(search),
            EtapeTraitement.type_demande_id == demande.type_demande_id,
            EtapeTraitement.deleted_at == None).first()

        demande.champs_questionnaire = validated_data.champs_questionnaire

        if validated_data.champs_questionnaire != None:
            demande.etape_traitement_id = etape_traitement.id
        
        try:
            user = current_user.toDict()
            data = {
                "demande_id": id,
                "username": user['username']
            }
            string = demande.champs_demande
            json_objet = json.loads(string)

            mail.all_mail_data('mails/admins/notif_questionnaire.html', 'Mise à jour du questionnaire '+json_objet['nom-entreprise'], ['d.lemec93@gmail.com','contact@legafrik.com'], data)
        except Exception as e:
            print(e)

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


def update_demande_champs_etape_traitements(current_user: User, id: int):
    request_data = request.json
    champs_etape_traitements_schema = ChampsEtapeTraitementSchema()

    try:
        validated_data = champs_etape_traitements_schema.load(
            request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400

    try:
        demande: Demande = session.query(Demande).get(id)

        demande.champs_etape_traitements = validated_data.champs_etape_traitements

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

    string = validated_data.champs_etape_traitements
    json_objet = json.loads(string)


    user = current_user.toDict()
    data = {
        "demande_id": id,
        "username": user['username'],
        "choix_signature": json_objet['choix-signature'],
        "date_livraison_signature": json_objet['date-livraison-signature']
    }
    stringD = demande.champs_demande
    json_objet_d = json.loads(stringD)
    
    if(json_objet['choix-signature'] == 'bureaux' or json_objet['choix-signature'] == 'livraison'):
        try:
            mail.all_mail_data('mails/admins/notif_signateur.html', json_objet_d['nom-entreprise'] + 'est prêt pour signature', ['d.lemec93@gmail.com','contact@legafrik.com'], data)
        except Exception as e:
            print(e)
    elif(json_objet['choix-signature'] == 'Terminé'):
        try:
            mail.all_mail('mails/admins/choix_signature.html', 'Choix date signature ', ['d.lemec93@gmail.com','contact@legafrik.com'])
        except Exception as e:
            print(e)

    response_data = {
        'success': True,
        'demande': demande.toDict()
    }

    return jsonify(response_data), 200


def update_demande_etape_traitement(current_user: User, id: int):
    request_data = request.json
    demande_schema = UpdateDemandeEtapeTraitementSchema()

    try:
        validated_data = demande_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400

    try:
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
        user = current_user.toDict()
        data = {
            "demande_id": demande.id,
            "username": user['username']
        }
        string = demande.champs_demande
        json_objet = json.loads(string)
        if(etape_traitement.libelle == 'Signature des documents'):
            try:
                mail.all_mail_data('mails/admins/notif_signature.html', 'Notification signature de document de '+json_objet['nom-entreprise'], ['d.lemec93@gmail.com','contact@legafrik.com'], data)
            except Exception as e:
                print(e)
        elif(etape_traitement.libelle == 'Rédaction des documents'):
            try:
                mail.all_mail_data('mails/admins/notif_ajout_document.html', 'Notification ajout de document de '+json_objet['nom-entreprise'], ['d.lemec93@gmail.com','contact@legafrik.com'], data)
            except Exception as e:
                print(e)
        elif(etape_traitement.libelle == 'AAA'):
            try:
                mail.all_mail('mails/admins/ajout_observation.html', 'Une observation a été ajouté au dossier ', ['d.lemec93@gmail.com','contact@legafrik.com'])
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


def update_champs_demande_capital_social(current_user: User, id: int):
    request_data = request.json
    champs_demande_capital_social = ChampsDemandeCapitalSocialSchema()

    try:
        validated_data = champs_demande_capital_social.load(request_data)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400

    try:
        demande: Demande = session.query(Demande).get(id)

        if demande is None:
            raise Exception("demande not found")

        champs_demande = json.loads(demande.champs_demande)
        champs_demande['capital-social'] = validated_data['capital_social']

        demande.champs_demande = json.dumps(champs_demande)

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

    return jsonify(response_data)


def store_paiement(current_user: User):
    # TODO _get_user_dossier
    request_data = request.json
    paiements_schema = PaiementSchema()

    try:
        validated_data = paiements_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        demande: Demande = session.query(Demande)\
            .filter(Demande.id == validated_data.demande_id,
            Demande.deleted_at == None).first()

        if (demande == None):
            raise Exception("demande not found")
        
        montant_paye = 0

        if (demande.montant_paye != None):
            montant_paye = demande.montant_paye + validated_data.montant
        else:
            montant_paye = validated_data.montant

        demande.montant_paye = montant_paye

        session.commit()

        # Get code promo and calculate new montant
        paiement = Paiement(
            type_paiement_id = validated_data.type_paiement_id,
            moyen_paiement_id = validated_data.moyen_paiement_id,
            demande_id = validated_data.demande_id,
            montant =  validated_data.montant, #replace with real amount
            status = "en-cours",
            code_promo_id = validated_data.code_promo_id,
            recu_paiement_url = "" #repalace with real reçu paiement
        )

        moyen_paiement: MoyenPaiement = session.query(MoyenPaiement)\
            .filter(MoyenPaiement.id == validated_data.moyen_paiement_id).first()

        if (moyen_paiement == None):
            raise Exception("moyen paiement not found")

        if (moyen_paiement.libelle.find("Carte") > -1):
            stripe: Stripe = Stripe()
            payment_data = json.loads(request_data['payment_data'])
            data = dict()

            data['amount'] = validated_data.montant
            data['currency'] = payment_data['currency']
            data['source'] = payment_data['source']
            data['description'] = payment_data['description']

            stripe.make_payment(data)
        
        session.add(paiement)
        session.commit()
        session.refresh(paiement)

        search = "%{}%".format("En cours")
        etat_demande: EtatDemande = session.query(EtatDemande)\
            .filter(EtatDemande.libelle.like(search),
            EtatDemande.deleted_at == None).first()

        if (etat_demande == None):
            raise Exception('etat_demande not found')

        demande.etat_demande_id = etat_demande.id
        paiement.status = "en-cours"

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
        'paiement': request_data
    }

    return jsonify(response_data), 200


def get_messages(current_user: User):
    messages = session.query(Message)\
        .filter(Message.deleted_at == None,
        Message.type_message == request.args.get('type_message'), 
        or_(Message.receiver_id == current_user.id, 
        Message.sender_id == current_user.id))\
        .order_by(Message.created_at.desc()).all()
    result = [row.toDict() for row in messages]

    response_data = {
        'success': True,
        'messages': result
    }

    session.close()

    return jsonify(response_data), 200


def store_message(current_user: User):
    request_data = request.json
    messages_schema = MessageSchema()

    try:
        validated_data = messages_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        message = Message(
            sender_id = current_user.id,
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


def get_pieces_by_demande_id(current_user: User, id: int):
    #TODO: check if id belongs to user dossier _get_user_dossier
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


def store_piece(current_user: User):
    # TODO check if demande belongs to user _get_user_dossier
    request_data = request.json
    piece_schema = PieceSchema()

    try:
        validated_data = piece_schema.load(request_data, session=session)
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


def update_piece(current_user: User, id: int):
    request_data = request.json
    piece_schema = PieceSchema()

    try:
        validated_data = piece_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        piece: Piece = session.query(Piece).filter(Piece.id == id).first()
        
        piece.demande_id == validated_data.demande_id
        piece.type_piece_id = validated_data.type_piece_id,
        piece.piece_url = validated_data.piece_url,

        session.commit()
    except ValidationError as err:
        session.rollback()

        response_data = {
            'error': True,
            'message': str(err)
        }

        return jsonify(response_data), 500
    finally:
        session.close()
    
    response_data = {
        'success': True,
        'user': request_data
    }

    return jsonify(response_data), 200


def delete_piece(current_user: User, id: int):    
    try:
        piece: Piece = session.query(Piece).filter(
            Piece.id == id).first()

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


def store_observation(current_user: User):
    request_data = request.json
    observation_schema = ObservationSchema()

    try:
        validated_data = observation_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400

    
    try:
        current_user_dossier: Dossier = _get_user_dossier(current_user)
        demande: Demande = session.query(Demande).filter(
            Demande.dossier_id == current_user_dossier.id,
            Demande.id == validated_data.demande_id,
            Demande.deleted_at == None).first()

        if demande is None:
            raise Exception("demande not found")

        observation = Observation(
            demande_id = validated_data.demande_id,
            type_document_id = validated_data.type_document_id,
            content = validated_data.content,
            document_url = validated_data.document_url
        )

        session.add(observation)
        session.commit()

        try:
            #print(current_user.toDict())
            user = current_user.toDict()
            data = {
                "demande_id": validated_data.demande_id,
                "username": user['username']
            }
            string = demande.champs_demande
            json_objet = json.loads(string)

            mail.all_mail_data('mails/admins/ajout_observation.html', 'Une observation a été ajouté au dossier de '+json_objet['nom-entreprise'], ['d.lemec93@gmail.com','contact@legafrik.com'], data)
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
        'observation': request_data
    }

    return jsonify(response_data), 200


def store_lead():
    request_data = request.json
    demandes_schema = DemandeSchema()

    try:
        validated_data_demande = demandes_schema.load(request_data.get("demande"), session=session)
    except ValidationError as err:
        session.close()
        return status_response.error_response("Erreur de validation des données types demandes", err.messages)

    
    try:
        etape_traitement = session.query(EtapeTraitement)\
            .filter(EtapeTraitement.deleted_at == None,
            EtapeTraitement.type_demande_id == validated_data_demande.type_demande_id,
            EtapeTraitement.is_default == True).first()

        if (etape_traitement is None):
            raise Exception('Etape de traitment not found')

        etat_demande = session.query(EtatDemande)\
            .filter(EtatDemande.deleted_at == None).first()

        if (etat_demande is None):
            raise Exception('Etat demande not found')

    

        demande = Demande(
            dossier_id = validated_data_demande.dossier_id,
            champs_demande = validated_data_demande.champs_demande,
            type_demande_id = validated_data_demande.type_demande_id,
            etape_traitement_id = etape_traitement.id,
            pays_id = validated_data_demande.pays_id,
            etat_demande_id = etat_demande.id,
            montant_total = validated_data_demande.montant_total,
            numero_demande = strings.get_random_string()
        )

        session.add(demande)
        session.commit()
        session.refresh(demande)
    except Exception as err:
        session.rollback()

        response_data = {
            'error': True,
            'message': str(err)
        }
        session.close()
        return status_response.error_response("Erreur de création demande", response_data)
        

    #data_paie = request_data.get("paiements")

    if(request_data.get("paiements") is None):
        response_data = {
                'success': True,
                'demande': request_data
            }
    else:
        if(request_data.get("paiements")['moyen_paiement_id'] == 3):
            response_data = {
                'success': True,
                'paiement': request_data
            }
        else:

            paiements_schema = PaiementLeadSchema()

            try:
                validated_data_paiement = paiements_schema.load(request_data.get("paiements"), session=session)
            except ValidationError as err:
                session.close()
                return status_response.error_response("Erreur de validation des données type paiement", err.messages)
            

            try:
                demande: Demande = session.query(Demande)\
                    .filter(Demande.id == demande.id,
                    Demande.deleted_at == None).first()

                if (demande == None):
                    raise Exception("Demande not found")

                # Get code promo and calculate new montant
                paiement = Paiement(
                    type_paiement_id = validated_data_paiement.type_paiement_id,
                    moyen_paiement_id = validated_data_paiement.moyen_paiement_id,
                    demande_id = demande.id,
                    montant = validated_data_paiement.montant, #replace with real amount
                    status = "en-cours",
                    code_promo_id = validated_data_paiement.code_promo_id,
                    recu_paiement_url = "" #repalace with real reçu paiement
                )

                moyen_paiement: MoyenPaiement = session.query(MoyenPaiement)\
                    .filter(MoyenPaiement.id == validated_data_paiement.moyen_paiement_id).first()

                if (moyen_paiement == None):
                    raise Exception("Moyen paiement not found")

                if (moyen_paiement.libelle.find("Stripe") > -1):
                    stripe: Stripe = Stripe()

                    payment_data = json.loads(request_data['payment_data'])


                    data = dict()

                    data['amount'] = validated_data_paiement.montant
                    data['currency'] = payment_data['currency']
                    data['source'] = payment_data['source']
                    data['description'] = payment_data['description']

                    stripe.make_payment(data)
                
                session.add(paiement)
                session.commit()
                session.refresh(paiement)

                search = "%{}%".format("En cours")
                etat_demande: EtatDemande = session.query(EtatDemande)\
                    .filter(EtatDemande.libelle.like(search),
                    EtatDemande.deleted_at == None).first()

                if (etat_demande == None):
                    raise Exception('etat_demande not found')

                demande.etat_demande_id = etat_demande.id
                paiement.status = "en-cours"

                session.commit()
            except Exception as err:
                session.rollback()

                response_data_paiement = {
                    'error': True,
                    'message': str(err)
                }

                return status_response.error_response("Erreur de création paiement", response_data_paiement)
            finally:
                session.close()
            
            response_data = {
                'success': True,
                'paiement': request_data
            }

    session.close()
    return status_response.success_response("Lead enrégistré", response_data)


def user_exist():
    request_data = request.json

    user = session.query(User)\
            .filter(User.email == request_data.get("email"))\
            .first()
    
    if user is None:
        user_schema = UserSchema()

        try:
            validated_data = user_schema.load(request_data, session=session)
        except ValidationError as err:
            session.close()
            return status_response.success_response("Erreur de validation des données", {"user_id": 1, "dossier_id":1})

        try:        
            user = User(
                numero_telephone = validated_data.numero_telephone,
                username = validated_data.username,
                email = validated_data.email,
                password = auth.hash_password("LegafrikV3")
            )

            session.add(user)
            session.commit()
            session.refresh(user)

            dossier = Dossier(
                user_id = user.id,
                numero_dossier = strings.get_random_string(),
            )
            response_data = {
                "user_id" : dossier.user_id,
                "dossier_id" : dossier.id
            }

            session.add(dossier)
            session.commit()

            response_data = {
                "user_id" : dossier.user_id,
                "dossier_id" : dossier.id
            }
            try:
                mail.all_mail('mails/inscription_bo.html', 'Inscription sur votre tableau de bord', [user.email])
            except Exception as e:
                print(e)
            
            # mail.send_register_mail(user)
        except Exception as e:
            session.rollback()

            response_data = {
                'error': True,
                'message': e._message()
            }
            return status_response.success_response("Erreur d'enregistrement des données", {"user_id": 1, "dossier_id":1, "error":response_data})
    
        finally:
            session.close()
        
        

        return status_response.success_response("Compte créé", response_data)
    else:
        
        dossier = session.query(Dossier)\
                .filter(Dossier.user_id == user.id)\
                .first()
        session.close()
        return status_response.success_response("Compte existant", {"user_id":dossier.user_id, "dossier_id":dossier.id})
    


def init_password():
    request_data = request.json
    user_schema = InitPasswordSchema()
    token = ''

    try:
        validated_data = user_schema.load(request_data)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    token = validated_data['token']
    index_tiret = token.find("-")  # Trouver l'indice du premier tiret
    user_id = token[index_tiret+1:]  # Sélectionner les caractères après le tiret

    user = session.query(User)\
            .filter(User.id == user_id)\
            .first()

    if user is None:
        response_data = {
            'error': True,
            'message': str(err)
        }
        return status_response.error_response("Utilisateur inexistant", response_data)
    else:
        try:

            if (auth.is_password("LegafrikV3", user.password) is False):  
                raise Exception("Token expiré")
            
            user.password = auth.hash_password(validated_data['password'])
            session.commit()
            token = jwt.encode(
            {'user_id' : user.id, 
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=3)}, 
            environ['JWT_SECRET_KEY'], "HS256")
        except ValidationError as err:
            session.rollback()

            response_data = {
                'error': True,
                'message': str(err)
            }

            return jsonify(response_data), 500
        finally:
            session.close()

    response_data = {
        'success': True,
        'user': user.toDict(),
        'token': token
    }
    return status_response.success_response("Mot de passe initialisé", response_data)
    

def get_articles():
    articles: Article = session.query(Article)\
        .filter(Article.deleted_at == None, 
        Article.is_status == True).order_by(Article.created_at.desc()).all()
    
    result = [row.toDict() for row in articles]

    response_data = {
        'success': True,
        'articles': result
    }

    session.close()

    return jsonify(response_data), 200