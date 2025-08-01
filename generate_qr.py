# major_project: generate_qr.py
# Purpose: Generate encrypted QR code and save product info to mock blockchain

import qrcode
import json
from cryptography.fernet import Fernet

# Function to generate AES encryption key
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    print("AES Key generated and saved as 'secret.key'.")

# Function to load AES key
def load_key():
    return open("secret.key", "rb").read()

# Function to encrypt data
def encrypt_data(data, key):
    f = Fernet(key)
    return f.encrypt(data.encode())

# Function to generate QR code
def generate_qr(encrypted_data, filename):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(encrypted_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    print(f"QR Code saved as {filename}")

# Save product details to mock blockchain (local JSON)
def save_to_mock_blockchain(product_info, encrypted_data):
    record = {
        "product_id": product_info["product_id"],
        "manufacturer": product_info["manufacturer"],
        "batch_no": product_info["batch_no"],
        "encrypted_qr_data": encrypted_data.decode()
    }

    try:
        with open('mock_blockchain.json', 'r') as file:
            blockchain = json.load(file)
    except FileNotFoundError:
        blockchain = []

    blockchain.append(record)

    with open('mock_blockchain.json', 'w') as file:
        json.dump(blockchain, file, indent=4)

    print("Product registered in mock blockchain (major_project).")

# Main process
if __name__ == "__main__":
    try:
        key = load_key()
    except FileNotFoundError:
        generate_key()
        key = load_key()

    product_info = {
        "product_id": "ES_5676",
        "manufacturer": " mercedes ",
        "batch_no": "656B"
    }

    # Encrypt product info
    product_data = json.dumps(product_info)
    encrypted_product_data = encrypt_data(product_data, key)

    # Generate QR code
    generate_qr(encrypted_product_data, "product_qr.png")

    # Save to mock blockchain
    #save_to_mock_blockchain(product_info, encrypted_product_data)
