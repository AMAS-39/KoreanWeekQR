#!/usr/bin/env python3
"""
WhatsApp Message Generator for Korea Week QR Code Invitations
Creates personalized WhatsApp messages with QR codes for all participants
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
                id_string = email.lower()
            else:
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
    
    # Create WhatsApp QR codes directory if it doesn't exist
    if not os.path.exists('whatsapp_qr_codes'):
        os.makedirs('whatsapp_qr_codes')
    
    # Save QR code image
    filename = f"whatsapp_qr_codes/QR_{participant_name.replace(' ', '_').replace('/', '_')}.png"
    img.save(filename)
    
    return filename

def create_whatsapp_message(participant):
    """Create WhatsApp message in English and Sorani Kurdish"""
    
    # Format activities for display
    activities_text = ", ".join(participant['activities']) if participant['activities'] else "Not specified"
    
    # English Message
    english_message = f"""🇰🇷 *Korea Week 2025 - Your Personal Invitation*

Dear {participant['fullName']},

You are cordially invited to participate in *Korea Week 2025*! This exciting event celebrates Korean culture, traditions, and modern innovations.

*Your Event Details:*
• Name: {participant['fullName']}
• Email: {participant['email']}
• Phone: {participant['phone']}
• City: {participant['city']}
• Selected Day: {participant['selectedDay']}
• Activities: {activities_text}
{f"• Dietary Requirements: {participant['dietary']}" if participant['dietary'] else ""}

*Your Personal QR Code:*
I've attached your personal QR code. Scan it at the event entrance to access your digital pass and check-in.

*How to Use Your QR Code:*
1. Save the QR code image
2. Present it at the event entrance
3. Staff will scan it to check you in
4. Your digital pass will display all your details

We look forward to seeing you at Korea Week 2025! Get ready for an amazing experience filled with Korean culture, food, music, and activities.

*Korea Week 2025 Organizing Committee*
📧 ahmadshwanaswad@gmail.com
🌐 korean-week-qr.vercel.app"""

    # Sorani Kurdish Message
    kurdish_message = f"""🇰🇷 *هەفتەی کۆریا ٢٠٢٥ - دەرگای تایبەتەکەت*

سڵاو {participant['fullName']}،

بە دڵخۆشی دەتەوێت بانگێشت بکەین بۆ بەشداریکردن لە *هەفتەی کۆریا ٢٠٢٥*! ئەم ڕووداوە سەرنجڕاکێشە کۆڵتوری کۆریا، نەریتەکان و نوێکارییە مۆدێرنەکان جێگەدەکات.

*وردەکارییەکانی ڕووداوەکەت:*
• ناو: {participant['fullName']}
• ئیمەیڵ: {participant['email']}
• ژمارەی مۆبایل: {participant['phone']}
• شار: {participant['city']}
• ڕۆژی هەڵبژێردراو: {participant['selectedDay']}
• چالاکییەکان: {activities_text}
{f"• پێویستییە خۆراکییەکان: {participant['dietary']}" if participant['dietary'] else ""}

*کۆدی QR تایبەتەکەت:*
کۆدی QR تایبەتەکەت هەڵگرتوومە. لە دەرگای ڕووداوەکەدا سکان بکە بۆ دەستگەیشتن بە پاسە دیجیتاڵەکەت و چێککردن.

*چۆن کۆدی QR بەکاربهێنیت:*
1. وێنەی کۆدی QR هەڵبگرە
2. لە دەرگای ڕووداوەکەدا پیشانی بدە
3. ستاف سکان دەکات بۆ چێککردنت
4. پاسە دیجیتاڵەکەت هەموو وردەکارییەکان پیشان دەدات

چاوەڕوانین ببینین لە هەفتەی کۆریا ٢٠٢٥! ئامادە بە بۆ ئەزموونێکی سەرنجڕاکێش پڕ لە کۆڵتوری کۆریا، خۆراک، مۆسیقا و چالاکییەکان.

