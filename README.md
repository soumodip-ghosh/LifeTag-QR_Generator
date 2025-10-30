# LifeTag: Emergency QR Code Generator

> A digital tool that embeds offline QR codes into phone wallpapers with critical medical and emergency information.

---

## 🌟 Features

- **Offline QR Code** - Access medical info without internet
- **Privacy-First** - All data stored locally, no cloud storage
- **Emergency Button** - Quick access to contacts without scanning
- **Customizable** - Add blood group, allergies, medications, and emergency contacts
- **Beautiful Wallpapers** - Standard or flower-themed designs
- **Easy Export** - Save as phone wallpaper (PNG/JPEG)

---

## 📋 Requirements

```bash
Python 3.9+
tkinter
qrcode==7.4.2
Pillow==9.5.0
```

---

## 🚀 Quick Start

### Installation
```bash
# Clone the repository
git clone https://github.com/soumodip-ghosh/LifeTag-QR_Generator.git
cd LifeTag-QR_Generator

# Install dependencies
pip install qrcode[pil] Pillow

# Run the application
python QRGenerator.py
```

### Usage
1. Fill in your medical information (Name, Blood Group, Emergency Contact)
2. Click "Generate QR Code"
3. Save the wallpaper and set it as your lock screen

---

## 📱 Versions

### Standard Version (`QRGenerator.py`)
- Clean medical-themed interface
- Emergency "i" button feature
- Compact design

### Flower-Themed (`QRGenerator_floral.py`)
- Decorative floral design
- 1080x1920 phone wallpaper
- Beautiful aesthetic

---

## 🔒 Privacy

- ✅ No internet required
- ✅ No cloud storage
- ✅ Complete user control
- ✅ Local data only

---

## 📊 QR Code Data

```json
{
  "type": "MEDICAL_EMERGENCY",
  "personal_info": {"name": "", "dob": "", "blood_group": ""},
  "medical_info": {"allergies": "", "conditions": "", "medications": ""},
  "emergency_contact": {"name": "", "phone": "", "relationship": ""},
  "address": "",
  "additional_info": ""
}
```

---

## 🛠️ Technology Stack

- **Python** - Core language
- **Tkinter** - GUI framework
- **QRCode** - QR generation with error correction
- **Pillow** - Image processing

---

## 👥 Team

**MCKV Institute of Engineering - CSE Department**

- Soumodip Ghosh (BTECH/CSE/23/106) (11600223113)
- Shadab Ali (11600223099)
- Nitesh Shaw (11600223070)
- Sovona Rana (11600223116)
- Debatwik Santra (BTECH/CSE/23/110) (11600223047)

**Guide:** Mr. Milan Chakrabortty

---

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

---
