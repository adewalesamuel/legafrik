from os import environ
from flask import Blueprint

from ..views import permission as permission_view
from ..utils import auth

from environs import Env

env = Env()
env.read_env()

permission = Blueprint('permission', __name__, 
url_prefix = environ['APP_API_PREFIX'] + '/admin/permissions')

@permission.get('')
@auth.admin_token_required
@auth.can('view-any-permission')
def index(current_admin): 
    return permission_view.index(current_admin)

@permission.post('')
@auth.admin_token_required
@auth.can('create-permission')
def store(current_admin): 
    return permission_view.store(current_admin)

@permission.put('/<int:id>')
@auth.admin_token_required
@auth.can('update-permission')
def update(current_admin, id): 
    return permission_view.update(current_admin, id)

@permission.delete('/<int:id>')
@auth.admin_token_required
@auth.can('delete-permission')
def delete(current_admin, id): 
    return permission_view.delete(current_admin, id)

