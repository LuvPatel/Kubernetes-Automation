from flask import Flask, request, jsonify
import os
import csv
import requests

app = Flask(__name__)

# Comment 1 for container 1
def save_file(filename, data):
    file_path = os.path.join('/luv_PV_dir', filename)
    data = data.replace(" ", "")
    try:
        with open(file_path, 'w') as file:
            file.write(data)
        print(f"File {filename} saved successfully.")
        return True
    except Exception as e:
        print(f"Error saving file {filename}: {e}")
        return False

@app.route('/store-file', methods=['POST'])
def store_file():
    try:
        data = request.get_json()
        print("Received request data:", data)

        if 'file' not in data or 'data' not in data:
            print("Invalid JSON input.")
            return jsonify({"file": None, "error": "Invalid JSON input."}), 400

        name = data['file']
        file_data = data['data']

        if save_file(name, file_data):
            print(f"File {name} stored successfully.")
            return jsonify({"file": name, "message": "Success."}), 200
        else:
            print(f"Error storing the file {name} to the storage.")
            return jsonify({"file": name, "error": "Error while storing the file to the storage."}), 500

    except Exception as e:
        print(f"Exception in /store-file: {e}")
        return jsonify({"file": data.get('file', None), 'error': str(e)}), 500

@app.route('/calculate', methods=['POST'])
def get_product_sum():
    data = request.get_json()
    try:
        print("Received request data for calculation:", data)
        response = requests.post('http://app2-service:6001/get-sum', json=data, headers={
            "Content-Type": "application/json"
        })
        print("Response from app2-service:", response.json())
        return jsonify(response.json())

    except Exception as e:
        print(f"Exception in /calculate: {e}")
        return jsonify({'file': data.get('file', None), 'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask application...")
    app.run(host='0.0.0.0', port=6000)
