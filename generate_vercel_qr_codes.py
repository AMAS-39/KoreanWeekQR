#!/usr/bin/env python3
"""
Generate QR codes for Vercel deployment with consistent IDs
All QR codes will point to korean-week-qr.vercel.app
"""

import pandas as pd
import qrcode
import os
import hashlib

def load_participants():
    """Load participants from Excel file with consistent IDs"""
    try:
        df = pd.read_excel('korea_week_split(1).xlsx')
        participants = []
        
        for index, row in df.iterrows():
            # Generate consistent ID based on email and name
            email = row.get('email', '').strip()
            name = row.get('fullName', '').strip()
            
            # Create a consistent hash-based ID
            if email:
                # Use email as primary identifier
                id_string = email.lower()
            else:
                # Fallback to name if no email
                id_string = name.lower()
            
            # Generate consistent 8-character ID
            participant_id = hashlib.md5(id_string.encode()).hexdigest()[:8]
            
            # Clean activities data - handle both JSON format and single activities
            activities = row.get('activities', '')
            if isinstance(activities, str):
                if activities.startswith('["') and activities.endswith('"]'):
                    # JSON format: ["kimbap","taekwondo","makeup"]
                    activities = activities.replace('"', '').replace('[', '').replace(']', '').split(',')
                elif activities:
                    # Single activity: "kimbap" or "makeup"
                    activities = [activities.strip()]
                else:
                    activities = []
            else:
                activities = []
            
            participants.append({
                'id': participant_id,
                'fullName': name,
                'email': email,
                'phone': str(row.get('phone', '')),
                'city': row.get('city', ''),
                'selectedDay': row.get('selectedDay', ''),
                'activities': activities,
                'dietary': row.get('dietary', '')
            })
        
        print(f"✅ Loaded {len(participants)} participants with consistent IDs")
        return participants
    except Exception as e:
        print(f"❌ Error loading participants: {e}")
        return []

def generate_qr_code(participant_id, participant_name):
    """Generate QR code for a participant"""
    # Create QR code with the Vercel URL
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
    
    # Create QR codes directory if it doesn't exist
    if not os.path.exists('vercel_qr_codes'):
        os.makedirs('vercel_qr_codes')
    
    # Save QR code image
    filename = f"vercel_qr_codes/QR_{participant_name.replace(' ', '_').replace('/', '_')}.png"
    img.save(filename)
    
    return filename

def generate_all_qr_codes():
    """Generate QR codes for all participants"""
    print("🔄 Generating QR codes for Vercel deployment...")
    print("🌐 Using URL: https://korean-week-qr.vercel.app")
    
    participants = load_participants()
    if not participants:
        print("❌ No participants loaded. Exiting.")
        return
    
    generated_files = []
    for participant in participants:
        filename = generate_qr_code(participant['id'], participant['fullName'])
        generated_files.append(filename)
        print(f"✅ Generated: {filename} (ID: {participant['id']})")
    
    print(f"\n🎉 Successfully generated {len(generated_files)} QR codes!")
    print("📁 QR codes saved in 'vercel_qr_codes' folder")
    print("🔗 All QR codes point to: https://korean-week-qr.vercel.app")
    
    # Save participant mapping for reference
    mapping_file = "participant_mapping.txt"
    with open(mapping_file, 'w', encoding='utf-8') as f:
        f.write("Participant ID Mapping for Vercel Deployment\n")
        f.write("=" * 50 + "\n\n")
        for participant in participants:
            f.write(f"ID: {participant['id']}\n")
            f.write(f"Name: {participant['fullName']}\n")
            f.write(f"Email: {participant['email']}\n")
            f.write(f"URL: https://korean-week-qr.vercel.app/user/{participant['id']}\n")
            f.write("-" * 30 + "\n")
    
    print(f"📄 Participant mapping saved to: {mapping_file}")
    
    return generated_files

if __name__ == "__main__":
    generate_all_qr_codes()
