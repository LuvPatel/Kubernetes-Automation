from flask import Flask, request, jsonify
import os
import csv

app = Flask(__name__)
# Comment 2 for container 2
@app.route('/get-sum', methods=['POST'])
def get_product_sum():
    try:
        data = request.get_json()
        print("Received request data:", data)
        
        if 'file' not in data or 'product' not in data or not data['file']:
            print("Invalid JSON input.")
            return jsonify({"file": None, "error": "Invalid JSON input."}), 400

        file_name = data['file']
        file_path = os.path.join('/luv_PV_dir', file_name)
        print(f"Looking for file: {file_path}")

        if not os.path.isfile(file_path):
            print(f"File not found: {file_path}")
            return jsonify({'file': file_name, 'error': 'File not found.'}), 404

        with open(file_path, 'r') as file:
            first_line = file.readline().strip()
        
        if not first_line.startswith('product,amount'):
            return jsonify({'file': file_name, 'error': 'Input file not in CSV format.'}), 400
        

        with open(file_path, 'r') as file:
            csv_data = list(csv.DictReader(file))

            
        product_name = data['product']
        product_sum = 0
        print(f"Calculating sum for product: {product_name}")

        for row in csv_data:
            product = row['product']
            amount = int(row['amount'])
            if product == product_name:
                product_sum += amount
                print(f"Adding {amount} to sum. Current sum: {product_sum}")

        response = {
            'file': file_name,
            'sum': product_sum
        }
        print(f"Calculation complete. Response: {response}")
        return jsonify(response)

    except Exception as e:
        print(f"Exception in /get-sum: {e}")
        return jsonify({"file": data.get('file', None), 'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask application on port 6001...")
    app.run(host='0.0.0.0', port=6001)
