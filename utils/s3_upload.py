import boto3
from os import environ
from botocore.exceptions import NoCredentialsError

from environs import Env

env = Env()
env.read_env()

S3_ACCESS_KEY = environ.get('S3_ACCESS_KEY')
S3_SECRET_KEY = environ.get('S3_SECRET_KEY')

def upload_file_s3(local_file, bucket, filename):
    s3 = boto3.client('s3', aws_access_key_id=S3_ACCESS_KEY,
                      aws_secret_access_key=S3_SECRET_KEY)

    try:
        s3.upload_fileobj(local_file, bucket, filename)
        
        return "https://legafrik.s3.us-west-2.amazonaws.com/"+filename
    except FileNotFoundError:
        return "The file was not found"
    except NoCredentialsError:
        return "Credentials not available"


def upload_gen_file_s3(local_file, bucket, filename):
    s3 = boto3.client('s3', aws_access_key_id=S3_ACCESS_KEY,
                      aws_secret_access_key=S3_SECRET_KEY)

    try:
        s3.put_object(Body=local_file, Bucket=bucket, Key=filename)
        
        return "https://legafrik.s3.us-west-2.amazonaws.com/"+filename
    except FileNotFoundError:
        return "The file was not found"
    except NoCredentialsError:
        return "Credentials not available"