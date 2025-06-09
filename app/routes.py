from flask import Blueprint, request, jsonify
from .models import Result
from . import db

main = Blueprint('main', __name__)

@main.route('/ping', methods=['GET'])
def ping():
    return jsonify({'status': 'ok'})

@main.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    
    if not data or 'name' not in data or 'score' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    
    try:
        score = int(data['score'])
    except ValueError:
        return jsonify({'error': 'Score must be an integer'}), 400
    
    new_result = Result(name=data['name'], score=score)
    db.session.add(new_result)
    db.session.commit()
    
    return jsonify({'message': 'Result added successfully'}), 201

@main.route('/results', methods=['GET'])
def get_results():
    results = Result.query.all()
    return jsonify([result.to_dict() for result in results])
