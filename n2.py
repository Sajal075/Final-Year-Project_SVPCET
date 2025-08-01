import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
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

        self.colors = {
            'bg_primary': "#0f172a", 'bg_secondary': "#1e293b",
            'accent_1': "#38bdf8", 'accent_2': "#06b6d4",
            'text_primary': "#f1f5f9", 'text_secondary': "#94a3b8",
            'success': "#10b981", 'error': "#f43f5e",
            'button_back': "#475569", # Custom color for back button
            'activity_bg': "#334155" # Custom background for activity entries
        }
        self.root.configure(bg=self.colors['bg_primary'])

        self.users = {"admin": "admin123", "user": "password", "manufacturer": "mfg2024"}
        self.current_user = None
        self.current_frame = None

        # Store product info temporarily after QR generation, before registration
        self.last_generated_product_info = None
        self.last_generated_encrypted_data = None

        self.ensure_files_exist()
        self.show_login_page()

    def _get_color(self, key_or_hex, default_key=None):
        """Helper to get color from theme or return direct hex code."""
        if key_or_hex and key_or_hex.startswith('#'):
            return key_or_hex
        return self.colors.get(key_or_hex, self.colors.get(default_key, None))

    def _create_label(self, parent, text, font_size, font_weight="normal", color_key='text_primary', bg_key='bg_secondary', **kwargs):
        """Helper to create a Tkinter Label."""
        fg_color = self._get_color(color_key, 'text_primary')
        bg_color = self._get_color(bg_key, 'bg_secondary')

        return tk.Label(parent, text=text, font=("Arial", font_size, font_weight),
                        fg=fg_color, bg=bg_color, **kwargs)

    def _create_button(self, parent, text, command, font_size, font_weight="bold",
                        bg_key='accent_1', fg_key='bg_primary', width=None, height=None, **kwargs):
        """Helper to create a Tkinter Button."""
        bg_color = self._get_color(bg_key, 'accent_1')
        fg_color = self._get_color(fg_key, 'bg_primary')

        return tk.Button(parent, text=text, font=("Arial", font_size, font_weight),
                          bg=bg_color, fg=fg_color,
                          width=width, height=height, relief="flat", cursor="hand2", command=command, **kwargs)

    def _create_entry(self, parent, width, show=None, **kwargs):
        """Helper to create a Tkinter Entry."""
        return tk.Entry(parent, font=("Arial", 12), width=width,
                         show=show, bg=self._get_color('activity_bg', '#334155'), # Using a key for this too for consistency
                         fg=self.colors['text_primary'], relief="flat", bd=5, **kwargs)

    def ensure_files_exist(self):
        """Ensure required files exist"""
        if not os.path.exists("secret.key"): self.generate_key()
        if not os.path.exists("mock_blockchain.json"):
            with open("mock_blockchain.json", "w") as f: json.dump([], f)

    def generate_key(self):
        """Generate AES encryption key"""
        with open("secret.key", "wb") as key_file: key_file.write(Fernet.generate_key())

    def load_key(self):
        """Load AES key"""
        return open("secret.key", "rb").read()

    def clear_frame(self):
        """Clear current frame"""
        if self.current_frame: self.current_frame.destroy()

    def show_login_page(self):
        """Display login page"""
        self.clear_frame()
        self.root.title("Login - Blockchain QR System")

        self.current_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.current_frame.pack(fill="both", expand=True)

        login_frame = tk.Frame(self.current_frame, bg=self.colors['bg_secondary'], relief="raised", bd=2)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        self._create_label(login_frame, "🔐 Blockchain QR System", 24, "bold", color_key='accent_1', bg_key='bg_secondary').pack(pady=30, padx=50)
        self._create_label(login_frame, "Secure Product Authentication", 12, bg_key='bg_secondary', color_key='text_secondary').pack(pady=(0, 30))

        self._create_label(login_frame, "Username:", 12, bg_key='bg_secondary').pack(pady=(10, 5))
        self.username_entry = self._create_entry(login_frame, 25)
        self.username_entry.pack(pady=(0, 15))

        self._create_label(login_frame, "Password:", 12, bg_key='bg_secondary').pack(pady=(0, 5))
        self.password_entry = self._create_entry(login_frame, 25, show="*")
        self.password_entry.pack(pady=(0, 20))

        self._create_button(login_frame, "LOGIN", self.login, 12, width=20, height=2, bg_key='accent_1', fg_key='bg_primary').pack(pady=(10, 30))

        info_frame = tk.Frame(login_frame, bg=self.colors['bg_secondary'])
        info_frame.pack(pady=(0, 20))
        self._create_label(info_frame, "Demo Credentials:", 10, "bold", color_key='accent_2', bg_key='bg_secondary').pack()
        self._create_label(info_frame, "admin/admin123 | user/password | manufacturer/mfg2024", 9, bg_key='bg_secondary', color_key='text_secondary').pack()

        self.root.bind('<Return>', lambda e: self.login())
        self.username_entry.focus()

    def login(self):
        """Handle login authentication"""
        username, password = self.username_entry.get(), self.password_entry.get()
        if username in self.users and self.users[username] == password:
            self.current_user = username
            self.show_main_page()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password!")
            self.password_entry.delete(0, tk.END)

    def show_main_page(self):
        """Display main dashboard"""
        self.clear_frame()
        self.root.title(f"Blockchain QR System - Welcome {self.current_user}")

        self.current_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.current_frame.pack(fill="both", expand=True)

        header_frame = tk.Frame(self.current_frame, bg=self.colors['bg_secondary'], height=80)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        self._create_label(header_frame, "🔗 Blockchain QR Verification System", 20, "bold", color_key='accent_1', bg_key='bg_secondary').pack(side="left", pady=20, padx=20)

        user_frame = tk.Frame(header_frame, bg=self.colors['bg_secondary'])
        user_frame.pack(side="right", pady=20, padx=20)
        self._create_label(user_frame, f"Welcome, {self.current_user}", 12, bg_key='bg_secondary').pack(side="left", padx=(0, 10))
        self._create_button(user_frame, "Logout", self.logout, 10, bg_key='error', fg_key='text_primary').pack(side="right")

        content_frame = tk.Frame(self.current_frame, bg=self.colors['bg_primary'])
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        stats_frame = tk.Frame(content_frame, bg=self.colors['bg_secondary'], relief="raised", bd=1)
        stats_frame.pack(fill="x", pady=(0, 20))
        self._create_label(stats_frame, "📊 System Statistics", 14, "bold", color_key='accent_1', bg_key='bg_secondary').pack(pady=10)

        total_products = len(json.load(open("mock_blockchain.json", "r"))) if os.path.exists("mock_blockchain.json") else 0
        stats_info = tk.Frame(stats_frame, bg=self.colors['bg_secondary'])
        stats_info.pack(pady=(0, 15))
        self._create_label(stats_info, f"Total Registered Products: {total_products}", 12, bg_key='bg_secondary').pack(side="left", padx=20)
        self._create_label(stats_info, f"Current User: {self.current_user}", 12, bg_key='bg_secondary').pack(side="right", padx=20)

        buttons_frame = tk.Frame(content_frame, bg=self.colors['bg_primary'])
        buttons_frame.pack(expand=True)

        # Action buttons setup
        for text_title, text_desc, btn_text, btn_command, accent_key, side in [
            ("📱 Generate QR Code", "Create encrypted QR codes for products (Not yet registered in blockchain)", "GENERATE QR", self.show_generate_qr, 'accent_1', "left"),
            ("🔍 Verify QR Code", "Scan and verify QR codes to check\nproduct authenticity against blockchain", "VERIFY QR", self.show_verify_qr, 'accent_2', "right")
        ]:
            frame = tk.Frame(buttons_frame, bg=self.colors['bg_secondary'], relief="raised", bd=2)
            frame.pack(side=side, padx=20, pady=20, fill="both", expand=True)
            self._create_label(frame, text_title, 16, "bold", color_key=accent_key, bg_key='bg_secondary').pack(pady=20)
            self._create_label(frame, text_desc, 11, bg_key='bg_secondary', color_key='text_secondary', justify="center").pack(pady=10)
            # Determine fg_key for button based on accent_key
            btn_fg_key = 'bg_primary' if accent_key == 'accent_1' else 'text_primary'
            self._create_button(frame, btn_text, btn_command, 14, width=20, height=3, bg_key=accent_key, fg_key=btn_fg_key).pack(pady=20)

        activity_frame = tk.Frame(content_frame, bg=self.colors['bg_secondary'], relief="raised", bd=1)
        activity_frame.pack(fill="x", pady=(20, 0))
        self._create_label(activity_frame, "📋 Recent Activity", 14, "bold", color_key='accent_1', bg_key='bg_secondary').pack(pady=10)

        try:
            blockchain_data = json.load(open("mock_blockchain.json", "r"))
            recent_entries = blockchain_data[-3:] if blockchain_data else []
            if not recent_entries:
                self._create_label(activity_frame, "No recent activity", 10, bg_key='bg_secondary', color_key='text_secondary').pack(pady=10)
            else:
                for entry in reversed(recent_entries):
                    entry_frame = tk.Frame(activity_frame, bg=self.colors['activity_bg']) # Use the new key here
                    entry_frame.pack(fill="x", padx=20, pady=2)
                    # Pass color_key directly as 'text_primary' and bg_key as 'activity_bg'
                    self._create_label(entry_frame, f"Product: {entry['product_id']} | Manufacturer: {entry['manufacturer']} | Registered On: {datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d %H:%M')}", 10, color_key='text_primary', bg_key='activity_bg').pack(side="left", pady=5, padx=10)
        except Exception:
            self._create_label(activity_frame, "No recent activity", 10, bg_key='bg_secondary', color_key='text_secondary').pack(pady=10)
        activity_frame.pack(pady=(0, 20))

    def show_generate_qr(self):
        """Show QR generation interface"""
        self.clear_frame()
        self.root.title("Generate QR Code - Blockchain QR System")

        self.current_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.current_frame.pack(fill="both", expand=True)

        header_frame = tk.Frame(self.current_frame, bg=self.colors['bg_secondary'], height=60)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        self._create_button(header_frame, "← Back", self.show_main_page, 12, bg_key='button_back', fg_key='text_primary').pack(side="left", pady=15, padx=20)
        self._create_label(header_frame, "📱 Generate QR Code", 18, "bold", color_key='accent_1', bg_key='bg_secondary').pack(pady=15)

        form_frame = tk.Frame(self.current_frame, bg=self.colors['bg_secondary'], relief="raised", bd=2)
        form_frame.pack(pady=20, padx=100, fill="both", expand=True)

        self._create_label(form_frame, "Enter Product Information", 16, "bold", bg_key='bg_secondary').pack(pady=20)

        fields = [
            ("Product ID:", "product_id_entry"),
            ("Manufacturer:", "manufacturer_entry"),
            ("Batch Number:", "batch_no_entry")
        ]
        for label_text, entry_attr in fields:
            self._create_label(form_frame, label_text, 12, bg_key='bg_secondary').pack(pady=(20 if label_text == "Product ID:" else 0, 5))
            setattr(self, entry_attr, self._create_entry(form_frame, 30))
            getattr(self, entry_attr).pack(pady=(0, 15))

        self._create_button(form_frame, "GENERATE QR CODE", self.generate_qr_code, 14, width=25, height=2, bg_key='accent_1', fg_key='bg_primary').pack(pady=20)

        self.qr_display_frame = tk.Frame(form_frame, bg=self.colors['bg_secondary'])
        self.qr_display_frame.pack(pady=20)

        # Button to register the product, initially hidden
        self.register_product_button = self._create_button(form_frame, "REGISTER PRODUCT IN BLOCKCHAIN", self.register_generated_product, 12, width=30, height=2, bg_key='success', fg_key='text_primary')
        self.register_product_button.pack(pady=(10, 0))
        self.register_product_button.pack_forget() # Hide it initially

    def generate_qr_code(self):
        """Generate encrypted QR code"""
        product_id, manufacturer, batch_no = self.product_id_entry.get().strip(), self.manufacturer_entry.get().strip(), self.batch_no_entry.get().strip()

        if not all([product_id, manufacturer, batch_no]):
            messagebox.showerror("Error", "Please fill all fields!")
            return

        try:
            key = self.load_key()
            product_info = {"product_id": product_id, "manufacturer": manufacturer, "batch_no": batch_no}

            f = Fernet(key)
            encrypted_data = f.encrypt(json.dumps(product_info).encode())

            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(encrypted_data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img.save("product_qr.png")

            # Store product info and encrypted data temporarily
            self.last_generated_product_info = product_info
            self.last_generated_encrypted_data = encrypted_data

            self.display_qr_code()
            messagebox.showinfo("Success", f"QR Code generated successfully!\n(Product not yet registered in blockchain)")
            self.register_product_button.pack(pady=(10, 0)) # Show the register button

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code: {str(e)}")
            self.register_product_button.pack_forget() # Hide button on error

    def register_generated_product(self):
        """Registers the last generated product's info to the mock blockchain."""
        if not self.last_generated_product_info or not self.last_generated_encrypted_data:
            messagebox.showerror("Error", "No QR code has been generated yet to register.")
            return

        try:
            self.save_to_mock_blockchain(self.last_generated_product_info, self.last_generated_encrypted_data)
            messagebox.showinfo("Registration Success", f"Product {self.last_generated_product_info['product_id']} successfully registered in the blockchain!")

            # Clear temporary data and hide the register button
            self.last_generated_product_info = None
            self.last_generated_encrypted_data = None
            self.register_product_button.pack_forget()
            self.show_main_page() # Go back to main page to see updated stats
        except Exception as e:
            messagebox.showerror("Registration Error", f"Failed to register product: {str(e)}")

    def save_to_mock_blockchain(self, product_info, encrypted_data):
        """Save product to blockchain"""
        record = {
            "product_id": product_info["product_id"], "manufacturer": product_info["manufacturer"],
            "batch_no": product_info["batch_no"], "encrypted_qr_data": encrypted_data.decode(),
            "timestamp": datetime.now().isoformat(), "created_by": self.current_user
        }

        blockchain = json.load(open('mock_blockchain.json', 'r')) if os.path.exists('mock_blockchain.json') else []
        blockchain.append(record)

        with open('mock_blockchain.json', 'w') as file: json.dump(blockchain, file, indent=4)

    def display_qr_code(self):
        """Display generated QR code"""
        for widget in self.qr_display_frame.winfo_children(): widget.destroy()

        try:
            qr_image = Image.open("product_qr.png")
            qr_image = qr_image.resize((200, 200), Image.Resampling.LANCZOS)
            qr_photo = ImageTk.PhotoImage(qr_image)

            qr_label = tk.Label(self.qr_display_frame, image=qr_photo, bg=self.colors['bg_secondary'])
            qr_label.image = qr_photo
            qr_label.pack(pady=10)

            self._create_label(self.qr_display_frame, "QR Code Generated Successfully!", 12, "bold", color_key='success', bg_key='bg_secondary').pack()
            self._create_label(self.qr_display_frame, "Click 'REGISTER PRODUCT' to add to blockchain.", 10, color_key='text_secondary', bg_key='bg_secondary').pack()
        except Exception as e:
            self._create_label(self.qr_display_frame, f"Error displaying QR: {str(e)}", 10, color_key='error', bg_key='bg_secondary').pack()

    def show_verify_qr(self):
        """Show QR verification interface"""
        self.clear_frame()
        self.root.title("Verify QR Code - Blockchain QR System")

        self.current_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.current_frame.pack(fill="both", expand=True)

        header_frame = tk.Frame(self.current_frame, bg=self.colors['bg_secondary'], height=60)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        self._create_button(header_frame, "← Back", self.show_main_page, 12, bg_key='button_back', fg_key='text_primary').pack(side="left", pady=15, padx=20)
        self._create_label(header_frame, "🔍 Verify QR Code", 18, "bold", color_key='accent_2', bg_key='bg_secondary').pack(pady=15)

        verify_frame = tk.Frame(self.current_frame, bg=self.colors['bg_secondary'], relief="raised", bd=2)
        verify_frame.pack(pady=20, padx=100, fill="both", expand=True)

        self._create_label(verify_frame, "QR Code Verification", 16, "bold", bg_key='bg_secondary').pack(pady=30)
        self._create_label(verify_frame, "Click the button below to scan and verify the QR code", 12, bg_key='bg_secondary', color_key='text_secondary').pack(pady=10)
        self._create_button(verify_frame, "🔍 SCAN & VERIFY QR", self.verify_qr_code, 14, width=25, height=3, bg_key='accent_2', fg_key='text_primary').pack(pady=30)

        self.result_frame = tk.Frame(verify_frame, bg=self.colors['bg_secondary'])
        self.result_frame.pack(pady=20, fill="both", expand=True)

    def verify_qr_code(self):
        """Verify QR code authenticity"""
        for widget in self.result_frame.winfo_children(): widget.destroy()

        scanning_label = self._create_label(self.result_frame, "🔍 Scanning QR Code...", 14, color_key='accent_2', bg_key='bg_secondary')
        scanning_label.pack(pady=20)
        self.root.update_idletasks() # Update the UI to show scanning message

        try:
            if not os.path.exists("product_qr.png"):
                raise Exception("QR code file 'product_qr.png' not found. Please generate a QR code first.")

            img = cv2.imread("product_qr.png")
            if img is None: # Check if image loaded successfully
                raise Exception("Could not load 'product_qr.png'. Ensure the file is not corrupted or open elsewhere.")

            detector = cv2.QRCodeDetector()
            data, _, _ = detector.detectAndDecode(img)

            if not data:
                raise Exception("No QR code detected in the image.")

            key = self.load_key()
            try:
                decrypted_data = Fernet(key).decrypt(data.encode()).decode()
                product_info = json.loads(decrypted_data)
            except Exception as decrypt_e:
                raise Exception(f"Failed to decrypt QR data. QR might be invalid or key mismatch. Error: {decrypt_e}")

            is_authentic = self.verify_product(product_info)
            scanning_label.destroy()
            self.show_verification_result(is_authentic, product_info)
        except Exception as e:
            for widget in self.result_frame.winfo_children(): widget.destroy()
            error_frame = tk.Frame(self.result_frame, bg=self.colors['error'], relief="raised", bd=2)
            error_frame.pack(pady=20, padx=20, fill="x")
            self._create_label(error_frame, "❌ ERROR", 16, "bold", color_key='text_primary', bg_key='error').pack(pady=10)
            self._create_label(error_frame, str(e), 12, color_key='text_primary', bg_key='error', wraplength=400).pack(pady=10)

    def verify_product(self, product_info):
        """Check if product exists in blockchain"""
        try:
            blockchain = json.load(open('mock_blockchain.json', 'r'))
            return any(record['product_id'] == product_info['product_id'] and
                       record['manufacturer'] == product_info['manufacturer'] and
                       record['batch_no'] == product_info['batch_no'] for record in blockchain)
        except Exception:
            return False

    def show_verification_result(self, is_authentic, product_info):
        """Display verification results"""
        if is_authentic:
            result_frame = tk.Frame(self.result_frame, bg=self.colors['success'], relief="raised", bd=3)
            result_frame.pack(pady=20, padx=20, fill="x")
            self._create_label(result_frame, "✅ AUTHENTIC PRODUCT", 18, "bold", color_key='text_primary', bg_key='success').pack(pady=15)

            info_frame = tk.Frame(result_frame, bg=self.colors['success'])
            info_frame.pack(pady=10)
            self._create_label(info_frame, f"Product ID: {product_info['product_id']}", 12, color_key='text_primary', bg_key='success').pack()
            self._create_label(info_frame, f"Manufacturer: {product_info['manufacturer']}", 12, color_key='text_primary', bg_key='success').pack()
            self._create_label(info_frame, f"Batch Number: {product_info['batch_no']}", 12, color_key='text_primary', bg_key='success').pack()

            self._create_label(result_frame, "This product is verified and registered in the blockchain.", 11, bg_key='success', color_key='text_primary').pack(pady=10)
        else:
            result_frame = tk.Frame(self.result_frame, bg=self.colors['error'], relief="raised", bd=3)
            result_frame.pack(pady=20, padx=20, fill="x")
            self._create_label(result_frame, "❌ FAKE PRODUCT DETECTED", 18, "bold", color_key='text_primary', bg_key='error').pack(pady=15)
            self._create_label(result_frame, "This product is NOT verified in the blockchain!", 12, "bold", color_key='text_primary', bg_key='error').pack(pady=10)
            self._create_label(result_frame, "⚠️ WARNING: This may be a counterfeit product", 11, bg_key='error', color_key='text_primary').pack(pady=5)

    def logout(self):
        """Handle user logout"""
        self.current_user = None
        self.show_login_page()

    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = BlockchainQRSystem()
    app.run()