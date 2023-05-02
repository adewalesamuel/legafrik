from os import environ
from sqlalchemy import create_engine


from environs import Env

env = Env()
env.read_env()

# Connexion à la base de données
host = environ.get('DB_HOSTNAME')
username = environ.get('DB_USERNAME')
password = environ.get('DB_PASSWORD')
database = environ.get('DATABASE')
engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}/{database}', 
echo = True, pool_size=100, max_overflow=0)
