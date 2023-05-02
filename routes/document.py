from os import environ
from flask import Blueprint

from ..views import document as document_view
from ..utils import auth

from environs import Env

env = Env()
env.read_env()

document = Blueprint('document', __name__, 
url_prefix = environ['APP_API_PREFIX'] + '/admin/documents')

@document.get('')
@auth.admin_token_required
@auth.can('view-any-document')
def index(current_admin): 
    return document_view.index(current_admin)

@document.post('')
@auth.admin_token_required
@auth.can('create-document')
def store(current_admin): 
    return document_view.store(current_admin)

@document.put('/<int:id>')
@auth.admin_token_required
@auth.can('update-document')
def update(current_admin, id): 
    return document_view.update(current_admin, id)

@document.delete('/<int:id>')
@auth.admin_token_required
@auth.can('delete-document')
def delete(current_admin, id): 
    return document_view.delete(current_admin, id)



@document.post('/sup')
#@auth.admin_token_required
def send_document_sup_mail():
    return document_view.send_document_sup_mail()

