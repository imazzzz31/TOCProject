# app.py
import logging
import json
from flask import Flask, render_template, request, jsonify
from modules.plagiarism_checker import PlagiarismChecker

app = Flask(__name__)

# -------------------------------
# 🔑 Google API Key and Search Engine ID
# -------------------------------
GOOGLE_API_KEY = "AIzaSyABwknD5VTYIAxdckzcGI8ZyUB4dOvGerU"      # Replace with your key
GOOGLE_CSE_ID = "60dbf464aba9e404a"        # Replace with your search engine ID

# -------------------------------
# Initialize plagiarism checker with Google API
# -------------------------------
plagiarism = PlagiarismChecker(google_api_key=GOOGLE_API_KEY, google_cse_id=GOOGLE_CSE_ID)

# -------------------------------
# Configure logging
# -------------------------------
logger = app.logger
logger.setLevel(logging.INFO)

def log_json(title, data):
    """Pretty-print JSON to console"""
    logger.info("%s:\n%s", title, json.dumps(data, indent=4, sort_keys=True))

# -------------------------------
# Routes
# -------------------------------
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/api/plagiarism_web', methods=['POST'])
def plagiarism_web_api():
    data = request.get_json()
    log_json("Received JSON input", data)  # Log the incoming request

    text_input = data.get('text_input', '').strip() if data else ''
    if not text_input:
        logger.warning("No text input provided")
        return jsonify({"error": "Please provide text input"}), 400

    try:
        # Check plagiarism via Google search
        result = plagiarism.check_web(text_input)
        log_json("Plagiarism check result", result)  # Log the result
        return jsonify({"status": "success", "result": result}), 200
    except Exception as e:
        logger.error("Error in plagiarism check: %s", e)
        return jsonify({"status": "error", "message": str(e)}), 500

# -------------------------------
# Run app
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)
