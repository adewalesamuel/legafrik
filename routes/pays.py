from os import environ
from flask import Blueprint

from ..views import pays as pays_view
from ..utils import auth

from environs import Env

env = Env()
env.read_env()

pays = Blueprint('pays', __name__, 
url_prefix = environ['APP_API_PREFIX'] + '/admin/pays')

@pays.get('')
@auth.admin_token_required
@auth.can('view-any-pays')
def index(current_admin): 
    return pays_view.index(current_admin)

@pays.post('')
@auth.admin_token_required
@auth.can('create-pays')
def store(current_admin): 
    return pays_view.store(current_admin)

@pays.put('/<int:id>')
@auth.admin_token_required
@auth.can('update-pays')
def update(current_admin, id): 
    return pays_view.update(current_admin, id)

@pays.delete('/<int:id>')
@auth.admin_token_required
@auth.can('delete-pays')
def delete(current_admin, id): 
    return pays_view.delete(current_admin, id)