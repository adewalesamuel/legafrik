from os import environ
from flask import Blueprint

from ..views import etat_etape_traitement as etat_etape_traitement_view
from ..utils import auth

from environs import Env

env = Env()
env.read_env()

etat_etape_traitement = Blueprint('etat_etape_traitement', __name__, 
url_prefix = environ['APP_API_PREFIX'] + '/admin/etat-etape-traitements')

@etat_etape_traitement.get('')
@auth.admin_token_required
@auth.can('view-any-etatetapetraitement')
def index(current_admin): 
    return etat_etape_traitement_view.index(current_admin)

@etat_etape_traitement.post('')
@auth.admin_token_required
@auth.can('create-etatetapetraitement')
def store(current_admin): 
    return etat_etape_traitement_view.store(current_admin)

@etat_etape_traitement.put('/<int:id>')
@auth.admin_token_required
@auth.can('update-etatetapetraitement')
def update(current_admin, id): 
    return etat_etape_traitement_view.update(current_admin, id)

@etat_etape_traitement.delete('/<int:id>')
@auth.admin_token_required
@auth.can('delete-etatetapetraitement')
def delete(current_admin, id): 
    return etat_etape_traitement_view.delete(current_admin, id)

