from os import environ
from flask import Blueprint

from ..views import message as message_view
from ..utils import auth

from environs import Env

env = Env()
env.read_env()

message = Blueprint('message', __name__, 
url_prefix = environ['APP_API_PREFIX'] + '/admin/messages')

@message.get('')
@auth.admin_token_required
@auth.can('view-any-message')
def index(current_admin): 
    return message_view.index(current_admin)

@message.post('')
@auth.admin_token_required
@auth.can('create-message')
def store(current_admin): 
    return message_view.store(current_admin)

@message.put('/<int:id>')
@auth.admin_token_required
@auth.can('update-message')
def update(current_admin, id): 
    return message_view.update(current_admin, id)

@message.delete('/<int:id>')
@auth.admin_token_required
@auth.can('delete-message')
def delete(current_admin, id): 
    return message_view.delete(current_admin, id)

