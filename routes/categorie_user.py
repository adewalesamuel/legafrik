from os import environ
from flask import Blueprint

from ..views import categorie_user as categorie_user_view
from ..utils import auth

from environs import Env

env = Env()
env.read_env()

categorie_user = Blueprint('categorie_user', __name__, 
url_prefix = environ['APP_API_PREFIX'] + '/admin/categorie-users')

@categorie_user.get('')
@auth.admin_token_required
@auth.can('view-any-categorieuser')
def index(current_admin): 
    return categorie_user_view.index(current_admin)

@categorie_user.post('')
@auth.admin_token_required
@auth.can('create-categorieuser')
def store(current_admin): 
    return categorie_user_view.store(current_admin)

@categorie_user.put('/<int:id>')
@auth.admin_token_required
@auth.can('update-categorieuser')
def update(current_admin, id): 
    return categorie_user_view.update(current_admin, id)

@categorie_user.delete('/<int:id>')
@auth.admin_token_required
@auth.can('delete-categorieuser')
def delete(current_admin, id): 
    return categorie_user_view.delete(current_admin, id)

