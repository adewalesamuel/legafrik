from os import environ
from flask import Blueprint

from ..views import type_document as type_document_view
from ..utils import auth

from environs import Env

env = Env()
env.read_env()

type_document = Blueprint('type_document', __name__, 
url_prefix = environ['APP_API_PREFIX'] + '/admin/type-documents')

@type_document.get('')
@auth.admin_token_required
@auth.can('view-any-typedocument')
def index(current_admin): 
    return type_document_view.index(current_admin)

@type_document.post('')
@auth.admin_token_required
@auth.can('create-typedocument')
def store(current_admin): 
    return type_document_view.store(current_admin)

@type_document.put('/<int:id>')
@auth.admin_token_required
@auth.can('update-typedocument')
def update(current_admin, id): 
    return type_document_view.update(current_admin, id)

@type_document.delete('/<int:id>')
@auth.admin_token_required
@auth.can('delete-typedocument')
def delete(current_admin, id): 
    return type_document_view.delete(current_admin, id)

