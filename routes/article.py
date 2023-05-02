from os import environ
from flask import Blueprint

from ..views import article as article_view
from ..utils import auth

from environs import Env

env = Env()
env.read_env()

article = Blueprint('article', __name__, 
url_prefix = environ['APP_API_PREFIX'] + '/admin/articles')

@article.get('')
@auth.admin_token_required
#@auth.can('view-any-article')
def index(current_admin): 
    return article_view.index(current_admin)

@article.get('/<int:id>')
@auth.admin_token_required
#@auth.can('view-any-article-detail')
def show(current_admin, id): 
    return article_view.show(current_admin, id)

@article.post('')
@auth.admin_token_required
#@auth.can('create-article')
def store_article(current_admin): 
    return article_view.store_article(current_admin)

@article.put('/<int:id>')
@auth.admin_token_required
#@auth.can('update-article')
def update(current_admin, id): 
    return article_view.update(current_admin, id)

@article.delete('/<int:id>')
@auth.admin_token_required
#@auth.can('delete-article')
def delete(current_admin, id): 
    return article_view.delete(current_admin, id)

@article.post('/categorie')
@auth.admin_token_required
#@auth.can('create-article-categorie')
def store_categorie(current_admin): 
    return article_view.store_categorie(current_admin)

@article.get('/categorie')
@auth.admin_token_required
#@auth.can('view-any-article')
def index_categorie(current_admin): 
    return article_view.index_categorie(current_admin)

@article.get('/categorie/select')
@auth.admin_token_required
#@auth.can('view-any-article')
def select_categorie(current_admin): 
    return article_view.select_categorie(current_admin)

