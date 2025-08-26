#!/usr/bin/env python3
"""
Send invitation emails to remaining participants who haven't received emails yet
"""

import pandas as pd
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import qrcode
import hashlib
import os
from datetime import datetime
import json

# Email configuration
SENDER_EMAIL = "ahmadshwanaswad@gmail.com"
SENDER_PASSWORD = "btmo qjdf fuzj plyz"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def generate_qr_code(participant_id, participant_name):
    """Generate QR code for a participant"""
    qr_url = f"https://korean-week-qr.vercel.app/user/{participant_id}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save to temporary file
    temp_filename = f"temp_qr_{participant_id}.png"
    img.save(temp_filename)
    return temp_filename

def create_email_content(participant_name, participant_id, selected_day, activities):
    """Create email content in English and Sorani Kurdish"""
    
    # Format activities
    if activities:
        if isinstance(activities, list):
            activities_text = ", ".join(activities)
        else:
            activities_text = str(activities)
    else:
        activities_text = "Various activities"
    
    # English content
    english_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9;">
        <div style="background: linear-gradient(135deg, #cd5c5c, #ff6b6b); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
            <h1 style="margin: 0; font-size: 28px;">🇰🇷 Korea Week 2025 Invitation 🇰🇷</h1>
            <p style="margin: 10px 0 0 0; font-size: 16px;">대한민국 주간 초대장</p>
        </div>
        
        <div style="background: white; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <p style="font-size: 18px; color: #333; margin-bottom: 20px;">Dear <strong>{participant_name}</strong>,</p>
            
            <p style="font-size: 16px; color: #555; line-height: 1.6; margin-bottom: 20px;">
                You are cordially invited to participate in <strong>Korea Week 2025</strong>, a celebration of Korean culture, technology, and innovation!
            </p>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3 style="color: #cd5c5c; margin-top: 0;">📅 Event Details:</h3>
                <p><strong>Selected Day:</strong> {selected_day.upper()}</p>
                <p><strong>Activities:</strong> {activities_text}</p>
                <p><strong>Event Start Time:</strong> 2:00 PM</p>
            </div>
            
            <p style="font-size: 16px; color: #555; line-height: 1.6; margin-bottom: 20px;">
                Please find your personalized QR code attached to this email. This QR code contains your digital pass with all your registration details.
            </p>
            
            <div style="text-align: center; margin: 30px 0;">
                <p style="font-size: 14px; color: #666;">Scan this QR code at the event entrance</p>
            </div>
            
            <div style="background: #e8f4fd; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3 style="color: #2c5aa0; margin-top: 0;">📧 Contact Information:</h3>
                <p style="margin: 5px 0;"><strong>From:</strong> Ahmad Shwan - Main Representative & Head of the Technology and Innovation department in Korea Kurdistan young Organization (KKYO)</p>
            </div>
            
            <p style="font-size: 16px; color: #555; line-height: 1.6; margin-bottom: 20px;">
                We look forward to seeing you at Korea Week 2025!
            </p>
            
            <p style="font-size: 16px; color: #555; line-height: 1.6;">
                Best regards,<br>
                <strong>Ahmad Shwan</strong><br>
                Main Representative & Head of Technology and Innovation<br>
                Korea Kurdistan young Organization (KKYO)
            </p>
        </div>
    </div>
    """
    
    # Sorani Kurdish content
    kurdish_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9;">
        <div style="background: linear-gradient(135deg, #cd5c5c, #ff6b6b); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
            <h1 style="margin: 0; font-size: 28px;">🇰🇷 هەفتەی کۆریا ٢٠٢٥ داواکاری 🇰🇷</h1>
            <p style="margin: 10px 0 0 0; font-size: 16px;">대한민국 주간 초대장</p>
        </div>
        
        <div style="background: white; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <p style="font-size: 18px; color: #333; margin-bottom: 20px;">ڕێزدار <strong>{participant_name}</strong>،</p>
            
            <p style="font-size: 16px; color: #555; line-height: 1.6; margin-bottom: 20px;">
                بە شێوەیەکی ڕێپێدراو داوات لێدەکرێت بەشداری لە <strong>هەفتەی کۆریا ٢٠٢٥</strong> بکەیت، کە بەڕێوەبردنی کلتوری کۆریا، تەکنەلۆژیا و نوێکارییە!
            </p>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3 style="color: #cd5c5c; margin-top: 0;">📅 وردەکاری ڕووداو:</h3>
                <p><strong>ڕۆژی هەڵبژێردراو:</strong> {selected_day.upper()}</p>
                <p><strong>چالاکییەکان:</strong> {activities_text}</p>
                <p><strong>کاتی دەستپێکی ڕووداو:</strong> ٢:٠٠ پ.م</p>
            </div>
            
            <p style="font-size: 16px; color: #555; line-height: 1.6; margin-bottom: 20px;">
                تکایە کۆدی QR تایبەت بە خۆت بدۆزەرەوە کە پەیوەنددراوە بەم ئیمەیڵە. ئەم کۆدی QR یەکە پاسپۆرتی دیجیتاڵی تۆی تێدایە لەگەڵ هەموو وردەکاری تۆمارکردنەکانت.
            </p>
            
            <div style="text-align: center; margin: 30px 0;">
                <p style="font-size: 14px; color: #666;">ئەم کۆدی QR لە دەرگەی ڕووداوەکەدا سکان بکە</p>
            </div>
            
            <div style="background: #e8f4fd; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3 style="color: #2c5aa0; margin-top: 0;">📧 زانیاری پەیوەندی:</h3>
                <p style="margin: 5px 0;"><strong>لەلایەن:</strong> ئەحمەد شوان - نوێنەری سەرەکی و سەرۆکی بەشی تەکنەلۆژیا و نوێکاری لە ڕێکخراوی گەنجانی کوردستانی کۆریا (KKYO)</p>
            </div>
            
            <p style="font-size: 16px; color: #555; line-height: 1.6; margin-bottom: 20px;">
                چاوەڕوانین لە هەفتەی کۆریا ٢٠٢٥دا ببینین!
            </p>
            
            <p style="font-size: 16px; color: #555; line-height: 1.6;">
                پێشکەش،<br>
                <strong>ئەحمەد شوان</strong><br>
                نوێنەری سەرەکی و سەرۆکی تەکنەلۆژیا و نوێکاری<br>
                ڕێکخراوی گەنجانی کوردستانی کۆریا (KKYO)
            </p>
        </div>
    </div>
    """
    
    # Combine both languages
    combined_content = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Korea Week 2025 Invitation</title>
    </head>
    <body>
        {english_content}
        <hr style="margin: 40px 0; border: none; border-top: 2px solid #eee;">
        {kurdish_content}
    </body>
    </html>
    """
    
    return combined_content

def send_email(recipient_email, recipient_name, participant_id, selected_day, activities):
    """Send invitation email with QR code"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email
        msg['Subject'] = f"🇰🇷 Korea Week 2025 Invitation - {recipient_name} 🇰🇷"
        
        # Create email content
        email_content = create_email_content(recipient_name, participant_id, selected_day, activities)
        msg.attach(MIMEText(email_content, 'html'))
        
        # Generate and attach QR code
        qr_filename = generate_qr_code(participant_id, recipient_name)
        with open(qr_filename, 'rb') as f:
            qr_image = MIMEImage(f.read())
            qr_image.add_header('Content-ID', '<qr_code>')
            qr_image.add_header('Content-Disposition', 'attachment', filename=f'QR_Code_{recipient_name}.png')
            msg.attach(qr_image)
        
        # Send email
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        
        # Clean up temporary QR file
        if os.path.exists(qr_filename):
            os.remove(qr_filename)
        
        return True, "Email sent successfully"
        
    except Exception as e:
        # Clean up temporary QR file if it exists
        qr_filename = f"temp_qr_{participant_id}.png"
        if os.path.exists(qr_filename):
            os.remove(qr_filename)
        return False, str(e)

