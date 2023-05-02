from os import environ
from flask import Blueprint

from ..views import type_piece as type_piece_view
from ..utils import auth

from environs import Env

env = Env()
env.read_env()

type_piece = Blueprint('type_piece', __name__, 
url_prefix = environ['APP_API_PREFIX'] + '/admin/type-pieces')

@type_piece.get('')
@auth.admin_token_required
@auth.can('view-any-typepiece')
def index(current_admin): 
    return type_piece_view.index(current_admin)

@type_piece.post('')
@auth.admin_token_required
@auth.can('create-typepiece')
def store(current_admin): 
    return type_piece_view.store(current_admin)

@type_piece.put('/<int:id>')
@auth.admin_token_required
@auth.can('update-typepiece')
def update(current_admin, id): 
    return type_piece_view.update(current_admin, id)

@type_piece.delete('/<int:id>')
@auth.admin_token_required
@auth.can('delete-typepiece')
def delete(current_admin, id): 
    return type_piece_view.delete(current_admin, id)

