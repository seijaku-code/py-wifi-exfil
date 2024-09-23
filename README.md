# Flask Webhook Listener with Encrypted Wi-Fi Data Transmission

This project provides a simple Python-based system for securely collecting and transmitting Wi-Fi profile data, including SSIDs and passwords, from a Windows machine to a webhook server using Flask and Gunicorn. The data is encrypted with AES encryption (via the `cryptography` library) before being sent, ensuring secure transmission.

## Features
- **Wi-Fi Profile Collection**: Uses Windows `netsh` commands to gather Wi-Fi SSIDs and passwords stored on the local machine.
- **AES Encryption**: Encrypts the Wi-Fi data using symmetric AES encryption with the `cryptography` library to protect sensitive information.
- **Secure Webhook Transmission**: Sends the encrypted data to a Flask-based webhook server over HTTP.
- **Decryption on Webhook**: The webhook listener decrypts the received data and stores it in a log file.
- **Gunicorn Support**: The Flask app can be run with Gunicorn for better performance and production use.
- **Supervisor Integration**: The project is designed to be managed with Supervisor, allowing easy control of the Flask/Gunicorn process and ensuring auto-restart in case of failure.

## Installation

### Prerequisites
- Python 3.x
- `pip` (Python package installer)
- A Windows machine for Wi-Fi profile extraction
- Linux or Windows for running the Flask webhook listener

### Dependencies
- Flask
- Gunicorn (optional for production)
- `cryptography` for encryption
- `requests` for sending the data to the webhook

Install the dependencies:
```bash
pip install flask gunicorn cryptography requests
```

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/seijaku-code/py-wifi-exfil.git
   cd py-wifi-exfil
   ```

2. Generate a secret key for encryption (store this key securely):
   ```python
   from cryptography.fernet import Fernet
   print(Fernet.generate_key())
   ```

3. Save the generated key in a safe location for both the sender and the Flask listener.

4. Configure the Flask webhook listener:
   - Set the secret key in both the sender and the listener scripts for encryption/decryption.
   - Modify the file paths for logging, if necessary.

### Running the Sender (Wi-Fi Data Extraction and Encryption)

On the Windows machine, run the Python script to extract and send Wi-Fi profiles to the webhook:
```bash
python wifi_sender.py
```

This will gather the Wi-Fi profiles, encrypt them, and send the encrypted data to the Flask webhook listener.

### Running the Webhook Listener

1. To run the Flask app locally:
   ```bash
   python webhook_listener.py
   ```

2. For production, use Gunicorn:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 webhook_listener:app
   ```

3. (Optional) Use Supervisor to manage the Gunicorn process in the background:
   ```bash
   sudo supervisorctl start webhook_listener
   ```

### Logs

The decrypted Wi-Fi data is stored in a log file (`webhook_data.txt` by default) on the server receiving the webhook.

### Security Considerations
- **Key Management**: Ensure the encryption key is stored securely (environment variables, secure storage, etc.).
- **HTTPS**: Consider using HTTPS for secure communication between the sender and the webhook listener.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
