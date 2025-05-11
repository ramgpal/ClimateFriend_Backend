from flask import Flask, request, jsonify
import os
from fire1 import detect_objects
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = r'A:\Forest Fire-Smoke Detection\Result'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/detect_media', methods=['POST'])
def detect_media():
    try:
        if 'media' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['media']

        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        file_name = file.filename
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        file.save(file_path)

        print(f"File saved to: {file_path}")

        # Call the detection function and get structured results
        detections = detect_objects(file_path)

        return jsonify({
            "message": "Detection completed successfully",
            "detections": detections
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
