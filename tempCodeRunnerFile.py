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
        self.root.configure(bg="#1a1a1a")
        
        
        # User credentials (in real app, this would be in a secure database)
        self.users = {
            "admin": "admin123",
            "user": "password",
            "manufacturer": "mfg2024"
        }
        
        self.current_user = None
        self.current_frame = None
        
        # Initialize system
        self.ensure_files_exist()
        self.show_login_page()
        
    def ensure_files_exist(self):
        """Ensure required files exist"""
        if not os.path.exists("secret.key"):
            self.generate_key()
        if not os.path.exists("mock_blockchain.json"):
            with open("mock_blockchain.json", "w") as f:
                json.dump([], f)
    
    def generate_key(self):
        """Generate AES encryption key"""
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
    
    def load_key(self):
        """Load AES key"""
        return open("secret.key", "rb").read()
    
    def clear_frame(self):
        """Clear current frame"""
        if self.current_frame:
            self.current_frame.destroy()
    
    def show_login_page(self):
        """Display login page"""
        self.clear_frame()
        self.root.title("Login - Blockchain QR System")
        
        self.current_frame = tk.Frame(self.root, bg="#1a1a1a")
        self.current_frame.pack(fill="both", expand=True)
        
        # Login container
        login_frame = tk.Frame(self.current_frame, bg="#2d2d30", relief="raised", bd=2)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title
        title_label = tk.Label(login_frame, text="🔐 Blockchain QR System", 
                              font=("Arial", 24, "bold"), fg="#00ff88", bg="#2d2d30")
        title_label.pack(pady=30, padx=50)
        
        # Subtitle
        subtitle_label = tk.Label(login_frame, text="Secure Product Authentication", 
                                 font=("Arial", 12), fg="#cccccc", bg="#2d2d30")
        subtitle_label.pack(pady=(0, 30))
        
        # Username
        tk.Label(login_frame, text="Username:", font=("Arial", 12), 
                fg="#ffffff", bg="#2d2d30").pack(pady=(10, 5))
        self.username_entry = tk.Entry(login_frame, font=("Arial", 12), width=25, 
                                      bg="#404040", fg="#ffffff", relief="flat", bd=5)
        self.username_entry.pack(pady=(0, 15))
        
        # Password
        tk.Label(login_frame, text="Password:", font=("Arial", 12), 
                fg="#ffffff", bg="#2d2d30").pack(pady=(0, 5))
        self.password_entry = tk.Entry(login_frame, font=("Arial", 12), width=25, 
                                      show="*", bg="#404040", fg="#ffffff", relief="flat", bd=5)
        self.password_entry.pack(pady=(0, 20))
        
        # Login button
        login_btn = tk.Button(login_frame, text="LOGIN", font=("Arial", 12, "bold"), 
                             bg="#00ff88", fg="#000000", width=20, height=2,
                             relief="flat", cursor="hand2", command=self.login)
        login_btn.pack(pady=(10, 30))
        
        # Demo credentials info
        info_frame = tk.Frame(login_frame, bg="#2d2d30")
        info_frame.pack(pady=(0, 20))
        
        tk.Label(info_frame, text="Demo Credentials:", font=("Arial", 10, "bold"), 
                fg="#ffaa00", bg="#2d2d30").pack()
        tk.Label(info_frame, text="admin/admin123 | user/password | manufacturer/mfg2024", 
                font=("Arial", 9), fg="#cccccc", bg="#2d2d30").pack()
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda e: self.login())
        
        # Focus on username entry
        self.username_entry.focus()
    
    def login(self):
        """Handle login authentication"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
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
        
        self.current_frame = tk.Frame(self.root, bg="#1a1a1a")
        self.current_frame.pack(fill="both", expand=True)
        
        # Header
        header_frame = tk.Frame(self.current_frame, bg="#2d2d30", height=80)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="🔗 Blockchain QR Verification System", 
                font=("Arial", 20, "bold"), fg="#00ff88", bg="#2d2d30").pack(side="left", pady=20, padx=20)
        
        # User info and logout
        user_frame = tk.Frame(header_frame, bg="#2d2d30")
        user_frame.pack(side="right", pady=20, padx=20)
        
        tk.Label(user_frame, text=f"Welcome, {self.current_user}", 
                font=("Arial", 12), fg="#ffffff", bg="#2d2d30").pack(side="left", padx=(0, 10))
        
        logout_btn = tk.Button(user_frame, text="Logout", font=("Arial", 10), 
                              bg="#ff4444", fg="#ffffff", relief="flat", 
                              cursor="hand2", command=self.logout)
        logout_btn.pack(side="right")
        
        # Main content area
        content_frame = tk.Frame(self.current_frame, bg="#1a1a1a")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Statistics panel
        stats_frame = tk.Frame(content_frame, bg="#2d2d30", relief="raised", bd=1)
        stats_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(stats_frame, text="📊 System Statistics", font=("Arial", 14, "bold"), 
                fg="#00ff88", bg="#2d2d30").pack(pady=10)
        
        # Load blockchain stats
        try:
            with open("mock_blockchain.json", "r") as f:
                blockchain_data = json.load(f)
            total_products = len(blockchain_data)
        except:
            total_products = 0
        
        stats_info = tk.Frame(stats_frame, bg="#2d2d30")
        stats_info.pack(pady=(0, 15))
        
        tk.Label(stats_info, text=f"Total Registered Products: {total_products}", 
                font=("Arial", 12), fg="#ffffff", bg="#2d2d30").pack(side="left", padx=20)
        
        tk.Label(stats_info, text=f"Current User: {self.current_user}", 
                font=("Arial", 12), fg="#ffffff", bg="#2d2d30").pack(side="right", padx=20)
        
        # Action buttons
        buttons_frame = tk.Frame(content_frame, bg="#1a1a1a")
        buttons_frame.pack(expand=True)
        
        # Generate QR Button
        generate_frame = tk.Frame(buttons_frame, bg="#2d2d30", relief="raised", bd=2)
        generate_frame.pack(side="left", padx=20, pady=20, fill="both", expand=True)
        
        tk.Label(generate_frame, text="📱 Generate QR Code", font=("Arial", 16, "bold"), 
                fg="#00ff88", bg="#2d2d30").pack(pady=20)
        
        tk.Label(generate_frame, text="Create encrypted QR codes for products\nand register them in the blockchain", 
                font=("Arial", 11), fg="#cccccc", bg="#2d2d30", justify="center").pack(pady=10)
        
        generate_btn = tk.Button(generate_frame, text="GENERATE QR", font=("Arial", 14, "bold"), 
                                bg="#00ff88", fg="#000000", width=20, height=3,
                                relief="flat", cursor="hand2", command=self.show_generate_qr)
        generate_btn.pack(pady=20)
        
        # Verify QR Button
        verify_frame = tk.Frame(buttons_frame, bg="#2d2d30", relief="raised", bd=2)
        verify_frame.pack(side="right", padx=20, pady=20, fill="both", expand=True)
        
        tk.Label(verify_frame, text="🔍 Verify QR Code", font=("Arial", 16, "bold"), 
                fg="#ff6b35", bg="#2d2d30").pack(pady=20)
        
        tk.Label(verify_frame, text="Scan and verify QR codes to check\nproduct authenticity against blockchain", 
                font=("Arial", 11), fg="#cccccc", bg="#2d2d30", justify="center").pack(pady=10)
        
        verify_btn = tk.Button(verify_frame, text="VERIFY QR", font=("Arial", 14, "bold"), 
                              bg="#ff6b35", fg="#ffffff", width=20, height=3,
                              relief="flat", cursor="hand2", command=self.show_verify_qr)
        verify_btn.pack(pady=20)
        
        # Recent activity
        activity_frame = tk.Frame(content_frame, bg="#2d2d30", relief="raised", bd=1)
        activity_frame.pack(fill="x", pady=(20, 0))
        
        tk.Label(activity_frame, text="📋 Recent Activity", font=("Arial", 14, "bold"), 
                fg="#00ff88", bg="#2d2d30").pack(pady=10)
        
        # Show recent blockchain entries
        try:
            recent_entries = blockchain_data[-3:] if len(blockchain_data) > 0 else []
            for entry in reversed(recent_entries):
                entry_frame = tk.Frame(activity_frame, bg="#404040")
                entry_frame.pack(fill="x", padx=20, pady=2)
                
                tk.Label(entry_frame, text=f"Product: {entry['product_id']} | Manufacturer: {entry['manufacturer']}", 
                        font=("Arial", 10), fg="#ffffff", bg="#404040").pack(side="left", pady=5, padx=10)
        except:
            tk.Label(activity_frame, text="No recent activity", 
                    font=("Arial", 10), fg="#888888", bg="#2d2d30").pack(pady=10)
        
        activity_frame.pack(pady=(0, 20))
    
    def show_generate_qr(self):
        """Show QR generation interface"""
        self.clear_frame()
        self.root.title("Generate QR Code - Blockchain QR System")
        
        self.current_frame = tk.Frame(self.root, bg="#1a1a1a")
        self.current_frame.pack(fill="both", expand=True)
        
        # Header with back button
        header_frame = tk.Frame(self.current_frame, bg="#2d2d30", height=60)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        back_btn = tk.Button(header_frame, text="← Back", font=("Arial", 12), 
                            bg="#666666", fg="#ffffff", relief="flat", 
                            cursor="hand2", command=self.show_main_page)
        back_btn.pack(side="left", pady=15, padx=20)
        
        tk.Label(header_frame, text="📱 Generate QR Code", font=("Arial", 18, "bold"), 
                fg="#00ff88", bg="#2d2d30").pack(pady=15)
        
        # Form container
        form_frame = tk.Frame(self.current_frame, bg="#2d2d30", relief="raised", bd=2)
        form_frame.pack(pady=20, padx=100, fill="both", expand=True)
        
        tk.Label(form_frame, text="Enter Product Information", font=("Arial", 16, "bold"), 
                fg="#ffffff", bg="#2d2d30").pack(pady=20)
        
        # Product ID
        tk.Label(form_frame, text="Product ID:", font=("Arial", 12), 
                fg="#ffffff", bg="#2d2d30").pack(pady=(20, 5))
        self.product_id_entry = tk.Entry(form_frame, font=("Arial", 12), width=30, 
                                        bg="#404040", fg="#ffffff", relief="flat", bd=5)
        self.product_id_entry.pack(pady=(0, 15))
        
        # Manufacturer
        tk.Label(form_frame, text="Manufacturer:", font=("Arial", 12), 
                fg="#ffffff", bg="#2d2d30").pack(pady=(0, 5))
        self.manufacturer_entry = tk.Entry(form_frame, font=("Arial", 12), width=30, 
                                          bg="#404040", fg="#ffffff", relief="flat", bd=5)
        self.manufacturer_entry.pack(pady=(0, 15))
        
        # Batch Number
        tk.Label(form_frame, text="Batch Number:", font=("Arial", 12), 
                fg="#ffffff", bg="#2d2d30").pack(pady=(0, 5))
        self.batch_no_entry = tk.Entry(form_frame, font=("Arial", 12), width=30, 
                                      bg="#404040", fg="#ffffff", relief="flat", bd=5)
        self.batch_no_entry.pack(pady=(0, 30))
        
        # Generate button
        generate_btn = tk.Button(form_frame, text="GENERATE QR CODE", font=("Arial", 14, "bold"), 
                                bg="#00ff88", fg="#000000", width=25, height=2,
                                relief="flat", cursor="hand2", command=self.generate_qr_code)
        generate_btn.pack(pady=20)
        
        # QR display area
        self.qr_display_frame = tk.Frame(form_frame, bg="#2d2d30")
        self.qr_display_frame.pack(pady=20)
        
    def generate_qr_code(self):
        """Generate encrypted QR code"""
        product_id = self.product_id_entry.get().strip()
        manufacturer = self.manufacturer_entry.get().strip()
        batch_no = self.batch_no_entry.get().strip()
        
        if not all([product_id, manufacturer, batch_no]):
            messagebox.showerror("Error", "Please fill all fields!")
            return
        
        try:
            # Load key and create product info
            key = self.load_key()
            product_info = {
                "product_id": product_id,
                "manufacturer": manufacturer,
                "batch_no": batch_no
            }
            
            # Encrypt product data
            product_data = json.dumps(product_info)
            f = Fernet(key)
            encrypted_data = f.encrypt(product_data.encode())
            
            # Generate QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(encrypted_data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img.save("product_qr.png")
            
            # Save to blockchain
            self.save_to_mock_blockchain(product_info, encrypted_data)
            
            # Display QR code
            self.display_qr_code()
            
            messagebox.showinfo("Success", f"QR Code generated successfully!\nProduct {product_id} registered in blockchain.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code: {str(e)}")
    
    def save_to_mock_blockchain(self, product_info, encrypted_data):
        """Save product to blockchain"""
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
        """Display generated QR code"""
        try:
            # Clear previous QR display
            for widget in self.qr_display_frame.winfo_children():
                widget.destroy()
            
            # Load and display QR image
            qr_image = Image.open("product_qr.png")
            qr_image = qr_image.resize((200, 200), Image.Resampling.LANCZOS)
            qr_photo = ImageTk.PhotoImage(qr_image)
            
            qr_label = tk.Label(self.qr_display_frame, image=qr_photo, bg="#2d2d30")
            qr_label.image = qr_photo  # Keep a reference
            qr_label.pack(pady=10)
            
            tk.Label(self.qr_display_frame, text="QR Code Generated Successfully!", 
                    font=("Arial", 12, "bold"), fg="#00ff88", bg="#2d2d30").pack()
            
        except Exception as e:
            tk.Label(self.qr_display_frame, text=f"Error displaying QR: {str(e)}", 
                    font=("Arial", 10), fg="#ff4444", bg="#2d2d30").pack()
    
    def show_verify_qr(self):
        """Show QR verification interface"""
        self.clear_frame()
        self.root.title("Verify QR Code - Blockchain QR System")
        
        self.current_frame = tk.Frame(self.root, bg="#1a1a1a")
        self.current_frame.pack(fill="both", expand=True)
        
        # Header with back button
        header_frame = tk.Frame(self.current_frame, bg="#2d2d30", height=60)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        back_btn = tk.Button(header_frame, text="← Back", font=("Arial", 12), 
                            bg="#666666", fg="#ffffff", relief="flat", 
                            cursor="hand2", command=self.show_main_page)
        back_btn.pack(side="left", pady=15, padx=20)
        
        tk.Label(header_frame, text="🔍 Verify QR Code", font=("Arial", 18, "bold"), 
                fg="#ff6b35", bg="#2d2d30").pack(pady=15)
        
        # Verify container
        verify_frame = tk.Frame(self.current_frame, bg="#2d2d30", relief="raised", bd=2)
        verify_frame.pack(pady=20, padx=100, fill="both", expand=True)
        
        tk.Label(verify_frame, text="QR Code Verification", font=("Arial", 16, "bold"), 
                fg="#ffffff", bg="#2d2d30").pack(pady=30)
        
        tk.Label(verify_frame, text="Click the button below to scan and verify the QR code", 
                font=("Arial", 12), fg="#cccccc", bg="#2d2d30").pack(pady=10)
        
        # Verify button
        verify_btn = tk.Button(verify_frame, text="🔍 SCAN & VERIFY QR", font=("Arial", 14, "bold"), 
                              bg="#ff6b35", fg="#ffffff", width=25, height=3,
                              relief="flat", cursor="hand2", command=self.verify_qr_code)
        verify_btn.pack(pady=30)
        
        # Result display area
        self.result_frame = tk.Frame(verify_frame, bg="#2d2d30")
        self.result_frame.pack(pady=20, fill="both", expand=True)
    
    def verify_qr_code(self):
        """Verify QR code authenticity"""
        try:
            # Clear previous results
            for widget in self.result_frame.winfo_children():
                widget.destroy()
            
            # Show scanning message
            scanning_label = tk.Label(self.result_frame, text="🔍 Scanning QR Code...", 
                                    font=("Arial", 14), fg="#ffaa00", bg="#2d2d30")
            scanning_label.pack(pady=20)
            
            self.root.update()
            
            # Read QR code
            if not os.path.exists("product_qr.png"):
                raise Exception("QR code file not found. Please generate a QR code first.")
            
            img = cv2.imread("product_qr.png")
            detector = cv2.QRCodeDetector()
            data, bbox, _ = detector.detectAndDecode(img)
            
            if not data:
                raise Exception("No QR code detected in the image.")
            
            # Decrypt data
            key = self.load_key()
            f = Fernet(key)
            decrypted_data = f.decrypt(data.encode()).decode()
            product_info = json.loads(decrypted_data)
            
            # Verify against blockchain
            is_authentic = self.verify_product(product_info)
            
            # Clear scanning message
            scanning_label.destroy()
            
            # Show results
            self.show_verification_result(is_authentic, product_info)
            
        except Exception as e:
            # Clear scanning message
            for widget in self.result_frame.winfo_children():
                widget.destroy()
            
            # Show error
            error_frame = tk.Frame(self.result_frame, bg="#660000", relief="raised", bd=2)
            error_frame.pack(pady=20, padx=20, fill="x")
            
            tk.Label(error_frame, text="❌ ERROR", font=("Arial", 16, "bold"), 
                    fg="#ffffff", bg="#660000").pack(pady=10)
            
            tk.Label(error_frame, text=str(e), font=("Arial", 12), 
                    fg="#ffffff", bg="#660000", wraplength=400).pack(pady=10)
    
    def verify_product(self, product_info):
        """Check if product exists in blockchain"""
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