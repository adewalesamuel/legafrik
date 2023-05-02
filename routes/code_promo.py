from os import environ
from flask import Blueprint

from ..views import code_promo as code_promo_view
from ..utils import auth

from environs import Env

env = Env()
env.read_env()

code_promo = Blueprint('code_promo', __name__, 
url_prefix = environ['APP_API_PREFIX'] + '/admin/code-promos')

@code_promo.get('')
@auth.admin_token_required
@auth.can('view-any-codepromo')
def index(current_admin): 
    return code_promo_view.index(current_admin)

@code_promo.post('')
@auth.admin_token_required
@auth.can('create-codepromo')
def store(current_admin): 
    return code_promo_view.store(current_admin)

@code_promo.put('/<int:id>')
@auth.admin_token_required
@auth.can('update-codepromo')
def update(current_admin, id): 
    return code_promo_view.update(current_admin, id)

@code_promo.delete('/<int:id>')
@auth.admin_token_required
@auth.can('delete-codepromo')
def delete(current_admin, id): 
    return code_promo_view.delete(current_admin, id)

