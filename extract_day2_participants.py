#!/usr/bin/env python3
"""
Extract participants from Day2 sheet and generate QR codes
"""

import pandas as pd
import qrcode
import hashlib
import os
from datetime import datetime

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
    filename = f"qr_codes/day2_{participant_name.replace(' ', '_')}_{participant_id}.png"
    img.save(filename)
    print(f"✅ Generated QR code: {filename}")
    return filename

def main():
    print("🔍 Extracting participants from Day2 sheet...")
    
    try:
        # Read the Day2 sheet
        df = pd.read_excel('korea_week_split(1).xlsx', sheet_name='Day2')
        print(f"📊 Found {len(df)} participants in Day2 sheet")
        
        # Create qr_codes directory if it doesn't exist
        if not os.path.exists('qr_codes'):
            os.makedirs('qr_codes')
        
        # Create a list to store participant data
        day2_participants = []
        
        print("\n🔗 Generating QR codes for Day2 participants...")
        
        for index, row in df.iterrows():
            try:
                # Get basic info
                name = str(row.get('fullName', '')).strip()
                email = str(row.get('email', '')).strip()
                
                # Skip empty rows
                if not name or name == 'nan':
                    continue
                
                # Generate ID using the same logic as main system
                if email and email != 'nan' and '@' in email:
                    id_string = email.lower()
                else:
                    id_string = name.lower()
                
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
                
                # Clean dietary data
                dietary = row.get('dietary', '')
                if dietary == 'nan' or not dietary:
                    dietary = None
                
                # Store participant data
                participant_data = {
                    'id': participant_id,
                    'fullName': name,
                    'age': row.get('age', ''),
                    'email': email,
                    'phone': str(row.get('phone', '')),
                    'city': row.get('city', ''),
                    'selectedDay': 'day2',  # Set to day2
                    'activities': activities,
                    'dietary': dietary,
                    'emergencyName': row.get('emergencyName', ''),
                    'emergencyPhone': str(row.get('emergencyPhone', '')),
                    'emergencyRelation': row.get('emergencyRelation', '')
                }
                
                day2_participants.append(participant_data)
                
                print(f"📝 Processing: {name}")
                print(f"🆔 Generated ID: {participant_id}")
                print(f"📧 Email: {email}")
                
                # Generate QR code
                filename = generate_qr_code(participant_id, name)
                
                print(f"🔗 QR Code URL: https://korean-week-qr.vercel.app/user/{participant_id}")
                print("---")
                
            except Exception as e:
                print(f"❌ Error processing row {index}: {e}")
                continue
        
        print(f"\n✅ Successfully processed {len(day2_participants)} Day2 participants!")
        
        # Save participant data to a file for reference
        import json
        with open('day2_participants.json', 'w', encoding='utf-8') as f:
            json.dump(day2_participants, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Participant data saved to: day2_participants.json")
        
        # Create a summary file
        with open('day2_summary.txt', 'w', encoding='utf-8') as f:
            f.write(f"Day2 Participants Summary - Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Total Participants: {len(day2_participants)}\n\n")
            
            for i, participant in enumerate(day2_participants, 1):
                f.write(f"{i}. {participant['fullName']}\n")
                f.write(f"   ID: {participant['id']}\n")
                f.write(f"   Email: {participant['email']}\n")
                f.write(f"   Phone: {participant['phone']}\n")
                f.write(f"   Activities: {', '.join(participant['activities']) if participant['activities'] else 'None'}\n")
                f.write(f"   QR Code: day2_{participant['fullName'].replace(' ', '_')}_{participant['id']}.png\n")
                f.write(f"   URL: https://korean-week-qr.vercel.app/user/{participant['id']}\n")
                f.write("-" * 40 + "\n")
        
        print(f"📄 Summary saved to: day2_summary.txt")
        
        print("\n🎉 Day2 QR Code generation completed!")
        print(f"📁 QR codes saved in: qr_codes/ folder")
        print(f"📊 Total Day2 participants: {len(day2_participants)}")
        
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")
        print("Make sure the Excel file has a sheet named 'Day2'")

if __name__ == "__main__":
    main()
