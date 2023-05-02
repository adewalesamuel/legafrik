from os import environ
from flask import Blueprint

from ..views import type_demande as type_demande_view
from ..utils import auth

from environs import Env

env = Env()
env.read_env()

type_demande = Blueprint('type_demande', __name__, 
url_prefix = environ['APP_API_PREFIX'] + '/admin/type-demandes')

@type_demande.get('')
@auth.admin_token_required
@auth.can('view-any-typedemande')
def index(current_admin): 
    return type_demande_view.index(current_admin)

@type_demande.get('/<int:id>/etape-traitements')
@auth.admin_token_required
@auth.can('view-any-etapetraitement')
def get_etape_traitements(current_admin, id): 
    return type_demande_view.get_etape_traitements(current_admin, id)

@type_demande.get('/<int:id>/type-documents')
@auth.admin_token_required
@auth.can('view-any-typedocument')
def get_type_documents(current_admin, id):
    return type_demande_view.get_type_documents(current_admin, id)

@type_demande.get('/<int:id>/type-pieces')
@auth.admin_token_required
@auth.can('view-any-typepiece')
def get_type_pieces(current_admin, id):
    return type_demande_view.get_type_pieces(current_admin, id)

@type_demande.post('')
@auth.admin_token_required
@auth.can('create-typedemande')
def store(current_admin): 
    return type_demande_view.store(current_admin)

@type_demande.put('/<int:id>')
@auth.admin_token_required
@auth.can('update-typedemande')
def update(current_admin, id): 
    return type_demande_view.update(current_admin, id)

@type_demande.delete('/<int:id>')
@auth.admin_token_required
@auth.can('delete-typedemande')
def delete(current_admin, id): 
    return type_demande_view.delete(current_admin, id)