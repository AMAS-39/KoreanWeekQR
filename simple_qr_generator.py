#!/usr/bin/env python3
"""
Simple QR Code Generator - Just creates QR code images
No web server, just generates QR codes for all participants
"""

import pandas as pd
import qrcode
import os
import uuid

def load_participants():
    """Load participants from Excel file"""
    try:
        df = pd.read_excel('korea_week_split(1).xlsx')
        participants = []
        
        for index, row in df.iterrows():
            # Generate unique ID for each participant
            participant_id = str(uuid.uuid4())[:8]
            
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
            
            participant = {
                'id': participant_id,
                'fullName': row.get('fullName', ''),
                'age': row.get('age', ''),
                'email': row.get('email', ''),
                'phone': str(row.get('phone', '')),
                'city': row.get('city', ''),
                'selectedDay': row.get('selectedDay', ''),
                'activities': activities,
                'dietary': row.get('dietary', ''),
                'emergencyName': row.get('emergencyName', ''),
                'emergencyPhone': str(row.get('emergencyPhone', '')),
                'emergencyRelation': row.get('emergencyRelation', '')
            }
            
            participants.append(participant)
        
        print(f"✅ Loaded {len(participants)} participants")
        return participants
    except Exception as e:
        print(f"❌ Error loading participants: {e}")
        return []

def generate_qr_code(participant, qr_type="url"):
    """Generate QR code for a participant"""
    
    if qr_type == "url":
        # QR code with URL to web page
        qr_data = f"http://localhost:5000/user/{participant['id']}"
    elif qr_type == "data":
        # QR code with participant data directly
        qr_data = f"""
Name: {participant['fullName']}
Email: {participant['email']}
Phone: {participant['phone']}
City: {participant['city']}
Day: {participant['selectedDay']}
Activities: {', '.join(participant['activities'])}
        """.strip()
    else:
        # QR code with JSON data
        import json
        qr_data = json.dumps(participant, indent=2)
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    # Create QR code image
    img = qr.make_image(fill_color="black", back_color="white")
    
    return img

def generate_all_qr_codes(qr_type="url"):
    """Generate QR codes for all participants"""
    print(f"🔄 Generating QR codes (type: {qr_type}) for all participants...")
    
    # Load participants
    participants = load_participants()
    if not participants:
        print("❌ No participants loaded. Exiting.")
        return
    
    # Create QR codes directory
    qr_dir = f"qr_codes_{qr_type}"
    if not os.path.exists(qr_dir):
        os.makedirs(qr_dir)
    
    # Generate QR codes
    generated_files = []
    for participant in participants:
        # Generate QR code
        qr_img = generate_qr_code(participant, qr_type)
        
        # Save QR code
        filename = f"{qr_dir}/QR_{participant['fullName'].replace(' ', '_').replace('/', '_')}.png"
        qr_img.save(filename)
        generated_files.append(filename)
        
        print(f"✅ Generated: {filename}")
    
    print(f"\n🎉 Successfully generated {len(generated_files)} QR codes!")
    print(f"📁 QR codes saved in '{qr_dir}' folder")
    
    if qr_type == "url":
        print("🔗 Each QR code links to: http://localhost:5000/user/[participant_id]")
        print("💡 Make sure to run the web server to view participant data!")
    elif qr_type == "data":
        print("📋 Each QR code contains participant data directly")
    else:
        print("📄 Each QR code contains JSON data")
    
    return generated_files

def main():
    """Main function"""
    print("🚀 Korea Week QR Code Generator")
    print("=" * 40)
    
    print("\nChoose QR code type:")
    print("1. URL (links to web page) - Recommended")
    print("2. Data (contains participant info directly)")
    print("3. JSON (contains all data in JSON format)")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        qr_type = "url"
    elif choice == "2":
        qr_type = "data"
    elif choice == "3":
        qr_type = "json"
    else:
        print("Invalid choice. Using URL type.")
        qr_type = "url"
    
    # Generate QR codes
    generate_all_qr_codes(qr_type)
    
    print("\n✅ Done! QR codes are ready to use.")
    
    if qr_type == "url":
        print("\n🌐 To view participant data when scanning:")
        print("1. Run: python generate_qr_codes.py")
        print("2. Open: http://localhost:5000")
        print("3. Scan any QR code with your phone")

if __name__ == "__main__":
    main()
