import datetime

from sqlalchemy.orm import sessionmaker, scoped_session
from flask import request, jsonify
from marshmallow import ValidationError
from ..models import Admin, Article, CategorieArticle, ArticleCategorieArticle
from ..db import engine
from ..schemas import ArticleSchema, CategorieArticleSchema, ArticleCategorieArticleSchema

from environs import Env

env = Env()
env.read_env()

session = scoped_session(sessionmaker(bind=engine), scopefunc=request)


def index(current_admin: Admin):
    articles: Article = session.query(Article)\
        .filter(Article.deleted_at == None, 
        Article.is_status == True).order_by(Article.created_at.desc()).all()
    
    result = [row.toDict() for row in articles]

    response_data = {
        'success': True,
        'articles': result
    }

    session.close()

    return jsonify(response_data), 200


def show(current_admin: Admin, id: int):
    article = session.query(Article).filter(Article.deleted_at == None,
        Article.id == id).first()
    
    result = article.toDict()
    
    response_data = {
        "success": True,
        "article": result
    }

    session.close()

    return jsonify(response_data), 200


def store_article(current_admin: Admin):
    
    request_data = request.json
    article_schema = ArticleSchema()

    try:
        validated_data = article_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400

    try:
        article = Article(
            image_article = validated_data.image_article,
            titre_article = validated_data.titre_article,
            resume_article = validated_data.resume_article,
            is_status = validated_data.is_status,
            nom_auteur = validated_data.nom_auteur,
            photo_auteur = validated_data.photo_auteur,
            fonction_auteur = validated_data.fonction_auteur,
            url_article = validated_data.url_article
        )

        session.add(article)
        session.commit()
        session.refresh(article)

        article_categorie_article_schema = ArticleCategorieArticleSchema()

        try:
            validated_data_categorie = article_categorie_article_schema.load(request_data, session=session)
        except ValidationError as err:
            session.close()
            return jsonify(err.messages), 400

        article_categorie_article = ArticleCategorieArticle(
            article_id = article.id,
            categorie_article_id = validated_data_categorie.categorie_article_id
        )

        session.add(article_categorie_article)
        session.commit()
    except Exception as err:
        session.rollback()
        session.close()

        response_data = {
            'error': True,
            'message': str(err)
        }

        return jsonify(response_data), 500
    finally:
        session.close()
    
    response_data = {
        'success': True,
        'article': request_data
    }

    return jsonify(response_data), 200


def store_categorie(current_admin: Admin):
    request_data = request.json
    categorie_article_schema = CategorieArticleSchema()

    try:
        validated_data = categorie_article_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400

    
    try:
        categorie_article = CategorieArticle(
            libelle = validated_data.libelle,
            description = validated_data.description
        )

        session.add(categorie_article)
        session.commit()
    except Exception as err:
        session.rollback()
        session.close()

        response_data = {
            'error': True,
            'message': str(err)
        }

        return jsonify(response_data), 500
    finally:
        session.close()
    
    response_data = {
        'success': True,
        'article': request_data
    }

    return jsonify(response_data), 200


def update(current_admin: Admin, id: int):
    request_data = request.json
    article_schema = ArticleSchema()

    try:
        validated_data = article_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400
    
    try:
        article: Article = session.query(Article).get(id)

        article.image_article = validated_data.image_article,
        article.titre_article = validated_data.titre_article,
        article.resume_article = validated_data.resume_article,
        article.duree_article = validated_data.duree_article,
        article.is_status = validated_data.is_status,
        article.nom_auteur = validated_data.nom_auteur,
        article.photo_auteur = validated_data.photo_auteur,
        article.fonction_auteur = validated_data.fonction_auteur,
        article.url_article = validated_data.url_article

        session.commit()
    except Exception as err:
        session.rollback()
        session.close()

        response_data = {
            'error': True,
            'message': str(err)
        }

        return jsonify(response_data), 500
    finally:
        session.close()
    
    response_data = {
        'success': True,
        'article': request_data
    }

    return jsonify(response_data), 200


def delete(current_admin: Admin, id: int):    
    try:
        article: Article = session.query(Article).get(id)

        article.deleted_at = datetime.datetime.utcnow()

        session.commit()
    except Exception as err:
        session.rollback()
        session.close()

        response_data = {
            'error': True,
            'message': str(err)
        }

        return jsonify(response_data), 500
    finally:
        session.close()
    
    response_data = {
        'success': True
    }

    return jsonify(response_data), 200


def store_categorie(current_admin: Admin):
    request_data = request.json
    categorie_article_schema = CategorieArticleSchema()

    try:
        validated_data = categorie_article_schema.load(request_data, session=session)
    except ValidationError as err:
        session.close()
        return jsonify(err.messages), 400

    
    try:
        categorie_article = CategorieArticle(
            libelle = validated_data.libelle,
            description = validated_data.description
        )

        session.add(categorie_article)
        session.commit()
    except Exception as err:
        session.rollback()
        session.close()

        response_data = {
            'error': True,
            'message': str(err)
        }

        return jsonify(response_data), 500
    finally:
        session.close()
    
    response_data = {
        'success': True,
        'article': request_data
    }

    return jsonify(response_data), 200


def select_categorie(current_admin: Admin):
    categorie: CategorieArticle = session.query(CategorieArticle)\
        .filter(CategorieArticle.deleted_at == None, 
        CategorieArticle.is_status == True).order_by(CategorieArticle.created_at.desc()).all()
    
    result = [row.toDict() for row in categorie]

    response_data = {
        'success': True,
        'categories': result
    }

    session.close()

    return jsonify(response_data), 200


def index_categorie(current_admin: Admin):
    categorie: CategorieArticle = session.query(CategorieArticle)\
        .filter(CategorieArticle.deleted_at == None).order_by(CategorieArticle.created_at.desc()).all()
    
    result = [row.toDict() for row in categorie]

    response_data = {
        'success': True,
        'categories': result
    }

    session.close()

    return jsonify(response_data), 200
