#!/usr/bin/env python3
"""
Preview Email Template for Korea Week Invitations
Shows how the email will look before sending
"""

import pandas as pd
import os
import webbrowser
from send_invitations import KoreaWeekInvitationSender

def preview_email_template():
    """Preview the email template for the first participant"""
    
    sender = KoreaWeekInvitationSender()
    
    # Load participants
    if not sender.load_participants():
        print("❌ Failed to load participants.")
        return
    
    if not sender.participants_data:
        print("❌ No participants found.")
        return
    
    # Get the first participant
    first_participant_id = list(sender.participants_data.keys())[0]
    first_participant = sender.participants_data[first_participant_id]
    
    print(f"📧 Previewing email for: {first_participant['fullName']}")
    print(f"📧 Email: {first_participant['email']}")
    print(f"📅 Day: {first_participant['selectedDay']}")
    print(f"🎯 Activities: {', '.join(first_participant['activities'])}")
    
    # Generate QR code if it doesn't exist
    qr_filename = f"{sender.qr_codes_dir}/QR_{first_participant['fullName'].replace(' ', '_').replace('/', '_')}.png"
    if not os.path.exists(qr_filename):
        qr_filename = sender.generate_qr_code(first_participant_id, first_participant['fullName'])
    
    # Create email template
    html_content = sender.create_email_template(first_participant)
    
    # Save preview to file
    preview_file = "email_preview.html"
    with open(preview_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n✅ Email preview saved to: {preview_file}")
    print("🌐 Opening preview in browser...")
    
    # Open in browser
    try:
        webbrowser.open(f"file://{os.path.abspath(preview_file)}")
        print("✅ Preview opened in browser!")
    except:
        print("⚠️  Could not open browser automatically.")
        print(f"📁 Please open {preview_file} manually in your browser.")
    
    print(f"\n📧 This is how the email will look for all participants.")
    print(f"🎨 The email includes:")
    print(f"   - Personalized greeting with participant name")
    print(f"   - Event details (day, activities, location)")
    print(f"   - Embedded QR code image")
    print(f"   - Instructions on how to use the QR code")
    print(f"   - Contact information")
    print(f"   - Beautiful Korea-themed design")

if __name__ == "__main__":
    print("🇰🇷 Korea Week Email Preview")
    print("=" * 40)
    preview_email_template()
