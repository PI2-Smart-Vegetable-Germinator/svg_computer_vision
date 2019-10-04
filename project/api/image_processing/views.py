import os

from flask_cors import CORS

from flask import Blueprint
from flask import jsonify
from flask import request

from project.api.image_processing.s3_utils import S3Utils
from werkzeug.utils import secure_filename

import json

image_processing_blueprint = Blueprint('image_processing', __name__)
CORS(image_processing_blueprint)

@image_processing_blueprint.route('/api/submit_image', methods=['POST'])
def image_processing():
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
