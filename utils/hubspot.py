from os import environ
from flask import current_app, jsonify

import requests
from environs import Env
from ..models import User
from ..utils import strings

env = Env()
env.read_env()

def create_contact(user: User):

    base_url = environ['HUBSPOT_API_URL']
    headers = {
        'Accept': 'application/json',
        'Content-type': 'application/json',
        'Authorization': 'Bearer {}'.format(environ['HUBSPOT_API_TOKEN'])
        }
    try:
        contact_response = requests.post(headers=headers, 
            url='{}/crm/v3/objects/contacts'.format(base_url),
            json={'properties': {
                "company": "Aucun",
                "email": user.email,
                "firstname": user.username,
                "lastname": "",
                "phone": user.numero_telephone,
                "website": "Aucun"
            }})

        if (contact_response.status_code >= 400):
            raise Exception(contact_response.json()['message'])


    except Exception as err:
        response_data = {
            "error": True,
            "message": str(err)
        }

        return jsonify(response_data), 400