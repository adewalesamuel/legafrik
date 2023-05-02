from os import environ
from flask import current_app, render_template
from flask_mail import Mail, Message

from ..models import StatusEtatTraitement, User, EtatEtapeTraitement, EtapeTraitement, Demande, Pays

from environs import Env

env = Env()
env.read_env()


# trouver un moyen d"envoyer de manière asynchrone. Ex: utilisaer Celery
def send_text_mail(subject: str, receivers: list, message: str):
    try:
        data = {
            "nom":"",
            "prenoms":"",
            "message":message,
            "confirm_email_url":"",
            "confirmation_token":""
        }
        
        mail = Mail(current_app)
        msg = Message(subject, sender = environ['MAIL_SENDER'], 
        recipients = receivers)
        #msg.body = message
        # msg.body = render_template('template.txt', **kwargs)
        msg.html = render_template('mails/test.html', data=data)
        # msg.html = f"<h2>Email Heading </h2>\n<p>Corps de l'e-mail</p><p><strong>Message : </strong>{message}</p>" 
        mail.send(msg)
    except Exception as err:
        raise Exception(str(err))


def send_register_mail(user: User):
    message = "Un nouvel utilisateur s'est inscris\n\n"
    message += f" Nom : {user.username}\n"
    message += f" Email : {user.email}\n"

    send_text_mail("Nouvelle inscription !", [environ['ADMIN_MAIL']], message)



def send_document_sup_mail(subject: str, receivers: list, datas: list):
    try:
        
        mail = Mail(current_app)
        msg = Message(subject, sender = environ['MAIL_SENDER'], 
        recipients = receivers)
        #msg.body = message
        # msg.body = render_template('template.txt', **kwargs)
        msg.html = render_template('mails/document_sup_mail.html', datas=datas)
        mail.send(msg)
    except Exception as err:
        raise Exception(str(err))
    

# trouver un moyen d"envoyer de manière asynchrone. Ex: utilisaer Celery
def init_password_mail(subject: str, receivers: list, message: str):
    try:
        data = {
            "app_url": environ.get('APP_URL_USER'),
            "parameter": "eyHl5dhf5fghgDDBBDVGGDZVZNb58dbHbddhbc85-"+message,
        }
        
        mail = Mail(current_app)
        msg = Message(subject, sender = environ['MAIL_SENDER'], 
        recipients = receivers)
        #msg.body = message
        # msg.body = render_template('template.txt', **kwargs)
        msg.html = render_template('mails/init_password.html', data=data)
        # msg.html = f"<h2>Email Heading </h2>\n<p>Corps de l'e-mail</p><p><strong>Message : </strong>{message}</p>" 
        mail.send(msg)
    except Exception as err:
        raise Exception(str(err))    



def all_mail(template: str, subject: str, receivers: list):
    data = {
        "app_url": environ['APP_URL_USER']
    }
    try:
        mail = Mail(current_app)
        msg = Message(subject, sender=(environ['MAIL_FROM_NAME'], environ['MAIL_SENDER']), 
        recipients = receivers)
        msg.html = render_template(template, data=data)
        mail.send(msg)
    except Exception as err:
        raise Exception(str(err))



def all_mail_data(template: str, subject: str, receivers: list, datas: dict):
    
    try:
        mail = Mail(current_app)
        msg = Message(subject, sender=(environ['MAIL_FROM_NAME'], environ['MAIL_SENDER']), 
        recipients = receivers)
        msg.html = render_template(template, data=datas)
        mail.send(msg)
    except Exception as err:
        raise Exception(str(err))



