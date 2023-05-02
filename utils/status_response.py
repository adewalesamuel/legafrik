from flask import jsonify


def success_response(message, data, status=200):

    response_data = {
        'message': message,
        'data': data,
        'status': status
    }

    return jsonify(response_data), status


def error_response(message, data, status=500):

    response_data = {
        'message': message,
        'data': data,
        'status': status
    }

    return jsonify(response_data), status

