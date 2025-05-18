from flask import jsonify

def handle_error(message, status_code):
    return jsonify({"error": message}), status_code