#!/usr/bin/env python3
"""
Generate QR codes for additional names
"""

import qrcode
import hashlib
import os

def generate_qr_code(participant_id, participant_name):
    """Generate QR code for a participant"""
    # Use the Vercel URL
    qr_url = f"https://korean-week-qr.vercel.app/user/{participant_id}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_url)
    qr.make(fit=True)
    
    # Create QR code image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save to file
    filename = f"qr_codes/{participant_name.replace(' ', '_')}_{participant_id}.png"
    img.save(filename)
    print(f"✅ Generated QR code: {filename}")
    return filename

def main():
    # Additional names
    additional_names = [
        "Qabil hadi aji mam",
        "lawand qabil hadi"
    ]
    
    # Create qr_codes directory if it doesn't exist
    if not os.path.exists('qr_codes'):
        os.makedirs('qr_codes')
    
    print("🔗 Generating QR codes for additional names...")
    
    for name in additional_names:
        # Generate ID using the same logic as the main system
        # Since these don't have emails, use name as identifier
        id_string = name.lower()
        participant_id = hashlib.md5(id_string.encode()).hexdigest()[:8]
        
        print(f"📝 Processing: {name}")
        print(f"🆔 Generated ID: {participant_id}")
        
        # Generate QR code
        filename = generate_qr_code(participant_id, name)
        
        print(f"🔗 QR Code URL: https://korean-week-qr.vercel.app/user/{participant_id}")
        print("---")
    
    print("✅ All QR codes generated successfully!")
    print("\n📋 Summary:")
    for name in additional_names:
        id_string = name.lower()
        participant_id = hashlib.md5(id_string.encode()).hexdigest()[:8]
        print(f"• {name} → ID: {participant_id}")

if __name__ == "__main__":
    main()
