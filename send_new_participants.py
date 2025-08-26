#!/usr/bin/env python3
"""
Send emails only to NEW participants who haven't received emails yet
"""

from email_sender import load_participants, generate_qr_code, send_email
import time
from datetime import datetime
import os

def get_sent_emails():
    """Get list of emails that have already been sent"""
    sent_emails = set()
    
    # Check for email log files
    for filename in os.listdir('.'):
        if filename.startswith('email_log_') and filename.endswith('.txt'):
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('Email: '):
                        email = line.replace('Email: ', '').strip()
                        sent_emails.add(email)
    
    return sent_emails

def send_new_emails():
    """Send emails only to new participants"""
    print("🚀 Starting email sending for NEW participants only...")
    print("📧 Sender: ahmadshwanaswad@gmail.com")
    
    # Get already sent emails
    sent_emails = get_sent_emails()
    print(f"📊 Found {len(sent_emails)} emails already sent")
    
    # Load participants
    participants = load_participants()
    if not participants:
        print("❌ No participants loaded. Exiting.")
        return
    
    # Filter for new participants only
    new_participants = []
    for p in participants:
        if p['email'] and '@' in p['email'] and p['email'] not in sent_emails:
            new_participants.append(p)
    
    print(f"📊 Found {len(new_participants)} NEW participants with valid emails")
    
    if not new_participants:
        print("✅ No new participants found. All emails already sent!")
        return
    
    # Show new participants
    print("\n📋 New participants to receive emails:")
    for i, p in enumerate(new_participants, 1):
        print(f"{i}. {p['fullName']} ({p['email']}) - {p['selectedDay']}")
    
    # Ask for confirmation
    print(f"\n⚠️  This will send emails to {len(new_participants)} NEW participants")
    confirm = input("Continue? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Operation cancelled.")
        return
    
    # Send emails
    successful_sends = 0
    failed_sends = 0
    
    for i, participant in enumerate(new_participants, 1):
        print(f"\n📧 Sending email {i}/{len(new_participants)} to {participant['email']}...")
        
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
    print(f"📊 Total new participants: {len(new_participants)}")
    
    # Save email log
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"email_log_new_{timestamp}.txt"
    
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(f"Korea Week 2025 - NEW Participants Email Sending Log\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Sender: ahmadshwanaswad@gmail.com\n")
        f.write(f"Total new participants: {len(new_participants)}\n")
        f.write(f"Successful sends: {successful_sends}\n")
        f.write(f"Failed sends: {failed_sends}\n\n")
        
        for participant in new_participants:
            f.write(f"Name: {participant['fullName']}\n")
            f.write(f"Email: {participant['email']}\n")
            f.write(f"Day: {participant['selectedDay']}\n")
            f.write("-" * 50 + "\n")
    
    print(f"📄 Email log saved to: {log_file}")

if __name__ == "__main__":
    print("🇰🇷 Korea Week 2025 - Send Emails to NEW Participants Only")
    print("=" * 65)
    send_new_emails()
