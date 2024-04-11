from flask import Flask, request, jsonify
import os
import glob

app = Flask(__name__)

# Determine the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ensure the path is within the allowed directories
def is_safe_path(base_path, path, follow_symlinks=True):
    if follow_symlinks:
        return os.path.realpath(path).startswith(base_path)
    return os.path.abspath(path).startswith(base_path)

@app.route('/files/create', methods=['POST'])
def create_file():
    path = os.path.join(BASE_DIR, request.json.get('path'))
    content = request.json.get('content', '')
    if is_safe_path(BASE_DIR, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as file:
            file.write(content)
        return jsonify({"message": "File created successfully."}), 200
    return jsonify({"error": "Invalid file path."}), 400

@app.route('/files/delete', methods=['POST'])
def delete_file():
    path = os.path.join(BASE_DIR, request.json.get('path'))
    if is_safe_path(BASE_DIR, path) and os.path.exists(path):
        os.remove(path)
        return jsonify({"message": "File deleted successfully."}), 200
    return jsonify({"error": "File not found or invalid path."}), 404

@app.route('/files/update', methods=['POST'])
def update_file():
    path = os.path.join(BASE_DIR, request.json.get('path'))
    content = request.json.get('content')
    if is_safe_path(BASE_DIR, path) and os.path.exists(path):
        with open(path, 'w') as file:
            file.write(content)
        return jsonify({"message": "File updated successfully."}), 200
    return jsonify({"error": "File not found or invalid path."}), 404

@app.route('/directory/structure', methods=['GET'])
def get_directory_structure():
    sub_path = request.args.get('path', '')
    path = os.path.join(BASE_DIR, sub_path)
    if is_safe_path(BASE_DIR, path):
        files = glob.glob(path + '/**', recursive=True)
        return jsonify({"files": files}), 200
    return jsonify({"error": "Invalid path."}), 400

@app.route('/directory/readall', methods=['GET'])
def read_all_from_directory():
    sub_path = request.args.get('path', '')
    path = os.path.join(BASE_DIR, sub_path)
    if is_safe_path(BASE_DIR, path):
        all_files_content = {}
        for filename in glob.iglob(path + '/**/*', recursive=True):
            if os.path.isfile(filename):
                with open(filename, 'r') as file:
                    all_files_content[filename.replace(BASE
