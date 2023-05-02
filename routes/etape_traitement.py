from os import environ
from flask import Blueprint

from ..views import etape_traitement as etape_traitement_view
from ..utils import auth

from environs import Env

env = Env()
env.read_env()

etape_traitement = Blueprint('etape_traitement', __name__, 
url_prefix = environ['APP_API_PREFIX'] + '/admin/etape-traitements')

@etape_traitement.get('')
@auth.admin_token_required
@auth.can('view-any-etapetraitement')
def index(curent_admin): 
    return etape_traitement_view.index(curent_admin)

@etape_traitement.get('/<int:id>')
@auth.admin_token_required
@auth.can('view-any-etatetapetraitement')
def show(curent_admin, id): 
    return etape_traitement_view.show(curent_admin, id)

@etape_traitement.get('/<int:id>/etat-etape-traitements')
@auth.admin_token_required
@auth.can('view-any-etatetapetraitement')
def get_etat_etape_traitements(curent_admin, id): 
    return etape_traitement_view.get_etat_etape_traitements(curent_admin, id)

@etape_traitement.post('')
@auth.admin_token_required
@auth.can('create-etapetraitement')
def store(current_admin): 
    return etape_traitement_view.store(current_admin)

@etape_traitement.put('/<int:id>')
@auth.admin_token_required
@auth.can('update-etapetraitement')
def update(current_admin, id): 
    return etape_traitement_view.update(current_admin, id)

@etape_traitement.delete('/<int:id>')
@auth.admin_token_required
@auth.can('delete-etapetraitement')
def delete(current_admin, id): 
    return etape_traitement_view.delete(current_admin, id)

