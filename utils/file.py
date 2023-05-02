import os
import uuid
from flask import request
from ..constants import UPLOAD_FOLDER_PATH
from . import s3_upload, status_response

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'pdf', 'docx']

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file_local():
    if 'file' not in request.files:
        return {"error": True, "message": "no file part"}

    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return {"error": True, "message": "no selected file"}

    if allowed_file(file.filename) is False:
        return {"error": True, "message": "file extension must be between ({})"
        .format(", ".join(ALLOWED_EXTENSIONS))}

    if allowed_file(file.filename):
        fileext = file.filename.rsplit('.', 1)[1].lower()
        new_filename = str(uuid.uuid4()).replace("-","") + f'.{fileext}'
        file_url = '{}/static/uploads/{}'.format(
            os.environ.get("APP_URL"), new_filename)

        file.save(os.path.join(UPLOAD_FOLDER_PATH, new_filename))

        return file_url

def upload_file():
    if 'file' not in request.files:
        return {"error": True, "message": "no file part"}

    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return {"error": True, "message": "no selected file"}

    if allowed_file(file.filename) is False:
        return {"error": True, "message": "file extension must be between ({})"
        .format(", ".join(ALLOWED_EXTENSIONS))}

    if allowed_file(file.filename):
        fileext = file.filename.rsplit('.', 1)[1].lower()
        new_filename = str(uuid.uuid4()).replace("-","") + f'.{fileext}'

        file_url = s3_upload.upload_gen_file_s3(file, 'legafrik', new_filename)

        return file_url