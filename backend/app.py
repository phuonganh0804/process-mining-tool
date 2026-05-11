from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
from alpha_miner.alpha_algorithm import AlphaAlgorithm
from heuristic_miner.heuristic_mining import HeuristicMiner
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'xes'}

app = Flask(__name__)
CORS(app)  # allows direct API access outside of Vite proxy
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-fallback-key')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

RESULTS_FOLDER = os.path.join(BASE_DIR, 'static', 'results')
os.makedirs(RESULTS_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed, only .xes files accepted'}), 400

    algorithm = request.form.get('algorithm')
    if algorithm not in ('Alpha Algorithm', 'Heuristic Miner'):
        return jsonify({'error': 'Invalid algorithm selected'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    try:
        if algorithm == 'Alpha Algorithm':
            mining = AlphaAlgorithm(file_path)
            result_path = mining.get_petri_net()
        elif algorithm == 'Heuristic Miner':
            try:
                dependency = float(request.form.get('dependency'))
                and_threshold = float(request.form.get('and'))
                positive_observation = float(request.form.get('observation'))
                relative_to_best = float(request.form.get('relative'))
            except ValueError:
                return jsonify({'error': 'Heuristic parameters must be numbers'}), 400
            mining = HeuristicMiner(file_path, dependency, and_threshold, positive_observation, relative_to_best)
            result_path = mining.heuristic_net()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'result': result_path}), 200


@app.route('/api/result')
def result():
    path = request.args.get('path')
    if not path:
        return jsonify({'error': 'No path provided'}), 400

    abs_path = os.path.abspath(os.path.join(BASE_DIR, '..', path))

    if not os.path.exists(abs_path):
        return jsonify({'error': f'Result not found: {abs_path}'}), 404

    return send_file(abs_path, mimetype='image/svg+xml')


if __name__ == '__main__':
    app.run(debug=True)