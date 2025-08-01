import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import qrcode
import cv2
from cryptography.fernet import Fernet
from PIL import Image, ImageTk
import os
from datetime import datetime

class BlockchainQRSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Blockchain QR Verification System")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a1a') # Basic background

        self.users = {"admin": "admin123", "user": "password", "manufacturer": "mfg2024"}
        self.current_user = None
        self.current_frame = None

        self.ensure_files_exist()
        self.show_login_page()
        self.root.mainloop()

    def ensure_files_exist(self):
        if not os.path.exists("secret.key"): self.generate_key()
        if not os.path.exists("mock_blockchain.json"):
            with open("mock_blockchain.json", "w") as f: json.dump([], f)

    def generate_key(self):
        with open("secret.key", "wb") as k_file: k_file.write(Fernet.generate_key())

    def load_key(self):
        return open("secret.key", "rb").read()

    def clear_frame(self):
        if self.current_frame: self.current_frame.destroy()

    def show_login_page(self):
        self.clear_frame()
        self.root.title("Login - Blockchain QR System")
        self.current_frame = tk.Frame(self.root, bg='#1a1a1a')
        self.current_frame.pack(fill="both", expand=True)

        l_frame = tk.Frame(self.current_frame, bg='#2d2d30', bd=2, relief="raised")
        l_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(l_frame, text="🔐 Blockchain QR System", font=("Arial", 20, "bold"), fg="#00ff88", bg='#2d2d30').pack(pady=20)
        tk.Label(l_frame, text="Username:", fg="white", bg='#2d2d30').pack(pady=(10,0))
        self.username_entry = tk.Entry(l_frame)
        self.username_entry.pack(pady=5)
        tk.Label(l_frame, text="Password:", fg="white", bg='#2d2d30').pack(pady=(10,0))
        self.password_entry = tk.Entry(l_frame, show="*")
        self.password_entry.pack(pady=5)
        tk.Button(l_frame, text="LOGIN", command=self.login, bg="#00ff88", fg="black").pack(pady=20)
        tk.Label(l_frame, text="Demo: admin/admin123, user/password, manufacturer/mfg2024", fg="#cccccc", bg='#2d2d30').pack(pady=(0,10))

        self.root.bind('<Return>', lambda e: self.login())
        self.username_entry.focus()

    def login(self):
        if self.username_entry.get() in self.users and self.users[self.username_entry.get()] == self.password_entry.get():
            self.current_user = self.username_entry.get()
            self.show_main_page()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials!")
            self.password_entry.delete(0, tk.END)

    def show_main_page(self):
        self.clear_frame()
        self.root.title(f"Welcome {self.current_user}")
        self.current_frame = tk.Frame(self.root, bg='#1a1a1a')
        self.current_frame.pack(fill="both", expand=True)

        header = tk.Frame(self.current_frame, bg='#2d2d30', height=60)
        header.pack(fill="x", padx=10, pady=(10,5))
        header.pack_propagate(False)
        tk.Label(header, text="🔗 Blockchain QR Verification", font=("Arial", 16, "bold"), fg="#00ff88", bg='#2d2d30').pack(side="left", padx=10)
        tk.Button(header, text="Logout", command=self.logout, bg="#ff4444", fg="white").pack(side="right", padx=10)
        tk.Label(header, text=f"User: {self.current_user}", fg="white", bg='#2d2d30').pack(side="right", padx=10)

        main_content = tk.Frame(self.current_frame, bg='#1a1a1a')
        main_content.pack(fill="both", expand=True, padx=10, pady=5)

        tk.Button(main_content, text="Generate QR", command=self.show_generate_qr, bg="#00ff88", fg="black", width=20, height=3).pack(pady=10)
        tk.Button(main_content, text="Verify QR", command=self.show_verify_qr, bg="#ff6b35", fg="white", width=20, height=3).pack(pady=10)

        stats_frame = tk.Frame(main_content, bg='#2d2d30', bd=1, relief="raised")
        stats_frame.pack(fill="x", pady=10)
        try:
            with open("mock_blockchain.json", "r") as f: blockchain = json.load(f)
            total_products = len(blockchain)
        except: total_products = 0
        tk.Label(stats_frame, text=f"Total Products: {total_products}", fg="white", bg='#2d2d30').pack(pady=5)

    def show_generate_qr(self):
        self.clear_frame()
        self.root.title("Generate QR Code")
        self.current_frame = tk.Frame(self.root, bg='#1a1a1a')
        self.current_frame.pack(fill="both", expand=True)

        header = tk.Frame(self.current_frame, bg='#2d2d30', height=50)
        header.pack(fill="x", padx=10, pady=(10,5))
        header.pack_propagate(False)
        tk.Button(header, text="← Back", command=self.show_main_page, bg="#666666", fg="white").pack(side="left", padx=10)
        tk.Label(header, text="📱 Generate QR Code", font=("Arial", 14, "bold"), fg="#00ff88", bg='#2d2d30').pack(side="left", padx=10)

        gen_frame = tk.Frame(self.current_frame, bg='#2d2d30', bd=2, relief="raised")
        gen_frame.pack(pady=20, padx=50, fill="both", expand=True)

        tk.Label(gen_frame, text="Product ID:", fg="white", bg='#2d2d30').pack(pady=(10,0))
        self.product_id_entry = tk.Entry(gen_frame)
        self.product_id_entry.pack(pady=5)
        tk.Label(gen_frame, text="Manufacturer:", fg="white", bg='#2d2d30').pack(pady=(10,0))
        self.manufacturer_entry = tk.Entry(gen_frame)
        self.manufacturer_entry.pack(pady=5)
        tk.Label(gen_frame, text="Batch Number:", fg="white", bg='#2d2d30').pack(pady=(10,0))
        self.batch_no_entry = tk.Entry(gen_frame)
        self.batch_no_entry.pack(pady=5)

        tk.Button(gen_frame, text="GENERATE", command=self.generate_qr_code, bg="#00ff88", fg="black").pack(pady=20)

        self.qr_display_frame = tk.Frame(gen_frame, bg='#2d2d30')
        self.qr_display_frame.pack(pady=10)

    def generate_qr_code(self):
        p_id, mfg, b_no = self.product_id_entry.get().strip(), self.manufacturer_entry.get().strip(), self.batch_no_entry.get().strip()
        if not all([p_id, mfg, b_no]): messagebox.showerror("Error", "Fill all fields!"); return

        try:
            key = self.load_key()
            p_info = {"product_id": p_id, "manufacturer": mfg, "batch_no": b_no}
            enc_data = Fernet(key).encrypt(json.dumps(p_info).encode())

            qr = qrcode.QRCode(version=1, box_size=10, border=5); qr.add_data(enc_data); qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white"); img.save("product_qr.png")

            self.save_to_mock_blockchain(p_info, enc_data)
            self.display_qr_code()
            messagebox.showinfo("Success", f"QR generated for {p_id} and registered.")
        except Exception as e: messagebox.showerror("Error", f"Failed to generate QR: {str(e)}")

    def save_to_mock_blockchain(self, p_info, enc_data):
        record = {**p_info, "encrypted_qr_data": enc_data.decode(), "timestamp": datetime.now().isoformat(), "created_by": self.current_user}
        try:
            with open('mock_blockchain.json', 'r') as f: blockchain = json.load(f)
        except FileNotFoundError: blockchain = []
        blockchain.append(record)
        with open('mock_blockchain.json', 'w') as f: json.dump(blockchain, f, indent=4)

    def display_qr_code(self):
        for w in self.qr_display_frame.winfo_children(): w.destroy()
        try:
            qr_img = Image.open("product_qr.png").resize((150, 150), Image.Resampling.LANCZOS)
            self.qr_photo = ImageTk.PhotoImage(qr_img) # Keep reference
            tk.Label(self.qr_display_frame, image=self.qr_photo, bg='#2d2d30').pack(pady=5)
            tk.Label(self.qr_display_frame, text="QR Code Displayed", fg="#00ff88", bg='#2d2d30').pack()
        except Exception as e: tk.Label(self.qr_display_frame, text=f"Error: {str(e)}", fg="red", bg='#2d2d30').pack()

    def show_verify_qr(self):
        self.clear_frame()
        self.root.title("Verify QR Code")
        self.current_frame = tk.Frame(self.root, bg='#1a1a1a')
        self.current_frame.pack(fill="both", expand=True)

        header = tk.Frame(self.current_frame, bg='#2d2d30', height=50)
        header.pack(fill="x", padx=10, pady=(10,5))
        header.pack_propagate(False)
        tk.Button(header, text="← Back", command=self.show_main_page, bg="#666666", fg="white").pack(side="left", padx=10)
        tk.Label(header, text="🔍 Verify QR Code", font=("Arial", 14, "bold"), fg="#ff6b35", bg='#2d2d30').pack(side="left", padx=10)

        verify_frame = tk.Frame(self.current_frame, bg='#2d2d30', bd=2, relief="raised")
        verify_frame.pack(pady=20, padx=50, fill="both", expand=True)

        tk.Label(verify_frame, text="QR Code Verification", font=("Arial", 16, "bold"), fg="white", bg='#2d2d30').pack(pady=20)
        tk.Button(verify_frame, text="SCAN & VERIFY QR", command=self.verify_qr_code, bg="#ff6b35", fg="white", width=20, height=3).pack(pady=20)

        self.result_frame = tk.Frame(verify_frame, bg='#2d2d30')
        self.result_frame.pack(pady=10, fill="both", expand=True)

    def verify_qr_code(self):
        for w in self.result_frame.winfo_children(): w.destroy()
        tk.Label(self.result_frame, text="Scanning...", fg="#ffaa00", bg='#2d2d30').pack(pady=10)
        self.root.update()

        try:
            if not os.path.exists("product_qr.png"): raise Exception("QR code file not found.")
            img = cv2.imread("product_qr.png")
            data, _, _ = cv2.QRCodeDetector().detectAndDecode(img)
            if not data: raise Exception("No QR code detected.")

            key = self.load_key()
            dec_data = Fernet(key).decrypt(data.encode()).decode()
            p_info = json.loads(dec_data)

            is_auth = self.verify_product_in_blockchain(p_info)
            self.show_verification_result(is_auth, p_info)
        except Exception as e:
            for w in self.result_frame.winfo_children(): w.destroy()
            tk.Label(self.result_frame, text=f"❌ Error: {str(e)}", fg="red", bg='#2d2d30').pack(pady=10)

    def verify_product_in_blockchain(self, p_info):
        try:
            with open('mock_blockchain.json', 'r') as f: blockchain = json.load(f)
            for rec in blockchain:
                if (rec['product_id'] == p_info['product_id'] and
                    rec['manufacturer'] == p_info['manufacturer'] and
                    rec['batch_no'] == p_info['batch_no']): return True
            return False
        except: return False

    def show_verification_result(self, is_authentic, p_info):
        for w in self.result_frame.winfo_children(): w.destroy() # Clear scanning message
        if is_authentic:
            res_frame = tk.Frame(self.result_frame, bg="#006600")
            tk.Label(res_frame, text="✅ AUTHENTIC", fg="white", bg="#006600").pack(pady=5)
            tk.Label(res_frame, text=f"ID: {p_info['product_id']}\nMfg: {p_info['manufacturer']}", fg="white", bg="#006600").pack(pady=5)
        else:
            res_frame = tk.Frame(self.result_frame, bg="#cc0000")
            tk.Label(res_frame, text="❌ FAKE PRODUCT", fg="white", bg="#cc0000").pack(pady=5)
            tk.Label(res_frame, text="Not verified in blockchain!", fg="white", bg="#cc0000").pack(pady=5)
        res_frame.pack(pady=10, padx=10, fill="x")

    def logout(self):
        self.current_user = None
        self.show_login_page()

if __name__ == "__main__":
    app = BlockchainQRSystem()