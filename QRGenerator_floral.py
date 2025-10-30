import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import qrcode
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageColor
import json
import os
import math
import random
from io import BytesIO


class MedicalEmergencyQRGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Flower-Themed Medical Emergency QR Generator")
        self.root.geometry("800x850")
        self.root.resizable(True, True)
        
        # Set flower theme colors
        self.primary_color = "#FF97BB"    # Pink flower
        self.secondary_color = "#F9F5E7"  # Soft cream background
        self.accent_color = "#88B04B"     # Green leaf
        self.highlight_color = "#FFCBA4"  # Peach accent
        
        self.root.configure(bg=self.secondary_color)
        
        # Variables for storing information
        self.qr_image = None
        self.photo_image = None
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            self.main_frame, 
            text="Flower-Themed Medical Emergency QR", 
            font=("Georgia", 18, "bold"),
            fg=self.primary_color,
            bg=self.secondary_color
        )
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(
            self.main_frame,
            text="Beautiful Wallpaper with Emergency Information",
            font=("Georgia", 12, "italic"),
            fg=self.accent_color,
            bg=self.secondary_color
        )
        subtitle_label.pack(pady=5)
        
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
            text="Generate Flower QR",
            command=self.generate_qr_code,
            bg=self.primary_color,
            fg="white",
            font=("Georgia", 12),
            relief=tk.RAISED,
            padx=10,
            pady=5
        )
        self.generate_button.pack(side=tk.LEFT, padx=5)
        
        # Save button
        self.save_button = tk.Button(
            self.buttons_frame,
            text="Save as Wallpaper",
            command=self.save_qr_code,
            bg=self.accent_color,
            fg="white",
            font=("Georgia", 12),
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
            bg=self.highlight_color,
            fg="white",
            font=("Georgia", 12),
            relief=tk.RAISED,
            padx=10,
            pady=5
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # QR Code display frame
        self.qr_frame = ttk.LabelFrame(self.main_frame, text="Flower QR Wallpaper Preview")
        self.qr_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # QR Code image label with scrollbars for larger wallpaper preview
        self.qr_canvas = tk.Canvas(self.qr_frame, bg=self.secondary_color)
        self.qr_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(self.qr_frame, orient=tk.VERTICAL, command=self.qr_canvas.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar = ttk.Scrollbar(self.qr_frame, orient=tk.HORIZONTAL, command=self.qr_canvas.xview)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.qr_canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Create a frame inside canvas to hold the image
        self.qr_image_frame = tk.Frame(self.qr_canvas, bg=self.secondary_color)
        self.qr_canvas.create_window((0, 0), window=self.qr_image_frame, anchor=tk.NW)
        
        # QR Code image label
        self.qr_image_label = tk.Label(self.qr_image_frame, bg=self.secondary_color)
        self.qr_image_label.pack(pady=10, expand=True)
        
        # Initial message
        self.initial_message = tk.Label(
            self.qr_image_label,
            text="Fill the form and click 'Generate Flower QR'",
            font=("Georgia", 14),
            bg=self.secondary_color,
            fg=self.primary_color
        )
        self.initial_message.pack(pady=50)
        
        # Add a description label
        description_text = (
            "This app creates a beautiful flower-themed wallpaper\n"
            "with an embedded QR code containing your medical emergency information.\n"
            "The emergency contact number will be clearly visible on the wallpaper."
        )
        
        self.description_label = tk.Label(
            self.qr_image_frame,
            text=description_text,
            font=("Georgia", 10),
            bg=self.secondary_color,
            fg=self.accent_color,
            justify=tk.CENTER
        )
        self.description_label.pack(pady=10)
    
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
            "additional_info": data.get("additional_info", "")
        }
        
        # Convert to JSON string
        qr_json = json.dumps(qr_data)
        
        # Generate QR code with higher error correction for better design flexibility
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,  # Higher error correction
            box_size=10,
            border=4,
        )
        qr.add_data(qr_json)
        qr.make(fit=True)
        
        # Create QR code image with custom colors
        self.qr_image = qr.make_image(fill_color="#060364", back_color="#F9F5E7")
        
        # Apply flower theme to QR code
        self.apply_flower_theme(data.get("emergency_contact_phone", ""))
        
        # Display QR code
        self.display_qr_code()
        
        # Enable save button
        self.save_button.config(state=tk.NORMAL)
    
    def apply_flower_theme(self, phone_number):
        """Apply flower theme to the QR code and add emergency phone number"""
        if not self.qr_image:
            return
            
        # Convert to RGBA if not already
        if self.qr_image.mode != 'RGBA':
            self.qr_image = self.qr_image.convert('RGBA')
            
        # Create a larger canvas for the wallpaper (16:9 ratio for phones)
        width, height = 1080, 1920  # Standard phone wallpaper size
        wallpaper = Image.new('RGBA', (width, height), (249, 245, 231, 255))  # Soft cream background
        
        # Calculate QR code size (about 1/3 of wallpaper width)
        qr_size = width // 2
        qr_resized = self.qr_image.resize((qr_size, qr_size), Image.LANCZOS)
        
        # Place QR code in the center of the upper third
        qr_position = ((width - qr_size) // 2, height // 4 - qr_size // 2)
        wallpaper.paste(qr_resized, qr_position, qr_resized)
        
        # Add decorative flower elements
        self.add_flower_decorations(wallpaper)
        
        # Add emergency contact information in a decorative banner
        self.add_emergency_contact_banner(wallpaper, phone_number)
        
        # Add medical emergency text
        self.add_medical_emergency_text(wallpaper)
        
        # Save the final wallpaper
        self.qr_image = wallpaper

    def add_flower_decorations(self, image):
        """Add flower decorations around the QR code"""
        width, height = image.size
        draw = ImageDraw.Draw(image)
        
        # Generate flower positions in a circular arrangement around the QR code
        center_x, center_y = width // 2, height // 4
        radius = min(width, height) // 3
        
        # Draw multiple flowers
        for i in range(12):
            angle = math.radians(i * 30)
            x = center_x + int(radius * math.cos(angle))
            y = center_y + int(radius * math.sin(angle))
            
            # Determine flower size
            flower_size = random.randint(30, 60)
            
            # Choose flower color
            flower_colors = [
                (255, 182, 193, 200),  # Light pink
                (255, 151, 187, 200),  # Pink
                (221, 160, 221, 200),  # Plum
                (255, 192, 203, 200),  # Pink
                (255, 228, 225, 200),  # Misty rose
            ]
            
            color = random.choice(flower_colors)
            
            # Draw a flower (simplified as overlapping circles)
            self.draw_flower(draw, x, y, flower_size, color)
        
        # Add some small flowers at the bottom
        for i in range(20):
            x = random.randint(0, width)
            y = random.randint(height // 2, height - 100)
            
            flower_size = random.randint(15, 30)
            color = random.choice(flower_colors)
            
            self.draw_flower(draw, x, y, flower_size, color)
    
    def draw_flower(self, draw, x, y, size, color):
        """Draw a simple flower using circles"""
        # Draw petals
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            offset = size // 2
            px = x + int(offset * math.cos(rad))
            py = y + int(offset * math.sin(rad))
            
            # Draw petal
            draw.ellipse((px - size//2, py - size//2, px + size//2, py + size//2), fill=color)
        
        # Draw center
        center_color = (255, 215, 0, 230)  # Gold center
        draw.ellipse((x - size//3, y - size//3, x + size//3, y + size//3), fill=center_color)
    
    def add_emergency_contact_banner(self, image, phone_number):
        """Add emergency contact information in a decorative banner"""
        width, height = image.size
        draw = ImageDraw.Draw(image)
        
        # Banner position (below QR code)
        banner_y = height // 2
        banner_height = 120
        
        # Create banner background
        banner_rect = [0, banner_y, width, banner_y + banner_height]
        draw.rectangle(banner_rect, fill=(255, 151, 187, 200))  # Semi-transparent pink
        
        # Add decorative edges
        edge_height = 20
        for i in range(edge_height):
            alpha = 150 * (1 - i/edge_height)
            edge_color = (255, 151, 187, int(alpha))
            draw.rectangle([0, banner_y - i, width, banner_y - i + 1], fill=edge_color)
            draw.rectangle([0, banner_y + banner_height + i - 1, width, banner_y + banner_height + i], fill=edge_color)
        
        # Add emergency text
        try:
            # Try to load a nice font, fall back to default if not available
            font_large = ImageFont.truetype("Georgia", 48)
            font_small = ImageFont.truetype("Georgia", 36)
        except IOError:
            # Use default font if custom font not available
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Add "EMERGENCY CONTACT" text
        text = "EMERGENCY CONTACT"
        draw.text((width//2, banner_y + 20), text, fill=(255, 255, 255), font=font_small, anchor="mm")
        
        # Add phone number in larger, bold font
        draw.text((width//2, banner_y + 70), phone_number, fill=(255, 255, 255), font=font_large, anchor="mm")
        
    def add_medical_emergency_text(self, image):
        """Add medical emergency text at the top of the image"""
        width, height = image.size
        draw = ImageDraw.Draw(image)
        
        try:
            font = ImageFont.truetype("Georgia", 42)
        except IOError:
            font = ImageFont.load_default()
            
        text = "MEDICAL EMERGENCY INFO"
        text_width, text_height = draw.textsize(text, font=font) if hasattr(draw, 'textsize') else (400, 50)
        
        # Position text at the top
        y_position = height // 10
        
        # Add a slight glow effect
        for offset in range(3, 0, -1):
            draw.text((width//2 - text_width//2 + offset, y_position + offset), 
                      text, fill=(0, 0, 0, 50), font=font)
        
        # Draw main text
        draw.text((width//2, y_position), text, fill=(136, 176, 75), font=font, anchor="mm")

    def display_qr_code(self):
        """Display the generated QR code"""
        if self.qr_image:
            # Remove all widgets from the QR image frame
            for widget in self.qr_image_frame.winfo_children():
                widget.destroy()
            
            # Hide description label if it exists
            if hasattr(self, 'description_label') and self.description_label:
                self.description_label.pack_forget()
            
            # Resize image for display while maintaining aspect ratio
            display_width = 400
            aspect_ratio = self.qr_image.height / self.qr_image.width
            display_height = int(display_width * aspect_ratio)
            
            img = self.qr_image.resize((display_width, display_height), Image.LANCZOS)
            self.photo_image = ImageTk.PhotoImage(img)
            
            # Display image in the label
            self.qr_image_label = tk.Label(self.qr_image_frame, image=self.photo_image, bg=self.secondary_color)
            self.qr_image_label.image = self.photo_image  # Keep a reference
            self.qr_image_label.pack(pady=10)
            
            # Update canvas scroll region
            self.qr_image_frame.update_idletasks()
            self.qr_canvas.config(scrollregion=self.qr_canvas.bbox("all"))
            
            # Center the content in the canvas
            self.center_frame_in_canvas()
    
    def save_qr_code(self):
        """Save the QR code to a file"""
        if not self.qr_image:
            messagebox.showerror("Error", "No QR code wallpaper has been generated yet.")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
            title="Save Flower QR Wallpaper"
        )
        
        if file_path:
            try:
                # For JPEG format, convert to RGB (no alpha channel)
                if file_path.lower().endswith('.jpg') or file_path.lower().endswith('.jpeg'):
                    if self.qr_image.mode == 'RGBA':
                        rgb_image = Image.new('RGB', self.qr_image.size, (255, 255, 255))
                        rgb_image.paste(self.qr_image, mask=self.qr_image.split()[3])
                        rgb_image.save(file_path, quality=95)
                    else:
                        self.qr_image.save(file_path, quality=95)
                else:
                    self.qr_image.save(file_path)
                    
                messagebox.showinfo("Success", 
                    f"Flower QR wallpaper saved to {file_path}\n\n"
                    f"Set this image as your phone's lock screen wallpaper for emergency access."
                )
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save wallpaper: {str(e)}")
    
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
            
            # Remove all widgets from the QR image label
            for widget in self.qr_image_label.winfo_children():
                widget.destroy()
            
            # Reinstate initial message
            self.initial_message = tk.Label(
                self.qr_image_label,
                text="Fill the form and click 'Generate Flower QR'",
                font=("Georgia", 14),
                bg=self.secondary_color,
                fg=self.primary_color
            )
            self.initial_message.pack(pady=50)
            
            # Reset description visibility
            self.description_label.pack(pady=10)
        
        # Disable save button
        self.save_button.config(state=tk.DISABLED)
        
        # Reset QR image
        self.qr_image = None
        self.photo_image = None
        
        # Show confirmation
        messagebox.showinfo("Form Cleared", "All form fields have been cleared.")

def main():
    root = tk.Tk()
    app = MedicalEmergencyQRGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()   