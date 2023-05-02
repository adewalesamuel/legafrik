from os import environ
from flask import Blueprint

from ..views import attribution as attribution_view
from ..utils import auth

from environs import Env

env = Env()
env.read_env()

attribution = Blueprint('attribution', __name__, 
url_prefix = environ['APP_API_PREFIX'] + '/admin/attributions')

@attribution.get('')
@auth.admin_token_required
@auth.can('view-any-attribution')
def index(current_admin): 
    return attribution_view.index(current_admin)

@attribution.get('/<int:id>')
@auth.admin_token_required
@auth.can('view-any-attribution')
def show(current_admin, id): 
    return attribution_view.show(current_admin, id)

@attribution.post('')
@auth.admin_token_required
@auth.can('create-attribution')
def store(current_admin): 
    return attribution_view.store(current_admin)

@attribution.put('/<int:id>')
@auth.admin_token_required
@auth.can('update-attribution')
def update(current_admin, id): 
    return attribution_view.update(current_admin, id)

@attribution.delete('/<int:id>')
@auth.admin_token_required
@auth.can('delete-attribution')
def delete(current_admin, id): 
    return attribution_view.delete(current_admin, id)