*کۆمیتەی ڕێکخستنی هەفتەی کۆریا ٢٠٢٥*
📧 ahmadshwanaswad@gmail.com
🌐 korean-week-qr.vercel.app"""

    return english_message, kurdish_message

def generate_all_whatsapp_messages():
    """Generate WhatsApp messages and QR codes for all participants"""
    print("🚀 Starting WhatsApp message generation...")
    
    # Load participants
    participants = load_participants()
    if not participants:
        print("❌ No participants loaded. Exiting.")
        return
    
    # Filter participants with valid phone numbers
    valid_participants = [p for p in participants if p['phone'] and len(p['phone']) > 5]
    print(f"📊 Found {len(valid_participants)} participants with valid phone numbers")
    
    if not valid_participants:
        print("❌ No participants with valid phone numbers found.")
        return
    
    # Generate messages and QR codes
    successful_generations = 0
    failed_generations = 0
    
    # Create messages directory
    if not os.path.exists('whatsapp_messages'):
        os.makedirs('whatsapp_messages')
    
    for i, participant in enumerate(valid_participants, 1):
        print(f"\n📱 Generating message {i}/{len(valid_participants)} for {participant['fullName']}...")
        
        try:
            # Generate QR code
            qr_filename = generate_qr_code(participant['id'], participant['fullName'])
            
            # Create messages
            english_msg, kurdish_msg = create_whatsapp_message(participant)
            
            # Save messages to file
            safe_name = participant['fullName'].replace(' ', '_').replace('/', '_')
            msg_filename = f"whatsapp_messages/message_{safe_name}.txt"
            
            with open(msg_filename, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write(f"KOREA WEEK 2025 - WHATSAPP MESSAGE\n")
                f.write(f"Participant: {participant['fullName']}\n")
                f.write(f"Phone: {participant['phone']}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 60 + "\n\n")
                
                f.write("🇬🇧 ENGLISH MESSAGE:\n")
                f.write("-" * 30 + "\n")
                f.write(english_msg)
                f.write("\n\n")
                
                f.write("🇰🇷 SORANI KURDISH MESSAGE:\n")
                f.write("-" * 30 + "\n")
                f.write(kurdish_msg)
                f.write("\n\n")
                
                f.write("=" * 60 + "\n")
                f.write(f"QR Code File: {qr_filename}\n")
                f.write(f"Vercel URL: https://korean-week-qr.vercel.app/user/{participant['id']}\n")
                f.write("=" * 60 + "\n")
            
            print(f"✅ Generated message for {participant['fullName']}")
            print(f"   📄 Message: {msg_filename}")
            print(f"   🖼️  QR Code: {qr_filename}")
            successful_generations += 1
            
        except Exception as e:
            print(f"❌ Failed to generate message for {participant['fullName']}: {e}")
            failed_generations += 1
    
    # Summary
    print(f"\n🎉 WhatsApp message generation completed!")
    print(f"✅ Successful generations: {successful_generations}")
    print(f"❌ Failed generations: {failed_generations}")
    print(f"📊 Total participants: {len(valid_participants)}")
    
    # Create summary file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_file = f"whatsapp_summary_{timestamp}.txt"
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(f"Korea Week 2025 WhatsApp Message Generation Summary\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total participants: {len(valid_participants)}\n")
        f.write(f"Successful generations: {successful_generations}\n")
        f.write(f"Failed generations: {failed_generations}\n\n")
        
        f.write("📱 PARTICIPANTS WITH MESSAGES:\n")
        f.write("=" * 50 + "\n")
        for participant in valid_participants:
            f.write(f"Name: {participant['fullName']}\n")
            f.write(f"Phone: {participant['phone']}\n")
            f.write(f"Day: {participant['selectedDay']}\n")
            f.write("-" * 30 + "\n")
    
    print(f"📄 Summary saved to: {summary_file}")
    print(f"\n💡 How to use:")
    print(f"1. Open any message file from 'whatsapp_messages' folder")
    print(f"2. Copy the message text (English or Kurdish)")
    print(f"3. Send via WhatsApp to the participant's phone number")
    print(f"4. Attach the corresponding QR code image")

def create_bulk_whatsapp_list():
    """Create a bulk WhatsApp contact list"""
    print("📋 Creating bulk WhatsApp contact list...")
    
    participants = load_participants()
    if not participants:
        print("❌ No participants loaded. Exiting.")
        return
    
    # Filter participants with valid phone numbers
    valid_participants = [p for p in participants if p['phone'] and len(p['phone']) > 5]
    
    if not valid_participants:
        print("❌ No participants with valid phone numbers found.")
        return
    
    # Create contact list file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    contact_file = f"whatsapp_contacts_{timestamp}.txt"
    
    with open(contact_file, 'w', encoding='utf-8') as f:
        f.write("Korea Week 2025 - WhatsApp Contact List\n")
        f.write("=" * 50 + "\n")
        f.write("Format: Name | Phone Number | Day | Activities\n")
        f.write("=" * 50 + "\n\n")
        
        for participant in valid_participants:
            activities_text = ", ".join(participant['activities']) if participant['activities'] else "Not specified"
            f.write(f"{participant['fullName']} | {participant['phone']} | {participant['selectedDay']} | {activities_text}\n")
    
    print(f"✅ Contact list saved to: {contact_file}")
    print(f"📊 Total contacts: {len(valid_participants)}")

if __name__ == "__main__":
    print("🇰🇷 Korea Week 2025 WhatsApp Message Generator")
    print("=" * 60)
    
    # Ask user what to do
    print("\nWhat would you like to do?")
    print("1. Generate WhatsApp messages and QR codes for all participants")
    print("2. Create bulk WhatsApp contact list")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        generate_all_whatsapp_messages()
    elif choice == "2":
        create_bulk_whatsapp_list()
    elif choice == "3":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice.")
