#!/usr/bin/env python3
"""
Generate QR codes for all participants and check which ones have emails
"""

import pandas as pd
import hashlib
import qrcode
import os
from datetime import datetime

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
            
            # Clean activities data
            activities = row.get('activities', '')
            if isinstance(activities, str):
                if activities.startswith('["') and activities.endswith('"]'):
                    activities = activities.replace('"', '').replace('[', '').replace(']', '').split(',')
                elif activities:
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
        
        print(f"✅ Loaded {len(participants)} participants")
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
    
    # Save QR code
    filename = f"QR_{participant_name.replace(' ', '_')}.png"
    filepath = os.path.join('qr_codes', filename)
    img.save(filepath)
    
    return filepath

def generate_all_qr_codes():
    """Generate QR codes for all participants"""
    print("🔄 Generating QR codes for all participants...")
    print(f"🌐 Using Vercel URL: https://korean-week-qr.vercel.app")
    
    # Create qr_codes directory if it doesn't exist
    if not os.path.exists('qr_codes'):
        os.makedirs('qr_codes')
    
    # Load participants
    participants = load_participants()
    if not participants:
        print("❌ No participants loaded. Exiting.")
        return
    
    generated_files = []
    
    for participant in participants:
        print(f"📱 Generating QR code for {participant['fullName']}...")
        filepath = generate_qr_code(participant['id'], participant['fullName'])
        generated_files.append(filepath)
    
    print(f"\n🎉 Successfully generated {len(generated_files)} QR codes!")
    print("📁 QR codes saved in 'qr_codes' folder")
    print(f"🔗 Each QR code links to: https://korean-week-qr.vercel.app/user/[participant_id]")
    
    return generated_files

def check_emails():
    """Check which participants have emails"""
    print("\n📧 Checking email addresses...")
    
    participants = load_participants()
    if not participants:
        return
    
    # Separate participants with and without emails
    with_emails = []
    without_emails = []
    
    for p in participants:
        if p['email'] and '@' in p['email']:
            with_emails.append(p)
        else:
            without_emails.append(p)
    
    print(f"\n📊 Email Status Summary:")
    print(f"✅ Participants with emails: {len(with_emails)}")
    print(f"❌ Participants without emails: {len(without_emails)}")
    
    if with_emails:
        print(f"\n📧 Participants with emails (can send automatically):")
        for i, p in enumerate(with_emails, 1):
            print(f"{i:2d}. {p['fullName']} - {p['email']} - {p['selectedDay']}")
    
    if without_emails:
        print(f"\n📝 Participants without emails (need manual sending):")
        for i, p in enumerate(without_emails, 1):
            print(f"{i:2d}. {p['fullName']} - {p['selectedDay']}")
    
    # Save lists to files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if with_emails:
        with open(f"participants_with_emails_{timestamp}.txt", 'w', encoding='utf-8') as f:
            f.write("Participants with emails (can send automatically):\n")
            f.write("=" * 60 + "\n")
            for p in with_emails:
                f.write(f"Name: {p['fullName']}\n")
                f.write(f"Email: {p['email']}\n")
                f.write(f"Day: {p['selectedDay']}\n")
                f.write(f"Phone: {p['phone']}\n")
                f.write("-" * 40 + "\n")
        print(f"\n📄 List saved to: participants_with_emails_{timestamp}.txt")
    
    if without_emails:
        with open(f"participants_without_emails_{timestamp}.txt", 'w', encoding='utf-8') as f:
            f.write("Participants without emails (need manual sending):\n")
            f.write("=" * 60 + "\n")
            for p in without_emails:
                f.write(f"Name: {p['fullName']}\n")
                f.write(f"Day: {p['selectedDay']}\n")
                f.write(f"Phone: {p['phone']}\n")
                f.write("-" * 40 + "\n")
        print(f"📄 List saved to: participants_without_emails_{timestamp}.txt")

def main():
    print("🇰🇷 Korea Week 2025 - QR Code Generation & Email Check")
    print("=" * 60)
    
    # Generate QR codes
    generate_all_qr_codes()
    
    # Check emails
    check_emails()
    
    print(f"\n🎉 Process completed!")
    print("📱 All QR codes are ready in the 'qr_codes' folder")
    print("📧 Check the generated text files for email status")

if __name__ == "__main__":
    main()
