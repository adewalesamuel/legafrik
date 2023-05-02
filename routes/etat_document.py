from os import environ
from flask import Blueprint

from ..views import etat_document as etat_document_view
from ..utils import auth

from environs import Env

env = Env()
env.read_env()

etat_document = Blueprint('etat_document', __name__, 
url_prefix = environ['APP_API_PREFIX'] + '/admin/etat-documents')

@etat_document.get('')
@auth.admin_token_required
@auth.can('view-any-etatdocument')
def index(current_admin): 
    return etat_document_view.index(current_admin)

@etat_document.post('')
@auth.admin_token_required
@auth.can('create-etatdocument')
def store(current_admin): 
    return etat_document_view.store(current_admin)

@etat_document.put('/<int:id>')
@auth.admin_token_required
@auth.can('update-etatdocument')
def update(current_admin, id): 
    return etat_document_view.update(current_admin, id)

@etat_document.delete('/<int:id>')
@auth.admin_token_required
@auth.can('delete-etatdocument')
def delete(current_admin, id): 
    return etat_document_view.delete(current_admin, id)

