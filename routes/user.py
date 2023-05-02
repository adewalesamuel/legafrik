from os import environ
from flask import Blueprint

from ..views import user as user_view
from ..utils import auth

from environs import Env

env = Env()
env.read_env()

user = Blueprint('user', __name__, url_prefix = environ['APP_API_PREFIX'])

@user.get('admin/users')
@auth.admin_token_required
@auth.can('view-any-user')
def index(current_admin): 
    return user_view.index(current_admin)

@user.get('admin/users/<int:id>')
@auth.admin_token_required
@auth.can('view-any-user')
def show(current_admin, id): 
    return user_view.show(current_admin, id) 
    
@user.post('admin/users')
@auth.admin_token_required
@auth.can('create-user')
def store(current_admin): 
    return user_view.store(current_admin)

@user.put('admin/users/<int:id>')
@auth.admin_token_required
@auth.can('update-user')
def update(current_admin, id): 
    return user_view.update(current_admin, id)

@user.delete('admin/users/<int:id>')
@auth.admin_token_required
@auth.can('delete-user')
def delete(current_admin, id): 
    return user_view.delete(current_admin, id)

@user.post('/register')
def register(): return user_view.register()

@user.post('/login')
def login(): return user_view.login()

@user.post('/logout')
def logout(): pass

@user.get('/user')
@auth.user_token_required
def current_user(current_user):
    return user_view.current_user(current_user)

@user.put('/user/profile')
@auth.user_token_required
def update_profile(current_user):
    return user_view.update_profile(current_user)

@user.put('/user/password')
@auth.user_token_required
def update_password(current_user): 
    return user_view.update_password(current_user)

@user.get('/user/dossier')
@auth.user_token_required
def get_dossier(current_user):
    return user_view.get_dossier(current_user)

@user.post('/user/dossiers')
@auth.user_token_required
def store_dossier(current_user):
    return user_view.store_dossier(current_user)

@user.post('/user/paiements')
@auth.user_token_required
def store_paiement(current_user): 
    return user_view.store_paiement(current_user)
    
@user.get('/user/demandes')
@auth.user_token_required
def get_demande(current_user):
    return user_view.get_demandes(current_user)

@user.get('/user/type-demandes/<int:id>/etape-traitements')
@auth.user_token_required
def get_etape_traitements_by_type_demande(current_user, id):
    return user_view.get_etape_traitements_by_type_demande(current_user, id)

@user.get('/user/type-demandes/<int:id>/type-documents')
@auth.user_token_required
def get_type_demande_type_documents(current_user, id):
    return user_view.get_type_demande_type_documents(current_user, id)

@user.get('/user/type-demandes/<int:id>/type-pieces')
@auth.user_token_required
def get_type_demande_type_pieces(current_user, id):
    return user_view.get_type_demande_type_pieces(current_user, id)

@user.get('/user/etape-traitements/<int:id>/etat-etape-traitements')
@auth.user_token_required
def get_etat_etape_traitements_by_etape_traitement(current_user, id):
    return user_view.get_etat_etape_traitements_by_etape_traitement(current_user, id)

@user.post('/user/demandes')
@auth.user_token_required
def store_demande(current_user):
    return user_view.store_demande(current_user)

@user.get('/user/demandes/<int:id>')
@auth.user_token_required
def show_demande(current_user, id):
    return user_view.show_demande(current_user, id)

@user.put('/user/demandes/<int:id>/champs-questionnaire')
@auth.user_token_required
def update_questionnaire(current_user, id):
    return user_view.update_questionnaire(current_user, id)

@user.put('/user/demandes/<int:id>/champs-etape-traitements')
@auth.user_token_required
def update_demande_champs_etape_traitements(current_user, id):
    return user_view.update_demande_champs_etape_traitements(current_user, id)

@user.put('/user/demandes/<int:id>/etape-traitement')
@auth.user_token_required
def update_demande_etape_traitement(current_user, id):
    return user_view.update_demande_etape_traitement(current_user, id)

@user.put('/user/demandes/<int:id>/champs-demande/capital-social')
@auth.user_token_required
def update_champs_demande_capital_social(current_user, id):
    return user_view.update_champs_demande_capital_social(current_user, id)

@user.get('/user/demandes/<int:id>/paiements')
@auth.user_token_required
def show_paiements_demande(current_user, id):
    return user_view.show_paiements_demande(current_user, id)

@user.get('/user/demandes/<int:id>/documents')
@auth.user_token_required
def get_demande_documents(current_user, id):
    return user_view.get_demande_documents(current_user, id)

@user.post('/user/demandes/<int:id>/end')
@auth.user_token_required
def end_demande(current_user, id):
    return user_view.end_demande(current_user, id)

@user.get('/user/demandes/<int:demande_id>/etape-traitements/<int:etape_traitement_id>/status-etat-traitement')
@auth.user_token_required
def show_status_etat_traitement(current_user, demande_id, 
etape_traitement_id):
    return user_view.show_status_etat_traitement(current_user, demande_id, etape_traitement_id)

@user.get('/user/messages')
@auth.user_token_required
def get_messages(current_user):
    return user_view.get_messages(current_user)

@user.post('/user/messages')
@auth.user_token_required
def store_message(current_user):
    return user_view.store_message(current_user)

@user.get('/user/demandes/<int:id>/pieces')
@auth.user_token_required
def get_pieces_by_demande_id(current_user, id):
    return user_view.get_pieces_by_demande_id(current_user, id)

@user.post('/user/pieces')
@auth.user_token_required
def store_piece(current_user):
    return user_view.store_piece(current_user)

@user.put('/user/pieces/<int:id>')
@auth.user_token_required
def update_piece(current_user, id):
    return user_view.update_piece(current_user, id)

@user.delete('/user/pieces/<int:id>')
@auth.user_token_required
def delete_piece(current_user, id):
    return user_view.delete_piece(current_user, id)

@user.post('/user/observations')
@auth.user_token_required
def store_observation(current_user): 
    return user_view.store_observation(current_user)

@user.post('/user/exist')
def user_exist(): return user_view.user_exist()

@user.post('/create/lead')
def store_lead(): return user_view.store_lead()

@user.post('/init/password')
def init_password(): return user_view.init_password()

@user.get('/user/articles')
def get_articles():
    return user_view.get_articles()