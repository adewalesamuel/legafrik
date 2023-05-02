from os import environ
from flask import Flask

from flask_cors import CORS
from .routes.user import user as user_routes
from .routes.categorie_user import categorie_user as categorie_user_routes
from .routes.type_demande import type_demande as type_demande_routes
from .routes.pays import pays as pays_routes
from .routes.etat_demande import etat_demande as etat_demande_routes
from .routes.etape_traitement import etape_traitement as etape_traitement_routes
from .routes.type_paiement import type_paiement as type_paiement_routes
from .routes.moyen_paiement import moyen_paiement as moyen_paiement_routes
from .routes.dossier import dossier as dossier_routes
from .routes.demande import demande as demande_routes
from .routes.type_document import type_document as type_document_routes
from .routes.etat_document import etat_document as etat_document_routes
from .routes.document import document as document_routes
from .routes.admin import admin as admin_routes
from .routes.type_piece import type_piece as type_piece_routes
from .routes.role import role as role_routes
from .routes.piece import piece as piece_routes
from .routes.permission import permission as permission_routes
from .routes.message import message as message_routes
from .routes.paiement import paiement as paiement_routes
from .routes.code_promo import code_promo as code_promo_routes
from .routes.public import pub as public_routes
from .routes.hubspot import hubspot as hubspot_routes
from .routes.etat_etape_traitement import etat_etape_traitement as etat_etape_traitement_routes
from .routes.test import test as test_routes
from .routes.status_etat_traitement import status_etat_traitement as status_etat_traitement_routes
from .routes.observation import observation as observation_routes
from .routes.attribution import attribution as attribution_routes
from .routes.article import article as article_routes

from environs import Env

env = Env()
env.read_env()

# Initialisation de l'application FLask
app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = environ['MAIL_SERVER']
app.config['MAIL_PORT'] = environ['MAIL_PORT']
app.config['MAIL_USERNAME'] = environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = environ['MAIL_PASSWORD']
app.config['MAIL_USE_TLS'] = environ['MAIL_USE_TLS']
#app.config['MAIL_USE_SSL'] = environ['MAIL_USE_SSL']
CORS(app)

# Definitions des routes
app.register_blueprint(user_routes)
app.register_blueprint(categorie_user_routes)
app.register_blueprint(type_demande_routes)
app.register_blueprint(pays_routes)
app.register_blueprint(etat_demande_routes)
app.register_blueprint(etape_traitement_routes)
app.register_blueprint(type_paiement_routes)
app.register_blueprint(moyen_paiement_routes)
app.register_blueprint(dossier_routes)
app.register_blueprint(demande_routes)
app.register_blueprint(type_document_routes)
app.register_blueprint(etat_document_routes)
app.register_blueprint(document_routes)
app.register_blueprint(admin_routes)
app.register_blueprint(type_piece_routes)
app.register_blueprint(role_routes)
app.register_blueprint(piece_routes)
app.register_blueprint(permission_routes)
app.register_blueprint(message_routes)
app.register_blueprint(paiement_routes)
app.register_blueprint(code_promo_routes)
app.register_blueprint(public_routes)
app.register_blueprint(hubspot_routes)
app.register_blueprint(etat_etape_traitement_routes)
app.register_blueprint(test_routes)
app.register_blueprint(status_etat_traitement_routes)
app.register_blueprint(observation_routes)
app.register_blueprint(attribution_routes)
app.register_blueprint(article_routes)
