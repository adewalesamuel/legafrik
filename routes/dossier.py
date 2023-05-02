from os import environ
from flask import Blueprint

from ..views import dossier as dossier_view
from ..utils import auth

from environs import Env

env = Env()
env.read_env()

dossier = Blueprint('dossier', __name__, 
url_prefix = environ['APP_API_PREFIX'] + '/admin/dossiers')

@dossier.get('')
@auth.admin_token_required
@auth.can('view-any-dossier')
def index(current_admin): 
    return dossier_view.index(current_admin)

@dossier.post('')
@auth.admin_token_required
@auth.can('create-dossier')
def store(current_admin): 
    return dossier_view.store(current_admin)

@dossier.put('/<int:id>')
@auth.admin_token_required
@auth.can('update-dossier')
def update(current_admin, id): 
    return dossier_view.update(current_admin, id)

@dossier.delete('/<int:id>')
@auth.admin_token_required
@auth.can('delete-dossier')
def delete(current_admin, id): 
    return dossier_view.delete(current_admin, id)

@dossier.get('/<int:id>/demandes')
@auth.admin_token_required
@auth.can('view-any-demande')
def get_demandes(current_admin, id): 
    return dossier_view.get_demandes(current_admin, id)


