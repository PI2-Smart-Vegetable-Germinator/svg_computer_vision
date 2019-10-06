import os

from flask_cors import CORS

from flask import Blueprint
from flask import jsonify
from flask import request

from project.api.computer_vision.s3_utils import S3Utils
from werkzeug.utils import secure_filename

import json

computer_vision_blueprint = Blueprint('computer_vision', __name__)
CORS(computer_vision_blueprint)

@computer_vision_blueprint.route('/api/ping', methods=['GET'])
def ping():
    return jsonify({
        'response': 'pong!'
    }), 200

@computer_vision_blueprint.route('/api/submit_image', methods=['POST'])
def computer_vision():
    if 'file' not in request.files:
        return jsonify({
            'response': 'Image not found!',
        }), 404
    file = request.files['file']
    filename = secure_filename(file.filename)
    s3 = S3Utils()
    s3.upload_to_s3(file)
    return jsonify({
        'response': 'Image found!',
        'filename' : file.filename
    }), 200