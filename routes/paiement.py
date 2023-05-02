from os import environ
from flask import Blueprint

from ..views import paiement as paiement_view
from ..utils import auth
from environs import Env

env = Env()
env.read_env()

paiement = Blueprint('paiement', __name__, 
url_prefix = environ['APP_API_PREFIX'] + '/admin/paiements')

@paiement.get('')
@auth.admin_token_required
@auth.can('view-any-paiement')
def index(current_admin): 
    return paiement_view.index(current_admin)

@paiement.post('')
@auth.admin_token_required
def store(current_admin): 
    return paiement_view.store(current_admin)

@paiement.put('/<int:id>')
@auth.admin_token_required
def update(current_admin, id): 
    return paiement_view.update(current_admin, id)

@paiement.delete('/<int:id>')
@auth.admin_token_required
def delete(current_admin, id): 
    return paiement_view.delete(current_admin, id)

