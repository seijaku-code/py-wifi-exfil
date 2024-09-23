from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
import json

app = Flask(__name__)

# Use the same key as used for encryption
key = b'your-fernet-key-here'  # Replace with the actual key
cipher_suite = Fernet(key)

# Path to the file where you want to save the decrypted data
FILE_PATH = 'webhook_data.txt'

@app.route('/webhook', methods=['POST'])
def webhook_listener():
    if request.method == 'POST':
        encrypted_data = request.json.get('encrypted_data')
        
        # Decrypt the data
        decrypted_data = decrypt_data(encrypted_data)
        
        # Log the decrypted data into a file
        write_to_file(decrypted_data)

        return jsonify({"status": "success", "message": "Decrypted data received"}), 200

def decrypt_data(encrypted_data):
    decrypted_data = cipher_suite.decrypt(encrypted_data.encode('utf-8'))
    return json.loads(decrypted_data.decode('utf-8'))

def write_to_file(data):
    try:
        with open(FILE_PATH, 'a') as file:
            file.write(json.dumps(data, indent=4))
            file.write("\n")
        print("Decrypted data successfully written to file.")
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

