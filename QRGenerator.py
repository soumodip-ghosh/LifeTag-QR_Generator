import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import qrcode
from PIL import Image, ImageTk
import json
import os

class MedicalEmergencyQRGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("LifeTag: The Emergency QR Code Generator for Wallpapers")
        self.root.geometry("700x750")
        self.root.resizable(True, True)
        
        # Set theme colors
        self.primary_color = "#e63946"  # Red for medical theme
        self.secondary_color = "#f1faee"
        self.accent_color = "#1d3557"
        
        self.root.configure(bg=self.secondary_color)
        
        # Variables for storing information
        self.qr_image = None
        self.photo_image = None
        
        # Info message and emergency number (can be configured)
        self.info_message = "This QR code contains vital medical information for emergency use."
        self.emergency_number = "911"  # Default emergency number
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header frame for title
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill=tk.X)
        
        # Title
        title_label = tk.Label(
            self.header_frame, 
            text="LifeTag: QR Emergency Wallpaper", 
            font=("Arial", 16, "bold"),
            fg=self.primary_color,
            bg=self.secondary_color
        )
        title_label.pack(side=tk.LEFT, pady=10)
        
        # Create settings button to configure info message
        self.settings_button = tk.Button(
            self.header_frame,
            text="⚙️",
            font=("Arial", 12),
            fg="white",
            bg=self.accent_color,
            width=2,
            height=1,
            borderwidth=0,
            command=self.open_settings,
            cursor="hand2"
        )
        self.settings_button.pack(side=tk.RIGHT, padx=5)
        
        # Create input frame
        self.input_frame = ttk.LabelFrame(self.main_frame, text="Personal Information")
        self.input_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create form fields
        self.create_form_field("Full Name:", "full_name")
        self.create_form_field("Date of Birth (DD/MM/YYYY):", "dob")
        self.create_form_field("Blood Group:", "blood_group")
        self.create_form_field("Allergies (separate with commas):", "allergies")
        self.create_form_field("Medical Conditions:", "medical_conditions")
        self.create_form_field("Current Medications:", "medications")
        self.create_form_field("Emergency Contact Name:", "emergency_contact_name")
        self.create_form_field("Emergency Contact Phone:", "emergency_contact_phone")
        self.create_form_field("Emergency Contact Relationship:", "emergency_contact_relation")
        self.create_form_field("Home Address:", "address")
        self.create_form_field("Additional Information:", "additional_info", height=3)
        
        # Create buttons frame
        self.buttons_frame = ttk.Frame(self.main_frame)
        self.buttons_frame.pack(fill=tk.X, pady=10)
        
        # Generate button
        self.generate_button = tk.Button(
            self.buttons_frame,
            text="Generate QR Code",
            command=self.generate_qr_code,
            bg=self.primary_color,
            fg="white",
            font=("Arial", 12),
            relief=tk.RAISED,
            padx=10,
            pady=5
        )
        self.generate_button.pack(side=tk.LEFT, padx=5)
        
        # Save button
        self.save_button = tk.Button(
            self.buttons_frame,
            text="Save QR Code",
            command=self.save_qr_code,
            bg=self.accent_color,
            fg="white",
            font=("Arial", 12),
            relief=tk.RAISED,
            padx=10,
            pady=5,
            state=tk.DISABLED
        )
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        self.clear_button = tk.Button(
            self.buttons_frame,
            text="Clear Form",
            command=self.clear_form,
            bg=self.accent_color,
            fg="white",
            font=("Arial", 12),
            relief=tk.RAISED,
            padx=10,
            pady=5
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # QR Code display frame
        self.qr_frame = ttk.LabelFrame(self.main_frame, text="QR Code")
        self.qr_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # QR section frame - contains QR code and info button
        self.qr_section = ttk.Frame(self.qr_frame)
        self.qr_section.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # QR Code image label
        self.qr_image_label = tk.Label(self.qr_section, bg="white")
        self.qr_image_label.pack(side=tk.LEFT, expand=True)
        
        # Info button (i) next to QR code
        self.info_button_frame = ttk.Frame(self.qr_section)
        self.info_button_frame.pack(side=tk.RIGHT, padx=10)
        
        self.info_button = tk.Button(
            self.info_button_frame,
            text="i",
            font=("Arial", 12, "bold"),
            fg="white",
            bg=self.accent_color,
            width=2,
            height=1,
            borderwidth=0,
            command=self.show_info_popup,
            cursor="hand2"
        )
        self.info_button.pack(pady=5)
        
        # Add a small label under the i button
        info_label = tk.Label(
            self.info_button_frame,
            text="Info",
            font=("Arial", 8),
            fg=self.accent_color,
            bg=self.secondary_color
        )
        info_label.pack()
        
        # Initial message
        self.initial_message = tk.Label(
            self.qr_image_label,
            text="Fill the form and click 'Generate QR Code'",
            font=("Arial", 12),
            bg="white",
            fg=self.accent_color
        )
        self.initial_message.pack(pady=50)
        
        # Try to load saved info message and emergency number
        self.load_info_settings()
    
    def show_info_popup(self):
        """Show information popup with customized message and emergency number"""
        popup = tk.Toplevel(self.root)
        popup.title("Emergency Information")
        popup.geometry("400x200")
        popup.configure(bg=self.secondary_color)
        popup.resizable(False, False)
        
        # Make popup appear on top
        popup.transient(self.root)
        popup.grab_set()
        
        # Add some padding
        frame = ttk.Frame(popup, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Message label
        message_label = tk.Label(
            frame,
            text=self.info_message,
            font=("Arial", 12),
            wraplength=350,
            justify=tk.LEFT,
            bg=self.secondary_color
        )
        message_label.pack(pady=10, anchor=tk.W)
        
        # Emergency number frame
        emergency_frame = ttk.Frame(frame)
        emergency_frame.pack(fill=tk.X, pady=10)
        
        emergency_label = tk.Label(
            emergency_frame,
            text="Emergency Number:",
            font=("Arial", 12, "bold"),
            bg=self.secondary_color
        )
        emergency_label.pack(side=tk.LEFT)
        
        number_label = tk.Label(
            emergency_frame,
            text=self.emergency_number,
            font=("Arial", 14, "bold"),
            fg=self.primary_color,
            bg=self.secondary_color
        )
        number_label.pack(side=tk.LEFT, padx=10)
        
        # Close button
        close_button = tk.Button(
            frame,
            text="Close",
            command=popup.destroy,
            bg=self.accent_color,
            fg="white",
            font=("Arial", 12),
            padx=20
        )
        close_button.pack(pady=10)
        
        # Center the popup window on the screen
        popup.update_idletasks()
        width = popup.winfo_width()
        height = popup.winfo_height()
        x = (self.root.winfo_rootx() + (self.root.winfo_width() // 2)) - (width // 2)
        y = (self.root.winfo_rooty() + (self.root.winfo_height() // 2)) - (height // 2)
        popup.geometry(f"{width}x{height}+{x}+{y}")
    
    def open_settings(self):
        """Open settings dialog to configure info message and emergency number"""
        settings = tk.Toplevel(self.root)
        settings.title("Info Settings")
        settings.geometry("500x300")
        settings.configure(bg=self.secondary_color)
        settings.resizable(False, False)
        
        # Make settings appear on top
        settings.transient(self.root)
        settings.grab_set()
        
        # Add some padding
        frame = ttk.Frame(settings, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Info message label and text field
        message_label = tk.Label(
            frame,
            text="Custom Information Message:",
            font=("Arial", 12),
            anchor=tk.W
        )
        message_label.pack(fill=tk.X, pady=(0, 5))
        
        message_text = tk.Text(
            frame,
            height=5,
            width=50,
            font=("Arial", 11),
            wrap=tk.WORD
        )
        message_text.pack(fill=tk.X, pady=(0, 10))
        message_text.insert("1.0", self.info_message)
        
        # Emergency number label and entry
        number_frame = ttk.Frame(frame)
        number_frame.pack(fill=tk.X, pady=10)
        
        number_label = tk.Label(
            number_frame,
            text="Emergency Number:",
            font=("Arial", 12),
            width=20
        )
        number_label.pack(side=tk.LEFT)
        
        number_var = tk.StringVar(value=self.emergency_number)
        number_entry = ttk.Entry(
            number_frame,
            textvariable=number_var,
            width=20,
            font=("Arial", 11)
        )
        number_entry.pack(side=tk.LEFT, padx=5)
        
        # Buttons frame
        buttons_frame = ttk.Frame(frame)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        # Save button
        save_button = tk.Button(
            buttons_frame,
            text="Save",
            command=lambda: self.save_info_settings(message_text.get("1.0", tk.END).strip(), number_var.get()),
            bg=self.primary_color,
            fg="white",
            font=("Arial", 12),
            padx=20
        )
        save_button.pack(side=tk.LEFT, padx=5)
        
        # Cancel button
        cancel_button = tk.Button(
            buttons_frame,
            text="Cancel",
            command=settings.destroy,
            bg=self.accent_color,
            fg="white",
            font=("Arial", 12),
            padx=20
        )
        cancel_button.pack(side=tk.LEFT, padx=5)
        
        # Center the settings window on the screen
        settings.update_idletasks()
        width = settings.winfo_width()
        height = settings.winfo_height()
        x = (self.root.winfo_rootx() + (self.root.winfo_width() // 2)) - (width // 2)
        y = (self.root.winfo_rooty() + (self.root.winfo_height() // 2)) - (height // 2)
        settings.geometry(f"{width}x{height}+{x}+{y}")
    
    def save_info_settings(self, message, number):
        """Save the info message and emergency number"""
        self.info_message = message
        self.emergency_number = number
        
        # Save settings to a file
        try:
            settings_data = {
                "info_message": self.info_message,
                "emergency_number": self.emergency_number
            }
            
            with open("qr_info_settings.json", "w") as file:
                json.dump(settings_data, file)
                
            messagebox.showinfo("Settings Saved", "Your information settings have been saved.")
            
            # Close the settings window
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Toplevel) and widget.title() == "Info Settings":
                    widget.destroy()
                    break
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
    
    def load_info_settings(self):
        """Load saved info message and emergency number"""
        try:
            if os.path.exists("qr_info_settings.json"):
                with open("qr_info_settings.json", "r") as file:
                    settings_data = json.load(file)
                    self.info_message = settings_data.get("info_message", self.info_message)
                    self.emergency_number = settings_data.get("emergency_number", self.emergency_number)
        except Exception:
            # Silently handle errors, keep defaults
            pass
    
    def create_form_field(self, label_text, variable_name, height=1):
        """Create a form field with label and entry widget"""
        frame = ttk.Frame(self.input_frame)
        frame.pack(fill=tk.X, pady=5)
        
        label = ttk.Label(frame, text=label_text, width=25)
        label.pack(side=tk.LEFT)
        
        if height > 1:
            widget = tk.Text(frame, height=height, width=40)
            setattr(self, variable_name, widget)
        else:
            var = tk.StringVar()
            setattr(self, variable_name + "_var", var)
            widget = ttk.Entry(frame, textvariable=var, width=40)
        
        widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def get_form_data(self):
        """Collect all form data into a dictionary"""
        data = {}
        
        # Get data from StringVar fields
        for field in ["full_name", "dob", "blood_group", "emergency_contact_name", 
                      "emergency_contact_phone", "emergency_contact_relation", "address"]:
            var = getattr(self, field + "_var", None)
            if var:
                data[field] = var.get().strip()
        
        # Get data from Text fields
        for field in ["allergies", "medical_conditions", "medications", "additional_info"]:
            widget = getattr(self, field, None)
            if isinstance(widget, tk.Text):
                data[field] = widget.get("1.0", tk.END).strip()
            else:
                var = getattr(self, field + "_var", None)
                if var:
                    data[field] = var.get().strip()
        
        return data
    
    def validate_form_data(self, data):
        """Validate that essential fields are filled"""
        required_fields = ["full_name", "blood_group", "emergency_contact_name", "emergency_contact_phone"]
        
        for field in required_fields:
            if not data.get(field):
                messagebox.showerror("Validation Error", f"Please fill in the {field.replace('_', ' ')} field.")
                return False
        
        return True
    
    def generate_qr_code(self):
        """Generate QR code from form data"""
        data = self.get_form_data()
        
        if not self.validate_form_data(data):
            return
        
        # Create QR code data
        qr_data = {
            "type": "MEDICAL_EMERGENCY",
            "personal_info": {
                "name": data.get("full_name", ""),
                "dob": data.get("dob", ""),
                "blood_group": data.get("blood_group", "")
            },
            "medical_info": {
                "allergies": data.get("allergies", ""),
                "conditions": data.get("medical_conditions", ""),
                "medications": data.get("medications", "")
            },
            "emergency_contact": {
                "name": data.get("emergency_contact_name", ""),
                "phone": data.get("emergency_contact_phone", ""),
                "relationship": data.get("emergency_contact_relation", "")
            },
            "address": data.get("address", ""),
            "additional_info": data.get("additional_info", ""),
            "emergency_number": self.emergency_number
        }
        
        # Convert to JSON string
        qr_json = json.dumps(qr_data)
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_json)
        qr.make(fit=True)
        
        # Create QR code image
        self.qr_image = qr.make_image(fill_color="black", back_color="white")
        
        # Display QR code
        self.display_qr_code()
        
        # Enable save button
        self.save_button.config(state=tk.NORMAL)
    
    def display_qr_code(self):
        """Display the generated QR code"""
        if self.qr_image:
            # Remove initial message if it exists
            for widget in self.qr_image_label.winfo_children():
                widget.destroy()
            
            # Resize image for display
            img = self.qr_image.resize((250, 250), Image.LANCZOS)
            self.photo_image = ImageTk.PhotoImage(img)
            
            # Display image
            self.qr_image_label.config(image=self.photo_image)
            self.qr_image_label.image = self.photo_image  # Keep a reference
    
    def save_qr_code(self):
        """Save the QR code to a file"""
        if not self.qr_image:
            messagebox.showerror("Error", "No QR code has been generated yet.")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            title="Save QR Code"
        )
        
        if file_path:
            try:
                self.qr_image.save(file_path)
                messagebox.showinfo("Success", f"QR code saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save QR code: {str(e)}")
    
    def clear_form(self):
        """Clear all form fields"""
        # Clear StringVar fields
        for field in ["full_name", "dob", "blood_group", "emergency_contact_name", 
                      "emergency_contact_phone", "emergency_contact_relation", "address"]:
            var = getattr(self, field + "_var", None)
            if var:
                var.set("")
        
        # Clear Text fields
        for field in ["allergies", "medical_conditions", "medications", "additional_info"]:
            widget = getattr(self, field, None)
            if isinstance(widget, tk.Text):
                widget.delete("1.0", tk.END)
            else:
                var = getattr(self, field + "_var", None)
                if var:
                    var.set("")
        
        # Clear QR code display
        if self.qr_image_label:
            self.qr_image_label.config(image="")
            
            # Reinstate initial message
            self.initial_message = tk.Label(
                self.qr_image_label,
                text="Fill the form and click 'Generate QR Code'",
                font=("Arial", 12),
                bg="white",
                fg=self.accent_color
            )
            self.initial_message.pack(pady=50)
        
        # Disable save button
        self.save_button.config(state=tk.DISABLED)
        
        # Reset QR image
        self.qr_image = None
        self.photo_image = None

def main():
    root = tk.Tk()
    app = MedicalEmergencyQRGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()