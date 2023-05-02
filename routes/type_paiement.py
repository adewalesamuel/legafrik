from os import environ
from flask import Blueprint

from ..views import type_paiement as type_paiement_view
from ..utils import auth

from environs import Env

env = Env()
env.read_env()

type_paiement = Blueprint('type_paiement', __name__, 
url_prefix = environ['APP_API_PREFIX'] + '/admin/type-paiements')

@type_paiement.get('')
@auth.admin_token_required
@auth.can('view-any-typepaiement')
def index(current_admin): 
    return type_paiement_view.index(current_admin)

@type_paiement.post('')
@auth.admin_token_required
@auth.can('create-typepaiement')
def store(current_admin): 
    return type_paiement_view.store(current_admin)

@type_paiement.put('/<int:id>')
@auth.admin_token_required
@auth.can('update-typepaiement')
def update(current_admin, id): 
    return type_paiement_view.update(current_admin, id)

@type_paiement.delete('/<int:id>')
@auth.admin_token_required
@auth.can('delete-typepaiement')
def delete(current_admin, id): 
    return type_paiement_view.delete(current_admin, id)

