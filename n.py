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
        self.root.title("🔗 BLOCKCHAIN QR SYSTEM - CYBERPUNK")
        self.root.geometry("900x700")
        
        # CYBERPUNK NEON COLOR SCHEME
        self.colors = {
            'bg_primary': '#0a0a0a',      # Deep black
            'bg_secondary': '#1a1a2e',    # Dark navy
            'bg_card': '#16213e',         # Card background
            'accent_1': '#00ffff',        # Cyan neon
            'accent_2': '#ff0080',        # Hot pink
            'text_primary': '#ffffff',    # White
            'text_secondary': '#b3b3ff',  # Light purple
            'success': '#00ff41',         # Matrix green
            'error': '#ff073a',           # Neon red
            'warning': '#ffff00'          # Electric yellow
        }
        
        self.root.configure(bg=self.colors['bg_primary'])
        
        # User credentials
        self.users = {
            "admin": "admin123",
            "user": "password",
            "manufacturer": "mfg2024"
        }
        
        self.current_user = None
        self.current_frame = None
        
        self.ensure_files_exist()
        self.show_login_page()
        
    def ensure_files_exist(self):
        if not os.path.exists("secret.key"):
            self.generate_key()
        if not os.path.exists("mock_blockchain.json"):
            with open("mock_blockchain.json", "w") as f:
                json.dump([], f)
    
    def generate_key(self):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
    
    def load_key(self):
        return open("secret.key", "rb").read()
    
    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
    
    def show_login_page(self):
        self.clear_frame()
        self.root.title("🔗 BLOCKCHAIN QR SYSTEM - CYBERPUNK LOGIN")
        
        self.current_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.current_frame.pack(fill="both", expand=True)
        
        # Animated background effect
        canvas = tk.Canvas(self.current_frame, bg=self.colors['bg_primary'], highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        
        # Login container with glow effect
        login_frame = tk.Frame(canvas, bg=self.colors['bg_secondary'], relief="solid", bd=3)
        login_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=500)
        
        # Neon border effect
        glow_frame = tk.Frame(canvas, bg=self.colors['accent_1'], relief="solid", bd=1)
        glow_frame.place(relx=0.5, rely=0.5, anchor="center", width=404, height=504)
        login_frame.lift()
        
        # Cyberpunk title with neon effect
        title_label = tk.Label(login_frame, text="⚡ BLOCKCHAIN", 
                              font=("Courier New", 20, "bold"), 
                              fg=self.colors['accent_1'], bg=self.colors['bg_secondary'])
        title_label.pack(pady=(30, 5))
        
        title_label2 = tk.Label(login_frame, text="QR SYSTEM", 
                               font=("Courier New", 20, "bold"), 
                               fg=self.colors['accent_2'], bg=self.colors['bg_secondary'])
        title_label2.pack(pady=(0, 10))
        
        # Subtitle with matrix effect
        subtitle_label = tk.Label(login_frame, text=">>> SECURE ACCESS PORTAL <<<", 
                                 font=("Courier New", 10), 
                                 fg=self.colors['success'], bg=self.colors['bg_secondary'])
        subtitle_label.pack(pady=(0, 30))
        
        # Username section
        tk.Label(login_frame, text=">> USERNAME:", font=("Courier New", 11, "bold"), 
                fg=self.colors['text_primary'], bg=self.colors['bg_secondary']).pack(pady=(10, 5))
        self.username_entry = tk.Entry(login_frame, font=("Courier New", 12), width=25, 
                                      bg=self.colors['bg_card'], fg=self.colors['accent_1'], 
                                      relief="solid", bd=2, insertbackground=self.colors['accent_1'])
        self.username_entry.pack(pady=(0, 15))
        
        # Password section
        tk.Label(login_frame, text=">> PASSWORD:", font=("Courier New", 11, "bold"), 
                fg=self.colors['text_primary'], bg=self.colors['bg_secondary']).pack(pady=(0, 5))
        self.password_entry = tk.Entry(login_frame, font=("Courier New", 12), width=25, show="*",
                                      bg=self.colors['bg_card'], fg=self.colors['accent_1'], 
                                      relief="solid", bd=2, insertbackground=self.colors['accent_1'])
        self.password_entry.pack(pady=(0, 30))
        
        # Cyberpunk login button
        login_btn = tk.Button(login_frame, text=">>> ACCESS GRANTED <<<", 
                             font=("Courier New", 12, "bold"), 
                             bg=self.colors['accent_1'], fg=self.colors['bg_primary'], 
                             width=25, height=2, relief="solid", bd=2,
                             cursor="hand2", command=self.login,
                             activebackground=self.colors['accent_2'])
        login_btn.pack(pady=(10, 20))
        
        # Demo credentials with cyberpunk styling
        info_frame = tk.Frame(login_frame, bg=self.colors['bg_secondary'])
        info_frame.pack(pady=(10, 20))
        
        tk.Label(info_frame, text="[ DEMO ACCESS CODES ]", font=("Courier New", 9, "bold"), 
                fg=self.colors['warning'], bg=self.colors['bg_secondary']).pack()
        tk.Label(info_frame, text="admin/admin123 | user/password | manufacturer/mfg2024", 
                font=("Courier New", 8), fg=self.colors['text_secondary'], bg=self.colors['bg_secondary']).pack()
        
        self.root.bind('<Return>', lambda e: self.login())
        self.username_entry.focus()
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username in self.users and self.users[username] == password:
            self.current_user = username
            self.show_main_page()
        else:
            messagebox.showerror("ACCESS DENIED", "Invalid access codes detected!")
            self.password_entry.delete(0, tk.END)
    
    def show_main_page(self):
        self.clear_frame()
        self.root.title(f"🔗 BLOCKCHAIN QR SYSTEM - USER: {self.current_user.upper()}")
        
        self.current_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.current_frame.pack(fill="both", expand=True)
        
        # Cyberpunk header with neon effects
        header_frame = tk.Frame(self.current_frame, bg=self.colors['bg_secondary'], height=100, relief="solid", bd=2)
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        header_frame.pack_propagate(False)
        
        # Neon glow for header
        glow_header = tk.Frame(self.current_frame, bg=self.colors['accent_1'], height=104)
        glow_header.place(x=8, y=8, relwidth=1.0, width=-16)
        header_frame.lift()
        
        tk.Label(header_frame, text="⚡ BLOCKCHAIN QR MATRIX ⚡", 
                font=("Courier New", 18, "bold"), fg=self.colors['accent_1'], bg=self.colors['bg_secondary']).pack(side="left", pady=30, padx=20)
        
        # User panel
        user_frame = tk.Frame(header_frame, bg=self.colors['bg_secondary'])
        user_frame.pack(side="right", pady=20, padx=20)
        
        tk.Label(user_frame, text=f"USER: {self.current_user.upper()}", 
                font=("Courier New", 11, "bold"), fg=self.colors['success'], bg=self.colors['bg_secondary']).pack(side="left", padx=(0, 15))
        
        logout_btn = tk.Button(user_frame, text="[ LOGOUT ]", font=("Courier New", 10, "bold"), 
                              bg=self.colors['error'], fg=self.colors['text_primary'], relief="solid", bd=2,
                              cursor="hand2", command=self.logout)
        logout_btn.pack(side="right")
        
        # Stats panel with matrix styling
        stats_frame = tk.Frame(self.current_frame, bg=self.colors['bg_card'], relief="solid", bd=2)
        stats_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(stats_frame, text=">>> SYSTEM STATUS <<<", font=("Courier New", 12, "bold"), 
                fg=self.colors['success'], bg=self.colors['bg_card']).pack(pady=10)
        
        try:
            with open("mock_blockchain.json", "r") as f:
                blockchain_data = json.load(f)
            total_products = len(blockchain_data)
        except:
            total_products = 0
        
        stats_info = tk.Frame(stats_frame, bg=self.colors['bg_card'])
        stats_info.pack(pady=(0, 15))
        
        tk.Label(stats_info, text=f"REGISTERED PRODUCTS: {total_products}", 
                font=("Courier New", 11), fg=self.colors['text_primary'], bg=self.colors['bg_card']).pack(side="left", padx=20)
        
        tk.Label(stats_info, text=f"CURRENT SESSION: {self.current_user.upper()}", 
                font=("Courier New", 11), fg=self.colors['text_primary'], bg=self.colors['bg_card']).pack(side="right", padx=20)
        
        # Action buttons with cyberpunk styling
        buttons_frame = tk.Frame(self.current_frame, bg=self.colors['bg_primary'])
        buttons_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Generate QR section
        generate_frame = tk.Frame(buttons_frame, bg=self.colors['bg_secondary'], relief="solid", bd=3)
        generate_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        
        # Neon glow effect
        gen_glow = tk.Frame(buttons_frame, bg=self.colors['accent_1'])
        gen_glow.place(in_=generate_frame, x=-2, y=-2, relwidth=1.0, relheight=1.0, width=4, height=4)
        generate_frame.lift()
        
        tk.Label(generate_frame, text="⚡ GENERATE", font=("Courier New", 14, "bold"), 
                fg=self.colors['accent_1'], bg=self.colors['bg_secondary']).pack(pady=(20, 5))
        tk.Label(generate_frame, text="QR MATRIX", font=("Courier New", 14, "bold"), 
                fg=self.colors['accent_2'], bg=self.colors['bg_secondary']).pack(pady=(0, 15))
        
        tk.Label(generate_frame, text=">>> Create encrypted QR codes\n>>> Register in blockchain matrix", 
                font=("Courier New", 9), fg=self.colors['text_secondary'], bg=self.colors['bg_secondary'], justify="center").pack(pady=10)
        
        generate_btn = tk.Button(generate_frame, text="[ INITIALIZE ]", font=("Courier New", 12, "bold"), 
                                bg=self.colors['success'], fg=self.colors['bg_primary'], width=18, height=3,
                                relief="solid", bd=2, cursor="hand2", command=self.show_generate_qr,
                                activebackground=self.colors['accent_1'])
        generate_btn.pack(pady=20)
        
        # Verify QR section
        verify_frame = tk.Frame(buttons_frame, bg=self.colors['bg_secondary'], relief="solid", bd=3)
        verify_frame.pack(side="right", padx=10, pady=10, fill="both", expand=True)
        
        # Neon glow effect
        ver_glow = tk.Frame(buttons_frame, bg=self.colors['accent_2'])
        ver_glow.place(in_=verify_frame, x=-2, y=-2, relwidth=1.0, relheight=1.0, width=4, height=4)
        verify_frame.lift()
        
        tk.Label(verify_frame, text="🔍 SCAN &", font=("Courier New", 14, "bold"), 
                fg=self.colors['accent_2'], bg=self.colors['bg_secondary']).pack(pady=(20, 5))
        tk.Label(verify_frame, text="VERIFY", font=("Courier New", 14, "bold"), 
                fg=self.colors['accent_1'], bg=self.colors['bg_secondary']).pack(pady=(0, 15))
        
        tk.Label(verify_frame, text=">>> Decode QR matrices\n>>> Verify blockchain authenticity", 
                font=("Courier New", 9), fg=self.colors['text_secondary'], bg=self.colors['bg_secondary'], justify="center").pack(pady=10)
        
        verify_btn = tk.Button(verify_frame, text="[ EXECUTE ]", font=("Courier New", 12, "bold"), 
                              bg=self.colors['accent_2'], fg=self.colors['text_primary'], width=18, height=3,
                              relief="solid", bd=2, cursor="hand2", command=self.show_verify_qr,
                              activebackground=self.colors['error'])
        verify_btn.pack(pady=20)
        
        # Recent activity with matrix effect
        activity_frame = tk.Frame(self.current_frame, bg=self.colors['bg_card'], relief="solid", bd=2)
        activity_frame.pack(fill="x", padx=10, pady=(5, 10))
        
        tk.Label(activity_frame, text=">>> RECENT BLOCKCHAIN ACTIVITY <<<", font=("Courier New", 11, "bold"), 
                fg=self.colors['success'], bg=self.colors['bg_card']).pack(pady=10)
        
        try:
            recent_entries = blockchain_data[-3:] if len(blockchain_data) > 0 else []
            for entry in reversed(recent_entries):
                entry_frame = tk.Frame(activity_frame, bg=self.colors['bg_secondary'])
                entry_frame.pack(fill="x", padx=20, pady=2)
                
                tk.Label(entry_frame, text=f">> PRODUCT: {entry['product_id']} | MFG: {entry['manufacturer']}", 
                        font=("Courier New", 9), fg=self.colors['text_primary'], bg=self.colors['bg_secondary']).pack(side="left", pady=3, padx=10)
        except:
            tk.Label(activity_frame, text=">>> NO RECENT ACTIVITY DETECTED <<<", 
                    font=("Courier New", 9), fg=self.colors['error'], bg=self.colors['bg_card']).pack(pady=10)
        
        activity_frame.pack(pady=(0, 10))
    
    def show_generate_qr(self):
        self.clear_frame()
        self.root.title("⚡ GENERATE QR MATRIX - BLOCKCHAIN SYSTEM")
        
        self.current_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.current_frame.pack(fill="both", expand=True)
        
        # Header with cyberpunk styling
        header_frame = tk.Frame(self.current_frame, bg=self.colors['bg_secondary'], height=70, relief="solid", bd=2)
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        header_frame.pack_propagate(False)
        
        back_btn = tk.Button(header_frame, text="[ << BACK ]", font=("Courier New", 10, "bold"), 
                            bg=self.colors['bg_card'], fg=self.colors['text_primary'], relief="solid", bd=2,
                            cursor="hand2", command=self.show_main_page)
        back_btn.pack(side="left", pady=15, padx=20)
        
        tk.Label(header_frame, text="⚡ QR MATRIX GENERATOR ⚡", font=("Courier New", 16, "bold"), 
                fg=self.colors['accent_1'], bg=self.colors['bg_secondary']).pack(pady=15)
        
        # Form with cyberpunk styling
        form_frame = tk.Frame(self.current_frame, bg=self.colors['bg_secondary'], relief="solid", bd=3)
        form_frame.pack(pady=10, padx=50, fill="both", expand=True)
        
        # Glow effect
        glow_form = tk.Frame(self.current_frame, bg=self.colors['accent_1'])
        glow_form.place(in_=form_frame, x=-2, y=-2, relwidth=1.0, relheight=1.0, width=4, height=4)
        form_frame.lift()
        
        tk.Label(form_frame, text=">>> ENTER PRODUCT DATA <<<", font=("Courier New", 14, "bold"), 
                fg=self.colors['success'], bg=self.colors['bg_secondary']).pack(pady=20)
        
        # Product ID
        tk.Label(form_frame, text=">> PRODUCT ID:", font=("Courier New", 11, "bold"), 
                fg=self.colors['text_primary'], bg=self.colors['bg_secondary']).pack(pady=(20, 5))
        self.product_id_entry = tk.Entry(form_frame, font=("Courier New", 12), width=35, 
                                        bg=self.colors['bg_card'], fg=self.colors['accent_1'], 
                                        relief="solid", bd=2, insertbackground=self.colors['accent_1'])
        self.product_id_entry.pack(pady=(0, 15))
        
        # Manufacturer
        tk.Label(form_frame, text=">> MANUFACTURER:", font=("Courier New", 11, "bold"), 
                fg=self.colors['text_primary'], bg=self.colors['bg_secondary']).pack(pady=(0, 5))
        self.manufacturer_entry = tk.Entry(form_frame, font=("Courier New", 12), width=35, 
                                          bg=self.colors['bg_card'], fg=self.colors['accent_1'], 
                                          relief="solid", bd=2, insertbackground=self.colors['accent_1'])
        self.manufacturer_entry.pack(pady=(0, 15))
        
        # Batch Number
        tk.Label(form_frame, text=">> BATCH NUMBER:", font=("Courier New", 11, "bold"), 
                fg=self.colors['text_primary'], bg=self.colors['bg_secondary']).pack(pady=(0, 5))
        self.batch_no_entry = tk.Entry(form_frame, font=("Courier New", 12), width=35, 
                                      bg=self.colors['bg_card'], fg=self.colors['accent_1'], 
                                      relief="solid", bd=2, insertbackground=self.colors['accent_1'])
        self.batch_no_entry.pack(pady=(0, 30))
        
        # Generate button
        generate_btn = tk.Button(form_frame, text=">>> GENERATE QR MATRIX <<<", font=("Courier New", 12, "bold"), 
                                bg=self.colors['success'], fg=self.colors['bg_primary'], width=30, height=2,
                                relief="solid", bd=2, cursor="hand2", command=self.generate_qr_code,
                                activebackground=self.colors['accent_1'])
        generate_btn.pack(pady=20)
        
        # QR display area
        self.qr_display_frame = tk.Frame(form_frame, bg=self.colors['bg_secondary'])
        self.qr_display_frame.pack(pady=20)
        
    def generate_qr_code(self):
        product_id = self.product_id_entry.get().strip()
        manufacturer = self.manufacturer_entry.get().strip()
        batch_no = self.batch_no_entry.get().strip()
        
        if not all([product_id, manufacturer, batch_no]):
            messagebox.showerror("DATA INCOMPLETE", "All fields must be completed!")
            return
        
        try:
            key = self.load_key()
            product_info = {
                "product_id": product_id,
                "manufacturer": manufacturer,
                "batch_no": batch_no
            }
            
            product_data = json.dumps(product_info)
            f = Fernet(key)
            encrypted_data = f.encrypt(product_data.encode())
            
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(encrypted_data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img.save("product_qr.png")
            
            self.save_to_mock_blockchain(product_info, encrypted_data)
            self.display_qr_code()
            
            messagebox.showinfo("QR MATRIX GENERATED", f"Product {product_id} successfully encoded and registered!")
            
        except Exception as e:
            messagebox.showerror("GENERATION FAILED", f"QR Matrix generation error: {str(e)}")
    
    def save_to_mock_blockchain(self, product_info, encrypted_data):
        record = {
            "product_id": product_info["product_id"],
            "manufacturer": product_info["manufacturer"],
            "batch_no": product_info["batch_no"],
            "encrypted_qr_data": encrypted_data.decode(),
            "timestamp": datetime.now().isoformat(),
            "created_by": self.current_user
        }
        
        try:
            with open('mock_blockchain.json', 'r') as file:
                blockchain = json.load(file)
        except FileNotFoundError:
            blockchain = []
        
        blockchain.append(record)
        
        with open('mock_blockchain.json', 'w') as file:
            json.dump(blockchain, file, indent=4)
    
    def display_qr_code(self):
        try:
            for widget in self.qr_display_frame.winfo_children():
                widget.destroy()
            
            qr_image = Image.open("product_qr.png")
            qr_image = qr_image.resize((200, 200), Image.Resampling.LANCZOS)
            qr_photo = ImageTk.PhotoImage(qr_image)
            
            qr_label = tk.Label(self.qr_display_frame, image=qr_photo, bg=self.colors['bg_secondary'])
            qr_label.image = qr_photo
            qr_label.pack(pady=10)
            
            tk.Label(self.qr_display_frame, text=">>> QR MATRIX GENERATED <<<", 
                    font=("Courier New", 11, "bold"), fg=self.colors['success'], bg=self.colors['bg_secondary']).pack()
            
        except Exception as e:
            tk.Label(self.qr_display_frame, text=f"DISPLAY ERROR: {str(e)}", 
                    font=("Courier New", 9), fg=self.colors['error'], bg=self.colors['bg_secondary']).pack()
    
    def show_verify_qr(self):
        self.clear_frame()
        self.root.title("🔍 VERIFY QR MATRIX - BLOCKCHAIN SYSTEM")
        
        self.current_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.current_frame.pack(fill="both", expand=True)
        
        # Header
        header_frame = tk.Frame(self.current_frame, bg=self.colors['bg_secondary'], height=70, relief="solid", bd=2)
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        header_frame.pack_propagate(False)
        
        back_btn = tk.Button(header_frame, text="[ << BACK ]", font=("Courier New", 10, "bold"), 
                            bg=self.colors['bg_card'], fg=self.colors['text_primary'], relief="solid", bd=2,
                            cursor="hand2", command=self.show_main_page)
        back_btn.pack(side="left", pady=15, padx=20)
        
        tk.Label(header_frame, text="🔍 QR MATRIX SCANNER 🔍", font=("Courier New", 16, "bold"), 
                fg=self.colors['accent_2'], bg=self.colors['bg_secondary']).pack(pady=15)
        
        # Verify container
        verify_frame = tk.Frame(self.current_frame, bg=self.colors['bg_secondary'], relief="solid", bd=3)
        verify_frame.pack(pady=10, padx=50, fill="both", expand=True)
        
        # Glow effect
        glow_verify = tk.Frame(self.current_frame, bg=self.colors['accent_2'])
        glow_verify.place(in_=verify_frame, x=-2, y=-2, relwidth=1.0, relheight=1.0, width=4, height=4)
        verify_frame.lift()
        
        tk.Label(verify_frame, text=">>> QR MATRIX VERIFICATION <<<", font=("Courier New", 14, "bold"), 
                fg=self.colors['success'], bg=self.colors['bg_secondary']).pack(pady=30)
        
        tk.Label(verify_frame, text="Initialize scanning protocol to verify QR matrix authenticity", 
                font=("Courier New", 10), fg=self.colors['text_secondary'], bg=self.colors['bg_secondary']).pack(pady=10)
        
        # Verify button
        verify_btn = tk.Button(verify_frame, text=">>> INITIATE SCAN <<<", font=("Courier New", 12, "bold"), 
                              bg=self.colors['accent_2'], fg=self.colors['text_primary'], width=25, height=3,
                              relief="solid", bd=2, cursor="hand2", command=self.verify_qr_code,
                              activebackground=self.colors['error'])
        verify_btn.pack(pady=30)
        
        # Result display area
        self.result_frame = tk.Frame(verify_frame, bg=self.colors['bg_secondary'])
        self.result_frame.pack(pady=20, fill="both", expand=True)
    
    def verify_qr_code(self):
        try:
            for widget in self.result_frame.winfo_children():
                widget.destroy()
            
            scanning_label = tk.Label(self.result_frame, text=">>> SCANNING QR MATRIX <<<", 
                                    font=("Courier New", 12, "bold"), fg=self.colors['warning'], bg=self.colors['bg_secondary'])
            scanning_label.pack(pady=20)
            
            self.root.update()
            
            if not os.path.exists("product_qr.png"):
                raise Exception("QR matrix file not detected. Generate QR matrix first.")
            
            img = cv2.imread("product_qr.png")
            detector = cv2.QRCodeDetector()
            data, bbox, _ = detector.detectAndDecode(img)
            
            if not data:
                raise Exception("No QR matrix detected in scan area.")
            
            key = self.load_key()
            f = Fernet(key)
            decrypted_data = f.decrypt(data.encode()).decode()
            product_info = json.loads(decrypted_data)
            
            is_authentic = self.verify_product(product_info)
            
            scanning_label.destroy()
            self.show_verification_result(is_authentic, product_info)
            
        except Exception as e:
            for widget in self.result_frame.winfo_children():
                widget.destroy()
            
            error_frame = tk.Frame(self.result_frame, bg=self.colors['error'], relief="solid", bd=3)
            error_frame.pack(pady=20, padx=20, fill="x")
            
            tk.Label(error_frame, text=">>> SCAN FAILED <<<", font=("Courier New", 14, "bold"), 
                    fg=self.colors['text_primary'], bg=self.colors['error']).pack(pady=10)
            
            tk.Label(error_frame, text=str(e), font=("Courier New", 10), 
                    fg=self.colors['text_primary'], bg=self.colors['error'], wraplength=400).pack(pady=10)
    
    def verify_product(self, product_info):
        try:
            with open('mock_blockchain.json', 'r') as file:
                blockchain = json.load(file)
            
            for record in blockchain:
                if (record['product_id'] == product_info['product_id'] and
                    record['manufacturer'] == product_info['manufacturer'] and
                    record['batch_no'] == product_info['batch_no']):
                    return True
            return False
        except:
            return False
        
    def show_verification_result(self, is_authentic, product_info):
        """Display verification results"""
        if is_authentic:
            # Authentic product
            result_frame = tk.Frame(self.result_frame, bg="#006600", relief="raised", bd=3)
            result_frame.pack(pady=20, padx=20, fill="x")
            
            tk.Label(result_frame, text="✅ AUTHENTIC PRODUCT", font=("Arial", 18, "bold"), 
                    fg="#ffffff", bg="#006600").pack(pady=15)
            
            info_frame = tk.Frame(result_frame, bg="#006600")
            info_frame.pack(pady=10)
            
            tk.Label(info_frame, text=f"Product ID: {product_info['product_id']}", 
                    font=("Arial", 12), fg="#ffffff", bg="#006600").pack()
            tk.Label(info_frame, text=f"Manufacturer: {product_info['manufacturer']}", 
                    font=("Arial", 12), fg="#ffffff", bg="#006600").pack()
            tk.Label(info_frame, text=f"Batch Number: {product_info['batch_no']}", 
                    font=("Arial", 12), fg="#ffffff", bg="#006600").pack()
            
            tk.Label(result_frame, text="This product is verified and registered in the blockchain.", 
                    font=("Arial", 11), fg="#ccffcc", bg="#006600").pack(pady=10)
        else:
            # Fake product
            result_frame = tk.Frame(self.result_frame, bg="#cc0000", relief="raised", bd=3)
            result_frame.pack(pady=20, padx=20, fill="x")
            
            tk.Label(result_frame, text="❌ FAKE PRODUCT DETECTED", font=("Arial", 18, "bold"), 
                    fg="#ffffff", bg="#cc0000").pack(pady=15)
            
            tk.Label(result_frame, text="This product is NOT verified in the blockchain!", 
                    font=("Arial", 12, "bold"), fg="#ffffff", bg="#cc0000").pack(pady=10)
            
            tk.Label(result_frame, text="⚠️ WARNING: This may be a counterfeit product", 
                    font=("Arial", 11), fg="#ffcccc", bg="#cc0000").pack(pady=5)
    
    def logout(self):
        """Handle user logout"""
        self.current_user = None
        self.show_login_page()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

# Run the application
if __name__ == "__main__":
    app = BlockchainQRSystem()
    app.run()