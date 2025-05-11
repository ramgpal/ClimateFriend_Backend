from flask import Flask, request, jsonify
import os
from fire import detect_objects  # Ensure 'fire.py' is accessible
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Directory where you want to save the files
UPLOAD_FOLDER = r'A:\Forest Fire-Smoke Detection\Result'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the directory exists

@app.route('/detect_media', methods=['POST'])
def detect_media():
    try:
        # Check if the file is part of the request
        if 'media' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['media']

        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        # Get the file name (from the frontend request)
        file_name = file.filename
        file_path = os.path.join(UPLOAD_FOLDER, file_name)

        # Save the uploaded file to the specified location
        file.save(file_path)

        print(f"File saved to: {file_path}")

        # Call the detection function
        detect_objects(file_path)

        # Optionally delete the file afterward if you no longer need it
        # os.remove(file_path)

        return jsonify({"message": "Detection completed successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
