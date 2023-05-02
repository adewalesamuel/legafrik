from os import environ
from flask import Blueprint

from ..views import moyen_paiement as moyen_paiement_view
from ..utils import auth

from environs import Env

env = Env()
env.read_env()

moyen_paiement = Blueprint('moyen_paiement', __name__, 
url_prefix = environ['APP_API_PREFIX'] + '/admin/moyen-paiements')

@moyen_paiement.get('')
@auth.admin_token_required
@auth.can('view-any-moyenpaiement')
def index(current_admin): 
    return moyen_paiement_view.index(current_admin)

@moyen_paiement.post('')
@auth.admin_token_required
@auth.can('create-moyenpaiement')
def store(current_admin): 
    return moyen_paiement_view.store(current_admin)

@moyen_paiement.put('/<int:id>')
@auth.admin_token_required
@auth.can('update-moyenpaiement')
def update(current_admin, id): 
    return moyen_paiement_view.update(current_admin, id)

@moyen_paiement.delete('/<int:id>')
@auth.admin_token_required
@auth.can('delete-moyenpaiement')
def delete(current_admin, id): 
    return moyen_paiement_view.delete(current_admin, id)

