from os import environ
import datetime
import json
import os
import jwt
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
from sqlalchemy import or_
from sqlalchemy.orm import sessionmaker, scoped_session
from flask import request, jsonify, current_app
from marshmallow import ValidationError
from ..payment_gateways.stripe import Stripe
from ..models import Role
from ..db import engine
from ..schemas import UserSchema
from ..utils import auth, mail, generate_pdf, s3_upload, status_response


load_dotenv()

# session = scoped_session(sessionmaker(bind=engine), scopefunc=request)

session = scoped_session(sessionmaker(bind=engine), scopefunc=request)


def get_all():
    return status_response.success_response('Test', {
        'success': True,
        'role': 'file.name'
    })

def upload_test():

    file = request.files['file']

    try:
        a = s3_upload.upload_file_s3(file, 'legafrik', file.filename)
        return status_response.success_response('Test', a)
    except NoCredentialsError:
        return status_response.error_response('Test', a)

def send_mail_test():
    request_data = request.json
    #print(request_data.get("subject"))
    response = mail.all_mail('mails/inscription_bo.html', 'Inscription BO', request_data.get("receivers"))
    return status_response.success_response('Mail Test', {
        'success': response,
        'role': 'file.name'
    })

def generate_pdf_test():
    request_data = request.json
    response = generate_pdf.gen_recap_demande_pdf(generate_pdf.optionsA4, request_data)

    return status_response.success_response('Generation', response)

def init_mail_test():
    request_data = request.json
    #print(request_data.get("subject"))
    response = mail.init_password_mail(request_data.get("subject"), request_data.get("receivers"), request_data.get("message"))
    return status_response.success_response('Mail Test', {
        'success': response,
        'role': 'file.name'
    })