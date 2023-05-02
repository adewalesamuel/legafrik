from os import environ
from flask import Blueprint

from ..views import public as public_view, etat_demande as etat_demande_view,\
moyen_paiement as moyen_paiement_view, pays as pays_view,\
type_demande as type_demande_view
from ..utils import mail

from environs import Env

env = Env()
env.read_env()

pub = Blueprint('public', __name__, url_prefix = environ['APP_API_PREFIX'])

@pub.post('upload-file')
def upload_file():
    return public_view.upload_file()

@pub.get('/etat-demandes')
def get_etat_demandes(current_admin = None): 
    return etat_demande_view.index(current_admin)

@pub.get('/moyen-paiements')
def get_moyen_paiements(current_admin = None): 
    return moyen_paiement_view.index(current_admin)

@pub.get('/pays')
def get_pays(current_admin = None): 
    return pays_view.index(current_admin)

@pub.get('/pays/<int:id>/type-demandes')
def get_pays_type_demandes(id): 
    return pays_view.get_type_demandes(id)

@pub.get('/type-demandes')
def gat_type_demandes(current_admin = None): 
    return type_demande_view.index(current_admin)

@pub.get('/type-demandes/<int:id>')
def show_type_demande(id): 
    return type_demande_view.show(id)

@pub.get("/test-mail")
def test_mail():
    try:
        mail.send_register_mail(None)
    except Exception as err:
        return str(err)

    return "OK"

@pub.get("/test-env")
def test_env():
    return str(environ)
