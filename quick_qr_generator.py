#!/usr/bin/env python3
"""
Quick QR Code Generator and Email Checker
"""

import pandas as pd
import hashlib
import qrcode
import os

def main():
    print("🇰🇷 Korea Week 2025 - Quick QR Generator")
    print("=" * 50)
    
    try:
        # Load data
        print("📊 Loading participant data...")
        df = pd.read_excel('korea_week_split(1).xlsx')
        print(f"✅ Loaded {len(df)} participants")
        
        # Create qr_codes directory
        if not os.path.exists('qr_codes'):
            os.makedirs('qr_codes')
        
        # Generate QR codes
        print("\n📱 Generating QR codes...")
        generated_count = 0
        
        for index, row in df.iterrows():
            name = str(row.get('fullName', '')).strip()
            email = str(row.get('email', '')).strip()
            
            if not name or name == 'nan':
                continue
            
            # Generate ID
            if email:
                id_string = email.lower()
            else:
                id_string = name.lower()
            
            participant_id = hashlib.md5(id_string.encode()).hexdigest()[:8]
            
            # Generate QR code
            qr_url = f"https://korean-week-qr.vercel.app/user/{participant_id}"
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
            qr.add_data(qr_url)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            filename = f"QR_{name.replace(' ', '_')}.png"
            filepath = os.path.join('qr_codes', filename)
            img.save(filepath)
            
            generated_count += 1
            print(f"✅ Generated QR for: {name}")
        
        print(f"\n🎉 Generated {generated_count} QR codes!")
        
        # Check emails
        print("\n📧 Checking email addresses...")
        with_emails = []
        without_emails = []
        
        for index, row in df.iterrows():
            name = str(row.get('fullName', '')).strip()
            email = str(row.get('email', '')).strip()
            day = str(row.get('selectedDay', '')).strip()
            
            if not name or name == 'nan':
                continue
                
            if email and '@' in email and email != 'nan':
                with_emails.append((name, email, day))
            else:
                without_emails.append((name, day))
        
        print(f"✅ Participants with emails: {len(with_emails)}")
        print(f"❌ Participants without emails: {len(without_emails)}")
        
        # Save lists
        with open('participants_with_emails.txt', 'w', encoding='utf-8') as f:
            f.write("Participants with emails (can send automatically):\n")
            f.write("=" * 60 + "\n")
            for name, email, day in with_emails:
                f.write(f"Name: {name}\nEmail: {email}\nDay: {day}\n")
                f.write("-" * 40 + "\n")
        
        with open('participants_without_emails.txt', 'w', encoding='utf-8') as f:
            f.write("Participants without emails (need manual sending):\n")
            f.write("=" * 60 + "\n")
            for name, day in without_emails:
                f.write(f"Name: {name}\nDay: {day}\n")
                f.write("-" * 40 + "\n")
        
        print("\n📄 Lists saved to:")
        print("  - participants_with_emails.txt")
        print("  - participants_without_emails.txt")
        
        print("\n🎉 Process completed!")
        print("📱 QR codes are in the 'qr_codes' folder")
        print("📧 Check the text files for email status")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
