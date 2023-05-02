from os import environ
from flask import Blueprint

from ..views import piece as piece_view
from ..utils import auth

from environs import Env

env = Env()
env.read_env()

piece = Blueprint('piece', __name__, 
url_prefix = environ['APP_API_PREFIX'] + '/admin/pieces')

@piece.get('')
@auth.admin_token_required
@auth.can('view-any-piece')
def index(current_admin): 
    return piece_view.index(current_admin)

@piece.post('')
@auth.admin_token_required
@auth.can('create-piece')
def store(current_admin): 
    return piece_view.store(current_admin)

@piece.put('/<int:id>')
@auth.admin_token_required
@auth.can('update-piece')
def update(current_admin, id): 
    return piece_view.update(current_admin, id)

@piece.delete('/<int:id>')
@auth.admin_token_required
@auth.can('delete-piece')
def delete(current_admin, id): 
    return piece_view.delete(current_admin, id)

