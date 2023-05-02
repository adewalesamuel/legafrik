from os import environ
from flask import Blueprint

from ..views import etat_demande as etat_demande_view
from ..utils import auth

from environs import Env

env = Env()
env.read_env()

etat_demande = Blueprint('etat_demande', __name__, 
url_prefix = environ['APP_API_PREFIX'] + '/admin/etat-demandes')

@etat_demande.get('')
@auth.admin_token_required
@auth.can('view-any-etatdemande')
def index(current_admin): 
    return etat_demande_view.index(current_admin)

@etat_demande.post('')
@auth.admin_token_required
@auth.can('create-etatdemande')
def store(current_admin): 
    return etat_demande_view.store(current_admin)

@etat_demande.put('/<int:id>')
@auth.admin_token_required
@auth.can('update-etatdemande')
def update(current_admin, id): 
    return etat_demande_view.update(current_admin, id)

@etat_demande.delete('/<int:id>')
@auth.admin_token_required
@auth.can('delete-etatdemande')
def delete(current_admin, id): 
    return etat_demande_view.delete(current_admin, id)

