from os import environ
from flask import Blueprint

from ..views import status_etat_traitement as status_etat_traitement_view
from ..utils import auth

from environs import Env

env = Env()
env.read_env()

status_etat_traitement = Blueprint('status_etat_traitement', __name__, 
url_prefix = environ['APP_API_PREFIX'] + '/admin/status-etat-traitements')

@status_etat_traitement.get('')
@auth.admin_token_required
@auth.can('view-any-statusetattraitement')
def index(current_admin): 
    return status_etat_traitement_view.index(current_admin)

@status_etat_traitement.post('')
@auth.admin_token_required
@auth.can('create-statusetattraitement')
def store(current_admin): 
    return status_etat_traitement_view.store(current_admin)

@status_etat_traitement.put('/<int:id>')
@auth.admin_token_required
@auth.can('update-statusetattraitement')
def update(current_admin, id): 
    return status_etat_traitement_view.update(current_admin, id)

@status_etat_traitement.delete('/<int:id>')
@auth.admin_token_required
@auth.can('delete-statusetattraitement')
def delete(current_admin, id): 
    return status_etat_traitement_view.delete(current_admin, id)

