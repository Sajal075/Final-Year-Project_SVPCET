# major_project: verify_qr.py
# Purpose: Scan encrypted QR code, verify authenticity visually

import json
import cv2
from cryptography.fernet import Fernet
from tkinter import Tk, Label, Canvas
import time

# Load AES key
def load_key():
    return open("secret.key", "rb").read()

# Decrypt QR data
def decrypt_data(encrypted_data, key):
    f = Fernet(key)
    return f.decrypt(encrypted_data.encode()).decode()

# Read QR using OpenCV
def read_qr_opencv(filename):
    img = cv2.imread(filename)
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)
    if data:
        return data
    else:
        raise Exception("No QR code detected.")

# Match with mock blockchain
def verify_product(product_info):
    with open('mock_blockchain.json', 'r') as file:
        blockchain = json.load(file)

    for record in blockchain:
        if (record['product_id'] == product_info['product_id'] and
            record['manufacturer'] == product_info['manufacturer'] and
            record['batch_no'] == product_info['batch_no']):
            return True
    return False

# Show final verification result (green/red window)
def show_result_window(status, product_info):
    result_window = Tk()
    result_window.title("Verification Result")
    result_window.geometry("400x200")

    if status:
        result_window.configure(bg="green")
        msg = f"✅ AUTHENTIC PRODUCT\n\nProduct ID: {product_info['product_id']}"
    else:
        result_window.configure(bg="red")
        msg = "❌ FAKE PRODUCT DETECTED"

    label = Label(result_window, text=msg, font=("Arial", 16), fg="white", bg=result_window["bg"])
    label.pack(expand=True)

    result_window.mainloop()

# Scanning animation with progress bar
def show_scanning_bar(callback):
    window = Tk()
    window.title("Scanning QR")
    window.geometry("400x120")
    window.configure(bg="black")

    label = Label(window, text="🔍 Scanning...", font=("Arial", 18), fg="white", bg="black")
    label.pack(pady=10)

    canvas = Canvas(window, width=300, height=20, bg="white", bd=0, highlightthickness=0)
    canvas.pack(pady=10)
    bar = canvas.create_rectangle(0, 0, 0, 20, fill="lime")

    def animate_bar(i=0):
        if i <= 300:
            canvas.coords(bar, 0, 0, i, 20)
            window.after(25, animate_bar, i + 10)
        else:
            window.destroy()
            callback()

    animate_bar()
    window.mainloop()

# Main logic: full verification after animation
def main_verification():
    try:
        key = load_key()
        encrypted_qr_data = read_qr_opencv("product_qr.png")
        decrypted_data = decrypt_data(encrypted_qr_data, key)
        product_info = json.loads(decrypted_data)
        status = verify_product(product_info)
        show_result_window(status, product_info)
    except Exception as e:
        show_error(str(e))

# Show error window if scan/decrypt fails
def show_error(message):
    error_win = Tk()
    error_win.title("Error")
    error_win.geometry("400x150")
    error_win.configure(bg="darkred")

    label = Label(error_win, text="❌ Error Occurred", font=("Arial", 16), fg="white", bg="darkred")
    label.pack(pady=10)

    msg_label = Label(error_win, text=message, font=("Arial", 12), fg="white", bg="darkred", wraplength=380)
    msg_label.pack(pady=5)

    error_win.mainloop()

# Start
if __name__ == "__main__":
    show_scanning_bar(main_verification)
