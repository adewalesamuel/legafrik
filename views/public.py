from flask import jsonify
from ..utils import file

def upload_file():

    try:
        file_url = file.upload_file()

        if "error" in file_url:
            raise(file_url['message'])
    except Exception as err:
        response_data = {
            "error": True,
            "message": str(err)
        }

        return jsonify(response_data), 500

    return jsonify({
        "success": True,
        "file_url": file_url
    })