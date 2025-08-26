#!/usr/bin/env python3
"""
Send emails to all participants automatically
"""

from email_sender import load_participants, generate_qr_code, send_email
import time
from datetime import datetime

def send_all_emails():
    """Send emails to all participants"""
    print("🚀 Starting email sending process...")
    print("📧 Sender: ahmadshwanaswad@gmail.com")
    
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
        f.write(f"Sender: ahmadshwanaswad@gmail.com\n")
        f.write(f"Total participants: {len(valid_participants)}\n")
        f.write(f"Successful sends: {successful_sends}\n")
        f.write(f"Failed sends: {failed_sends}\n\n")
        
        for participant in valid_participants:
            f.write(f"Name: {participant['fullName']}\n")
            f.write(f"Email: {participant['email']}\n")
            f.write(f"Day: {participant['selectedDay']}\n")
            f.write("-" * 50 + "\n")
    
    print(f"📄 Email log saved to: {log_file}")

if __name__ == "__main__":
    print("🇰🇷 Korea Week 2025 - Sending Emails to All Participants")
    print("=" * 60)
    send_all_emails()
