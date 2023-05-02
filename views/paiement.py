import datetime
import json

from sqlalchemy.orm import sessionmaker, scoped_session
from flask import request, jsonify
from marshmallow import ValidationError
from ..payment_gateways.stripe import Stripe
from ..models import Paiement  , TypePaiement, MoyenPaiement, Demande,\
    Admin, EtatDemande
from ..db import engine
from ..schemas import PaiementSchema

from environs import Env

env = Env()
env.read_env()

session = scoped_session(sessionmaker(bind=engine), scopefunc=request)


def index(current_admin: Admin):
    paiements = session.query(Paiement )\
        .join(TypePaiement, MoyenPaiement, Demande)\
        .filter(Paiement.deleted_at == None)\
        .order_by(Paiement.created_at.desc()).all()
    result = list()

    for paiement in paiements:
        type_paiement_dict = paiement.type_paiement.toDict()
        moyen_paiement_dict = paiement.moyen_paiement.toDict()
        demande_dict = paiement.demande.toDict()
        paiement_dict = paiement.toDict()

        paiement_dict['type_paiement'] = type_paiement_dict
        paiement_dict['moyen_paiement'] = moyen_paiement_dict
        paiement_dict['demande'] = demande_dict

        result.append(paiement_dict)

    response_data = {
        'success': True,
        'paiements': result
    }

    session.close()

    return jsonify(response_data), 200


def store(current_admin: Admin):
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
    # request_data = request.json
    # paiements_schema = PaiementSchema()

    # try:
    #     validated_data = paiements_schema.load(request_data, session=session)
    # except ValidationError as err:
    #     session.close()
    #     return jsonify(err.messages), 400
    
    # try:
    #     demande: Demande = session.query(Demande)\
    #         .filter(Demande.id == validated_data.demande_id).first()

    #     if (demande == None):
    #         raise Exception("demande not found")

    #     # Get code promo and calculate new montant
    #     paiement = Paiement(
    #         type_paiement_id = validated_data.type_paiement_id,
    #         moyen_paiement_id = validated_data.moyen_paiement_id,
    #         demande_id = validated_data.demande_id,
    #         montant = validated_data.montant, #replace with real amount
    #         status = "en-cours",
    #         code_promo_id = validated_data.code_promo_id,
    #         recu_paiement_url = "" #repalace with real reçu paiement
    #     )

    #     #Change etat paiement demande

    #     session.add(paiement)
    #     session.commit()
    # except Exception as err:
    #     session.rollback()
    #     session.close()

    #     response_data = {
    #         'error': True,
    #         'message': str(err)
    #     }

    #     return jsonify(response_data), 500
    # finally:
    #     session.close()
    
    # response_data = {
    #     'success': True,
    #     'paiement': request_data
    # }

    # return jsonify(response_data), 200


def update(current_admin: Admin, id: int):
    request_data = request.json
    paiements_schema = PaiementSchema()

    try:
        validated_data = paiements_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        paiement: Paiement  = session.query(Paiement).get(id)

        paiement.type_paiement_id = validated_data.type_paiement_id,
        paiement.moyen_paiement_id = validated_data.moyen_paiement_id,
        paiement.demande_id = validated_data.demande_id,
        paiement.montant = validated_data.montant, #replace with real amount
        paiement.recu_paiement_url = "" #replace with real reçu paiement

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


def delete(current_admin: Admin, id: int):    
    try:
        paiement: Paiement  = session.query(Paiement).get(id)

        paiement.deleted_at = datetime.datetime.utcnow()

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