def main():
    print("📧 Starting to send remaining invitation emails...")
    
    try:
        # Load all participants from Excel
        df = pd.read_excel('korea_week_split(1).xlsx')
        print(f"📊 Loaded {len(df)} participants from Excel file")
        
        # Load previously sent emails log if exists
        sent_emails = set()
        if os.path.exists('email_log_20250826_005601.txt'):
            with open('email_log_20250826_005601.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    if 'Email sent to:' in line:
                        email = line.split('Email sent to:')[1].strip()
                        sent_emails.add(email)
            print(f"📋 Found {len(sent_emails)} previously sent emails")
        
        # Process participants
        successful_sends = 0
        failed_sends = 0
        skipped_sends = 0
        
        # Create new log file for this session
        log_filename = f"email_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(log_filename, 'w', encoding='utf-8') as log_file:
            log_file.write(f"Email sending session started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            log_file.write("=" * 60 + "\n\n")
            
            for index, row in df.iterrows():
                try:
                    name = str(row.get('fullName', '')).strip()
                    email = str(row.get('email', '')).strip()
                    selected_day = str(row.get('selectedDay', '')).strip()
                    
                    # Skip if no name or invalid email
                    if not name or name == 'nan':
                        continue
                    
                    if not email or email == 'nan' or '@' not in email:
                        print(f"⏭️ Skipping {name}: No valid email")
                        skipped_sends += 1
                        continue
                    
                    # Check if email was already sent
                    if email in sent_emails:
                        print(f"⏭️ Skipping {name}: Email already sent")
                        skipped_sends += 1
                        continue
                    
                    # Generate participant ID
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
                    
                    print(f"📧 Sending email to: {name} ({email})")
                    
                    # Send email
                    success, message = send_email(email, name, participant_id, selected_day, activities)
                    
                    if success:
                        print(f"✅ Email sent successfully to {name}")
                        successful_sends += 1
                        sent_emails.add(email)
                        log_file.write(f"✅ Email sent to: {email} - {name} - {message}\n")
                    else:
                        print(f"❌ Failed to send email to {name}: {message}")
                        failed_sends += 1
                        log_file.write(f"❌ Failed to send to: {email} - {name} - {message}\n")
                    
                    # Add delay to avoid rate limiting
                    import time
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"❌ Error processing row {index}: {e}")
                    failed_sends += 1
                    log_file.write(f"❌ Error processing row {index}: {e}\n")
                    continue
            
            # Write summary
            log_file.write(f"\n" + "=" * 60 + "\n")
            log_file.write(f"Session Summary:\n")
            log_file.write(f"Successful sends: {successful_sends}\n")
            log_file.write(f"Failed sends: {failed_sends}\n")
            log_file.write(f"Skipped sends: {skipped_sends}\n")
            log_file.write(f"Total processed: {successful_sends + failed_sends + skipped_sends}\n")
        
        print(f"\n🎉 Email sending completed!")
        print(f"✅ Successful sends: {successful_sends}")
        print(f"❌ Failed sends: {failed_sends}")
        print(f"⏭️ Skipped sends: {skipped_sends}")
        print(f"📄 Log saved to: {log_filename}")
        
    except Exception as e:
        print(f"❌ Error loading Excel file: {e}")

if __name__ == "__main__":
    main()
