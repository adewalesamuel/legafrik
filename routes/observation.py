from os import environ
from flask import Blueprint

from ..views import observation as observation_view
from ..utils import auth

from environs import Env

env = Env()
env.read_env()

observation = Blueprint('observation', __name__, 
url_prefix = environ['APP_API_PREFIX'] + '/admin/observations')

@observation.get('')
@auth.admin_token_required
@auth.can('view-any-observation')
def index(curent_admin): 
    return observation_view.index(curent_admin)

@observation.get('/<int:id>')
@auth.admin_token_required
@auth.can('view-any-bservation')
def show(curent_admin, id): 
    return observation_view.show(curent_admin, id)

@observation.post('')
@auth.admin_token_required
@auth.can('create-observation')
def store(current_admin): 
    return observation_view.store(current_admin)

@observation.put('/<int:id>')
@auth.admin_token_required
@auth.can('update-observation')
def update(current_admin, id): 
    return observation_view.update(current_admin, id)

@observation.delete('/<int:id>')
@auth.admin_token_required
@auth.can('delete-observation')
def delete(current_admin, id): 
    return observation_view.delete(current_admin, id)

