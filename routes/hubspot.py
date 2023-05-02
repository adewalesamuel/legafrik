from os import environ
from flask import Blueprint

from ..views import hubspot as hubspot_view
from ..utils import auth

from environs import Env

env = Env()
env.read_env()

hubspot = Blueprint('hubspot', __name__, url_prefix = environ['APP_API_PREFIX'])

@hubspot.post('/hubspot/leads')
@auth.user_token_required
def store_lead(current_user):
    return hubspot_view.store_lead(current_user)