import os

from flask_cors import CORS

from flask import Blueprint
from flask import jsonify
from flask import request

from project.api.computer_vision.s3_utils import S3Utils
from project.api.computer_vision.image_processing import ImageProcessing
from werkzeug.utils import secure_filename

import json, requests

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

    s3 = S3Utils()
    post_data = json.loads(request.form['json'])
    filename = '%s.jpg' % post_data['planting_id']
    s3.upload_to_s3(file, filename)

    response = {
        'response': 'Image submitted!',
        'filename' : filename
    }
    return jsonify(response), 200

@computer_vision_blueprint.route('/api/process_image_data', methods=['POST'])
def process_image_data():
    if 'file' not in request.files:
        return jsonify({
            'response': 'Image not found!',
        }), 404
    file = request.files['file']

    ip = ImageProcessing()
    img = ip.image_treatment(file)
    green_percentage = ip.green_percentage(img)
    sprouted_seedlings = 0
    if(ip.green_percentage(img)):
        sprouted_seedlings = ip.count_sprouted_seedlings(img)

    post_data = json.loads(request.form['json'])
    filename = '%s.jpg' % post_data['planting_id']

    data = {
        'sprouted_seedlings': sprouted_seedlings,
        'green_percentage': green_percentage,
        'planting_id' : post_data['planting_id']
    }

    response = requests.post('%s/api/image_processing_results' % os.getenv('SVG_GATEWAY_URI'), json=data)
    return jsonify(response.json()), response.status_code