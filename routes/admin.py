from os import environ
from flask import Blueprint

from ..views import admin as admin_view
from ..utils import auth

from environs import Env

env = Env()
env.read_env()

admin = Blueprint('admin', __name__, 
url_prefix = environ['APP_API_PREFIX'] + '/admin')

@admin.get('/admins')
@auth.admin_token_required
@auth.can('view-any-admin')
def index(current_admin):
    return admin_view.index(current_admin)

@admin.post('/login')
def login(): return admin_view.login()

@auth.admin_token_required
@auth.can('create-admin')
@admin.post('/admins')
def store(current_admin=None): 
    return admin_view.store(current_admin)

@admin.put('/admins/<int:id>')
@auth.admin_token_required
@auth.can('update-admin')
def update(current_admin, id): 
    return admin_view.update(current_admin, id)

@admin.delete('/admins/<int:id>')
@auth.admin_token_required
@auth.can('delete-admin')
def delete(current_admin, id): 
    return admin_view.delete(current_admin, id)

@admin.post('/logout')
def logout(): pass

@admin.get('/admin')
@auth.admin_token_required
def current_admin(current_admin):
    return admin_view.current_admin(current_admin)

@admin.put('/admin/profile')
@auth.admin_token_required
def update_profile(current_admin):
    return admin_view.update_profile(current_admin)

@admin.put('/admin/password')
@auth.admin_token_required
def update_password(current_admin): 
    return admin_view.update_password(current_admin)
