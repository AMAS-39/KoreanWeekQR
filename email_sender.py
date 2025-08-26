#!/usr/bin/env python3
"""
Email Sender for Korea Week QR Code Invitations
Sends personalized emails with QR codes to all participants in English and Sorani Kurdish
"""

import pandas as pd
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
import os
import hashlib
import qrcode
from datetime import datetime
import time

# Email Configuration
SENDER_EMAIL = "ahmadshwanaswad@gmail.com"
SENDER_PASSWORD = "btmo qjdf fuzj plyz"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def load_participants():
    """Load participants from Excel file with consistent IDs"""
    try:
        df = pd.read_excel('korea_week_split(1).xlsx')
        participants = []
        
        for index, row in df.iterrows():
            # Generate consistent ID based on email and name
            email = str(row.get('email', '')).strip()
            name = str(row.get('fullName', '')).strip()
            
            # Skip empty rows
            if not name or name == 'nan':
                continue
            
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
    """Generate QR code for a participant and return the image data"""
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
    
    # Convert to bytes
    import io
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    return img_byte_arr

def create_email_content(participant):
    """Create email content in English and Sorani Kurdish"""
    
    # Format activities for display
    activities_text = ", ".join(participant['activities']) if participant['activities'] else "Not specified"
    
    # English Content
    english_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9;">
        <div style="background: linear-gradient(135deg, #cd5c5c 0%, #ff6b6b 50%, #ee5a24 100%); color: white; padding: 30px; text-align: center; border-radius: 15px 15px 0 0;">
            <h1 style="margin: 0; font-size: 2.5rem;">🇰🇷 Korea Week 2025</h1>
            <p style="margin: 10px 0 0 0; font-size: 1.2rem; opacity: 0.9;">Digital Invitation & QR Code</p>
        </div>
        
        <div style="background: white; padding: 30px; border-radius: 0 0 15px 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
            <h2 style="color: #cd5c5c; margin-bottom: 20px;">Dear {participant['fullName']},</h2>
            
                         <p style="font-size: 16px; line-height: 1.6; color: #333;">
                 You are cordially invited to participate in <strong>Korea Week 2025</strong>! 
                 This exciting event celebrates Korean culture, traditions, and modern innovations.
                 <br><br>
                 <strong>Event Start Time: 2:00 PM</strong>
             </p>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #cd5c5c;">
                <h3 style="color: #cd5c5c; margin-top: 0;">Your Event Details:</h3>
                <p><strong>Name:</strong> {participant['fullName']}</p>
                <p><strong>Email:</strong> {participant['email']}</p>
                <p><strong>Phone:</strong> {participant['phone']}</p>
                <p><strong>City:</strong> {participant['city']}</p>
                <p><strong>Selected Day:</strong> {participant['selectedDay']}</p>
                <p><strong>Activities:</strong> {activities_text}</p>
                {f'<p><strong>Dietary Requirements:</strong> {participant["dietary"]}</p>' if participant['dietary'] else ''}
            </div>
            
            <div style="text-align: center; margin: 30px 0;">
                <h3 style="color: #cd5c5c;">Your Personal QR Code</h3>
                <p style="color: #666; margin-bottom: 20px;">
                    Scan this QR code at the event entrance to access your digital pass and check-in.
                </p>
                <img src="cid:qr_code" alt="QR Code" style="max-width: 200px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.2);">
            </div>
            
            <div style="background: #e8f5e8; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #28a745;">
                <h3 style="color: #28a745; margin-top: 0;">📱 How to Use Your QR Code:</h3>
                <ol style="color: #333;">
                    <li>Save this email or print the QR code</li>
                    <li>Present it at the event entrance</li>
                    <li>Staff will scan it to check you in</li>
                    <li>Your digital pass will display all your details</li>
                </ol>
            </div>
            
            <p style="font-size: 16px; line-height: 1.6; color: #333;">
                We look forward to seeing you at Korea Week 2025! 
                Get ready for an amazing experience filled with Korean culture, food, music, and activities.
            </p>
            
                         <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                 <p style="color: #666; margin: 0;">
                     <strong>Ahmad Shwan</strong><br>
                     <em>Main Representative & Head of Technology and Innovation in</em><br>
                                           <strong>Korea Kurdistan Young Organization (KKYO)</strong><br>
                      📧 ahmadshwanaswad@gmail.com
                 </p>
             </div>
        </div>
    </div>
    """
    
    # Sorani Kurdish Content
    kurdish_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9;">
        <div style="background: linear-gradient(135deg, #cd5c5c 0%, #ff6b6b 50%, #ee5a24 100%); color: white; padding: 30px; text-align: center; border-radius: 15px 15px 0 0;">
            <h1 style="margin: 0; font-size: 2.5rem;">🇰🇷 هەفتەی کۆریا ٢٠٢٥</h1>
            <p style="margin: 10px 0 0 0; font-size: 1.2rem; opacity: 0.9;">دەرگا و کۆدی QR دیجیتاڵ</p>
        </div>
        
        <div style="background: white; padding: 30px; border-radius: 0 0 15px 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
            <h2 style="color: #cd5c5c; margin-bottom: 20px;">سڵاو {participant['fullName']}،</h2>
            
                         <p style="font-size: 16px; line-height: 1.6; color: #333;">
                 بە دڵخۆشی دەتەوێت بانگێشت بکەین بۆ بەشداریکردن لە <strong>هەفتەی کۆریا ٢٠٢٥</strong>! 
                 ئەم ڕووداوە سەرنجڕاکێشە کۆڵتوری کۆریا، نەریتەکان و نوێکارییە مۆدێرنەکان جێگەدەکات.
                 <br><br>
                 <strong>کاتی دەستپێکردنی ڕووداو: ٢:٠٠ دوای نیوەڕۆ</strong>
             </p>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #cd5c5c;">
                <h3 style="color: #cd5c5c; margin-top: 0;">وردەکارییەکانی ڕووداوەکەت:</h3>
                <p><strong>ناو:</strong> {participant['fullName']}</p>
                <p><strong>ئیمەیڵ:</strong> {participant['email']}</p>
                <p><strong>ژمارەی مۆبایل:</strong> {participant['phone']}</p>
                <p><strong>شار:</strong> {participant['city']}</p>
                <p><strong>ڕۆژی هەڵبژێردراو:</strong> {participant['selectedDay']}</p>
                <p><strong>چالاکییەکان:</strong> {activities_text}</p>
                {f'<p><strong>پێویستییە خۆراکییەکان:</strong> {participant["dietary"]}</p>' if participant['dietary'] else ''}
            </div>
            
            <div style="text-align: center; margin: 30px 0;">
                <h3 style="color: #cd5c5c;">کۆدی QR تایبەتەکەت</h3>
                <p style="color: #666; margin-bottom: 20px;">
                    ئەم کۆدی QR لە دەرگای ڕووداوەکەدا سکان بکە بۆ دەستگەیشتن بە پاسە دیجیتاڵەکەت و چێککردن.
                </p>
                <img src="cid:qr_code" alt="کۆدی QR" style="max-width: 200px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.2);">
            </div>
            
            <div style="background: #e8f5e8; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #28a745;">
                <h3 style="color: #28a745; margin-top: 0;">📱 چۆن کۆدی QR بەکاربهێنیت:</h3>
                <ol style="color: #333;">
                    <li>ئەم ئیمەیڵە هەڵبگرە یان کۆدی QR چاپ بکە</li>
                    <li>لە دەرگای ڕووداوەکەدا پیشانی بدە</li>
                    <li>ستاف سکان دەکات بۆ چێککردنت</li>
                    <li>پاسە دیجیتاڵەکەت هەموو وردەکارییەکان پیشان دەدات</li>
                </ol>
            </div>
            
            <p style="font-size: 16px; line-height: 1.6; color: #333;">
                چاوەڕوانین ببینین لە هەفتەی کۆریا ٢٠٢٥! 
                ئامادە بە بۆ ئەزموونێکی سەرنجڕاکێش پڕ لە کۆڵتوری کۆریا، خۆراک، مۆسیقا و چالاکییەکان.
            </p>
            
                         <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                 <p style="color: #666; margin: 0;">
                     <strong>ئەحمەد شوان</strong><br>
                     <em>نوێنەری سەرەکی و سەرۆکی تەکنەلۆجیا و نوێکاری</em><br>
                                           <strong>ڕێکخراوی گەنجانی کۆریا کوردستان (KKYO)</strong><br>
                      📧 ahmadshwanaswad@gmail.com
                 </p>
             </div>
        </div>
    </div>
    """
    
    # Combine both languages
    combined_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Korea Week 2025 - هەفتەی کۆریا ٢٠٢٥</title>
    </head>
    <body>
        {english_content}
        <hr style="margin: 40px 0; border: none; border-top: 2px solid #eee;">
        {kurdish_content}
    </body>
    </html>
    """
    
    return combined_content

def send_email(participant, qr_image_data):
    """Send email to a participant"""
    try:
        # Create message
        msg = MIMEMultipart('related')
        msg['From'] = SENDER_EMAIL
        msg['To'] = participant['email']
        msg['Subject'] = f"🇰🇷 Korea Week 2025 - Your Personal QR Code | هەفتەی کۆریا ٢٠٢٥ - کۆدی QR تایبەتەکەت"
        
        # Create the HTML content
        html_content = create_email_content(participant)
        
        # Attach HTML content
        html_part = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(html_part)
        
        # Attach QR code image
        qr_attachment = MIMEImage(qr_image_data)
        qr_attachment.add_header('Content-ID', '<qr_code>')
        qr_attachment.add_header('Content-Disposition', 'inline', filename=f"QR_{participant['fullName'].replace(' ', '_')}.png")
        msg.attach(qr_attachment)
        
        # Create SMTP session
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            
            # Send email
            text = msg.as_string()
            server.sendmail(SENDER_EMAIL, participant['email'], text)
        
        return True
        
    except Exception as e:
        print(f"❌ Error sending email to {participant['email']}: {e}")
        return False

def send_all_emails():
    """Send emails to all participants"""
    print("🚀 Starting email sending process...")
    print(f"📧 Sender: {SENDER_EMAIL}")
    
    # Load participants
    participants = load_participants()
    if not participants:
        print("❌ No participants loaded. Exiting.")
        return
    
    # Filter participants with valid emails
    valid_participants = [p for p in participants if p['email'] and '@' in p['email']]
    print(f"📊 Found {len(valid_participants)} participants with valid emails")
    
    if not valid_participants:
        print("❌ No participants with valid emails found.")
        return
    
    # Send emails
    successful_sends = 0
    failed_sends = 0
    
    for i, participant in enumerate(valid_participants, 1):
        print(f"\n📧 Sending email {i}/{len(valid_participants)} to {participant['email']}...")
        
        # Generate QR code
        qr_image_data = generate_qr_code(participant['id'], participant['fullName'])
        
        # Send email
        if send_email(participant, qr_image_data):
            print(f"✅ Email sent successfully to {participant['fullName']} ({participant['email']})")
            successful_sends += 1
        else:
            print(f"❌ Failed to send email to {participant['fullName']} ({participant['email']})")
            failed_sends += 1
        
        # Add delay to avoid rate limiting
        time.sleep(2)
    
    # Summary
    print(f"\n🎉 Email sending completed!")
    print(f"✅ Successful sends: {successful_sends}")
    print(f"❌ Failed sends: {failed_sends}")
    print(f"📊 Total participants: {len(valid_participants)}")
    
    # Save email log
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"email_log_{timestamp}.txt"
    
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(f"Korea Week 2025 Email Sending Log\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Sender: {SENDER_EMAIL}\n")
        f.write(f"Total participants: {len(valid_participants)}\n")
        f.write(f"Successful sends: {successful_sends}\n")
        f.write(f"Failed sends: {failed_sends}\n\n")
        
        for participant in valid_participants:
            f.write(f"Name: {participant['fullName']}\n")
            f.write(f"Email: {participant['email']}\n")
            f.write(f"Day: {participant['selectedDay']}\n")
            f.write("-" * 50 + "\n")
    
    print(f"📄 Email log saved to: {log_file}")

def test_email_system():
    """Test the email system with a single email"""
    print("🧪 Testing email system...")
    
    # Create a test participant
    test_participant = {
        'id': 'test123',
        'fullName': 'Test User',
        'email': SENDER_EMAIL,  # Send to yourself for testing
        'phone': '+964750000000',
        'city': 'Erbil',
        'selectedDay': 'Day 1',
        'activities': ['Kimbap Making', 'Taekwondo'],
        'dietary': 'Vegetarian'
    }
    
    # Generate QR code
    qr_image_data = generate_qr_code(test_participant['id'], test_participant['fullName'])
    
    # Send test email
    if send_email(test_participant, qr_image_data):
        print("✅ Test email sent successfully!")
        print(f"📧 Check your inbox: {SENDER_EMAIL}")
    else:
        print("❌ Test email failed!")

if __name__ == "__main__":
    print("🇰🇷 Korea Week 2025 Email Sender")
    print("=" * 50)
    
    # Ask user what to do
    print("\nWhat would you like to do?")
    print("1. Send emails to all participants")
    print("2. Test email system (send to yourself)")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        print("\n⚠️  WARNING: This will send emails to ALL participants!")
        confirm = input("Are you sure? Type 'YES' to continue: ").strip()
        if confirm == "YES":
            send_all_emails()
        else:
            print("❌ Operation cancelled.")
    elif choice == "2":
        test_email_system()
    elif choice == "3":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice.")
