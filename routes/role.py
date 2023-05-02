from os import environ
from flask import Blueprint

from ..views import role as role_view
from ..utils import auth

from environs import Env

env = Env()
env.read_env()

role = Blueprint('role', __name__, 
url_prefix = environ['APP_API_PREFIX'] + '/admin/roles')

@role.get('')
@auth.admin_token_required
@auth.can('view-any-role')
def index(current_admin): 
    return role_view.index(current_admin)

@role.post('')
@auth.admin_token_required
@auth.can('create-role')
def store(current_admin): 
    return role_view.store(current_admin)

@role.put('/<int:id>')
@auth.admin_token_required
@auth.can('update-role')
def update(current_admin, id): 
    return role_view.update(current_admin, id)

@role.delete('/<int:id>')
@auth.admin_token_required
@auth.can('delete-role')
def delete(current_admin, id): 
    return role_view.delete(current_admin, id)

