import os
from environs import Env

env = Env()
env.read_env()

UPLOAD_FOLDER_PATH = os.path.join(os.getcwd(), 
os.getenv('APP_DIRECTORY'), 'static', 'uploads')
