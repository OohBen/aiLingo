import os
from pathlib import Path
from flask import Flask, request, jsonify

app = Flask(__name__)
BASE_DIR = Path('/home/oohben/aiLingo/backend/')
WHITELISTED_DIRS = {'tempfront/ailingo-frontend', 'aiLingo'}
IGNORED_DIRS = {'node_modules', '__pycache__','.venv'}

def is_within_whitelisted_dirs(file_path: Path):
    if any(ignored_dir in file_path.parts for ignored_dir in IGNORED_DIRS):
        return False
    # Only consider paths within whitelisted directories or their subdirectories
    return any(str(file_path).startswith(str(BASE_DIR / whitelisted)) for whitelisted in WHITELISTED_DIRS)

@app.route('/files/create', methods=['POST'])
def create_file():
    data = request.json
    file_path = BASE_DIR.joinpath(data.get('path', '')).resolve()
    if not is_within_whitelisted_dirs(file_path):
        return jsonify({"error": "Operation not allowed"}), 403
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(data.get('content', ''))
    return jsonify({"message": "File created successfully"}), 201

@app.route('/files/delete', methods=['DELETE'])
def delete_file():
    file_path = BASE_DIR.joinpath(request.args.get('path', '')).resolve()
    if not is_within_whitelisted_dirs(file_path):
        return jsonify({"error": "Operation not allowed"}), 403
    if file_path.exists():
        file_path.unlink()
        return jsonify({"message": "File deleted successfully"}), 200
    return jsonify({"error": "File not found"}), 404

@app.route('/directory/structure', methods=['GET'])
def directory_structure():
    structure = {"directories": [], "files": []}
    for whitelisted_dir in WHITELISTED_DIRS:
        dir_path = BASE_DIR / whitelisted_dir
        if dir_path.exists():
            for item in dir_path.rglob('*'):
                if item.is_dir() and is_within_whitelisted_dirs(item):
                    structure["directories"].append(str(item.relative_to(BASE_DIR)))
                elif item.is_file() and is_within_whitelisted_dirs(item):
                    structure["files"].append(str(item.relative_to(BASE_DIR)))
    
    return jsonify(structure), 200

@app.route('/directory/data', methods=['GET'])
def directory_data():
    data = {}
    for whitelisted_dir in WHITELISTED_DIRS:
        dir_path = BASE_DIR / whitelisted_dir
        if dir_path.exists():
            for item in dir_path.rglob('*'):
                if item.is_file() and is_within_whitelisted_dirs(item):
                    try:
                        data[str(item.relative_to(BASE_DIR))] = item.read_text()
                    except UnicodeDecodeError:
                        data[str(item.relative_to(BASE_DIR))] = "Error: Could not decode file content."
    
    return jsonify(data), 200

@app.route('/file', methods=['GET'])
def get_file():
    print(request.args)
    file_path = BASE_DIR.joinpath(request.args.get('path', '')).resolve()
    print(file_path)
    if not is_within_whitelisted_dirs(file_path):
        return jsonify({"error": "Access denied"}), 403
    if file_path.is_file():
        return jsonify({"content": file_path.read_text()}), 200
    return jsonify({"error": "File not found"}), 404

@app.route('/whitelisted-dirs', methods=['GET'])
def get_whitelisted_dirs():
    # Returns the list of whitelisted directories within the BASE_DIR
    dirs = {d for d in WHITELISTED_DIRS if (BASE_DIR / d).exists()}
    return jsonify(list(dirs)), 200

if __name__ == '__main__':
    app.run(debug=True)