from os import environ
from flask import Blueprint
from dotenv import load_dotenv
from ..views import test as test_view
from ..utils import mail

load_dotenv()

test = Blueprint('test', __name__, url_prefix = environ['APP_API_PREFIX'] + '/test')

@test.get('/all')
def get_all():
    return test_view.get_all()

@test.post('/upload')
def upload_test():
    return test_view.upload_test()

@test.post('/send/mail')
def send_mail_test():
    return test_view.send_mail_test()

@test.post('/generate/pdf')
def generate_pdf_test():
    return test_view.generate_pdf_test()

@test.post('/init/mail')
def init_mail_test():
    return test_view.init_mail_test()