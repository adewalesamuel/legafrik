from os import environ
from flask import Blueprint

from ..views import demande as demande_view
from ..utils import auth

from environs import Env

env = Env()
env.read_env()

demande = Blueprint('demande', __name__, 
url_prefix = environ['APP_API_PREFIX'] + '/admin/demandes')

@demande.get('')
@auth.admin_token_required
@auth.can('view-any-demande')
def index(current_admin): 
    return demande_view.index(current_admin)

@demande.get('/<int:id>')
@auth.admin_token_required
@auth.can('view-any-demande')
def show(current_admin, id): 
    return demande_view.show(current_admin, id)

@demande.post('')
@auth.admin_token_required
@auth.can('create-demande')
def store(current_admin): 
    return demande_view.store(current_admin)

@demande.put('/<int:id>')
@auth.admin_token_required
@auth.can('update-demande')
def update(current_admin, id): 
    return demande_view.update(current_admin, id)

@demande.put('/<int:id>/champs-questionnaire')
@auth.admin_token_required
@auth.can('update-demande')
def update_questionnaire(current_admin, id): 
    return demande_view.update_questionnaire(current_admin, id)

@demande.delete('/<int:id>')
@auth.admin_token_required
@auth.can('delete-demande')
def delete(current_admin, id): 
    return demande_view.delete(current_admin, id)

@demande.get('/<int:id>/paiements')
@auth.admin_token_required
@auth.can('view-any-paiement')
def get_paiements(current_admin, id): 
    return demande_view.get_paiements(current_admin, id)

@demande.get('/<int:id>/pieces')
@auth.admin_token_required
@auth.can('view-any-piece')
def get_pieces(current_admin, id): 
    return demande_view.get_pieces(current_admin, id)

@demande.get('/<int:id>/documents')
@auth.admin_token_required
@auth.can('view-any-document')
def get_documents(current_admin, id): 
    return demande_view.get_documents(current_admin, id)

@demande.get('/<int:id>/observations')
@auth.admin_token_required
@auth.can('view-any-observation')
def get_observations(current_admin, id): 
    return demande_view.get_observations(current_admin, id)

@demande.put('/<int:id>/etape-traitement')
@auth.admin_token_required
@auth.can('update-etapetraitement')
def update_etape_traitement(current_admin, id):
    return demande_view.update_etape_traitement(current_admin, id)

@demande.get('/<int:demande_id>/etape-traitements/<int:etape_traitement_id>/status-etat-traitement')
@auth.admin_token_required
@auth.can('view-any-statusetattraitement')
def show_status_etat_traitement(current_admin, demande_id, 
etape_traitement_id):
    return demande_view.show_status_etat_traitement(current_admin, demande_id, etape_traitement_id)

@demande.get('genarate/recap/pdf/<int:id>')
@auth.admin_token_required
@auth.can('view-any-demande')
def gen_recap_demande_pdf(current_admin, id): 
    return demande_view.gen_recap_demande_pdf(current_admin, id)