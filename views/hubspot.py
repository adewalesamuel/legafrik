from os import environ
import json

from sqlalchemy.orm import sessionmaker, scoped_session
from flask import request, jsonify
from marshmallow import ValidationError
import requests
from ..db import engine
from ..models import User, TypeDemande, Pays
from ..schemas import DemandeSchema
from ..utils import strings

from environs import Env

env = Env()
env.read_env()
session = scoped_session(sessionmaker(bind=engine), scopefunc=request)

def store_lead(current_user: User):
    request_data = request.json
    demande_schema = DemandeSchema()

    try:
        validated_data = demande_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400


    base_url = environ['HUBSPOT_API_URL']
    headers = {
        'Accept': 'application/json',
        'Content-type': 'application/json',
        'Authorization': 'Bearer {}'.format(environ['HUBSPOT_API_TOKEN'])
        }
    champs_demande = json.loads(request_data['champs_demande'])

    try:
        contact_response = requests.post(headers=headers, 
            url='{}/crm/v3/objects/contacts'.format(base_url),
            json={'properties': {
                "company": champs_demande.get('nom-entreprise'),
                "email": "{}¶{}".format( strings.get_random_string(4),
                current_user.email),
                "firstname": current_user.username,
                "lastname": "",
                "phone": current_user.numero_telephone,
                "website": ""
            }})

        if (contact_response.status_code >= 400):
            raise Exception(contact_response.json()['message'])


    except Exception as err:
        response_data = {
            "error": True,
            "message": str(err)
        }
        session.close()

        return jsonify(response_data), 400

    try:
        type_demande: TypeDemande = session.query(TypeDemande)\
        .filter(TypeDemande.id == validated_data.type_demande_id).first()
        pays: Pays = session.query(Pays).filter(Pays.id == validated_data.pays_id,
        Pays.deleted_at == None).first()

        company_response = requests.post(headers=headers, 
            url='{}/crm/v3/objects/companies'.format(base_url),
            json={'properties': {
                "city": '',
                "domain": champs_demande.get('domaine-action'),
                "industry": champs_demande.get('secteur-activite'),
                "name": champs_demande.get('nom-entreprise'),
                "phone": current_user.numero_telephone,
                "state": "",
                "type_de_la_demande": type_demande.libelle,
                "anteriorite_dans_la_ceeation_d_entreprise": champs_demande.get('a-entreprise'),
                "nombre_d_associes": champs_demande.get('nombre-associes'),
                "forme_juridique": "",
                "date_de_reception_idu": champs_demande.get('date-reception-certificat'),
                "element_a_proteger": champs_demande.get('protection'),
                "nom_pour_le_depot": champs_demande.get('nom-marque'),
                "proprietaire_de_la_marque": champs_demande.get('proprietaire'),
                "actuel_siege_social": champs_demande.get('siege-entreprise'),
                "capital_social": champs_demande.get('capital-social'),
                "identite_du_president": champs_demande.get('est-president'),
                "origine_de_la_demande__pays_": pays.libelle
            }})

        if (company_response.status_code >= 400):
            raise Exception(company_response.json()['message'])
        
    except Exception as err:
        response_data = {
            "error": True,
            "message": str(err)
        }
        session.close()

        return jsonify(response_data), 400
    
    try:
        association_response = requests.put(headers=headers, 
            url='{}/crm/v3/objects/companies/{}/associations/contact/{}/2'
            .format(base_url, company_response.json()['id'], 
            contact_response.json()['id']), json={})

        if (association_response.status_code >= 400):
            raise Exception(association_response.json()['message'])

    except Exception as err:
        response_data = {
            "error": True,
            "message": str(err)
        }
        session.close()

        return jsonify(response_data), 400

    response_data = {
        "success": True,
        "contact": contact_response.json(),
        "company": company_response.json(),
        "association": association_response.json()
    }
    session.close()

    return jsonify(response_data), 200
