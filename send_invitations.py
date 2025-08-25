#!/usr/bin/env python3
"""
Email Invitation System for Korea Week
Sends personalized invitations with QR codes to all participants
"""

import pandas as pd
import smtplib
import os
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
import qrcode
import uuid
import socket
from datetime import datetime
import time

class KoreaWeekInvitationSender:
    def __init__(self):
        self.participants_data = {}
        self.qr_codes_dir = "qr_codes"
        self.email_templates_dir = "email_templates"
        
        # Email configuration - UPDATE THESE WITH YOUR EMAIL DETAILS
        self.smtp_server = "smtp.gmail.com"  # or your email provider's SMTP
        self.smtp_port = 587
        self.sender_email = "your-email@gmail.com"  # UPDATE THIS
        self.sender_password = "your-app-password"  # UPDATE THIS (use app password for Gmail)
        
        # Create directories if they don't exist
        os.makedirs(self.qr_codes_dir, exist_ok=True)
        os.makedirs(self.email_templates_dir, exist_ok=True)
    
    def get_local_ip(self):
        """Get the local IP address of this computer"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "192.168.1.9"  # Fallback IP
    
    def load_participants(self):
        """Load participants from Excel file"""
        try:
            df = pd.read_excel('korea_week_split(1).xlsx')
            
            for index, row in df.iterrows():
                # Generate unique ID for each participant
                participant_id = str(uuid.uuid4())[:8]
                
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
                
                self.participants_data[participant_id] = {
                    'id': participant_id,
                    'fullName': row.get('fullName', ''),
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
            
            print(f"✅ Loaded {len(self.participants_data)} participants")
            return True
        except Exception as e:
            print(f"❌ Error loading participants: {e}")
            return False
    
    def generate_qr_code(self, participant_id, participant_name):
        """Generate QR code for a participant"""
        local_ip = self.get_local_ip()
        qr_url = f"http://{local_ip}:5000/user/{participant_id}"
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        filename = f"{self.qr_codes_dir}/QR_{participant_name.replace(' ', '_').replace('/', '_')}.png"
        img.save(filename)
        
        return filename
    
    def generate_all_qr_codes(self):
        """Generate QR codes for all participants"""
        print("🔄 Generating QR codes for all participants...")
        
        for participant_id, participant in self.participants_data.items():
            filename = self.generate_qr_code(participant_id, participant['fullName'])
            print(f"✅ Generated: {filename}")
        
        print(f"🎉 Successfully generated {len(self.participants_data)} QR codes!")
    
    def create_email_template(self, participant):
        """Create personalized email template for a participant"""
        
        # Format activities for display
        activities_text = ""
        if participant['activities']:
            if len(participant['activities']) == 1:
                activities_text = f"<strong>{participant['activities'][0]}</strong>"
            else:
                activities_text = f"<strong>{', '.join(participant['activities'][:-1])}</strong> and <strong>{participant['activities'][-1]}</strong>"
        
        # Create the email HTML template
        html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Korea Week 2025 - You're Invited!</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f4f4f4;
        }}
        .email-container {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        .header {{
            background: linear-gradient(135deg, #cd5c5c 0%, #ff6b6b 50%, #ee5a24 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 30px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.2rem;
            font-weight: 700;
        }}
        .header p {{
            margin: 10px 0 0 0;
            font-size: 1.1rem;
            opacity: 0.9;
        }}
        .korean-flag {{
            font-size: 2rem;
            margin-bottom: 10px;
        }}
        .content {{
            padding: 0 20px;
        }}
        .greeting {{
            font-size: 1.3rem;
            color: #cd5c5c;
            margin-bottom: 20px;
            font-weight: 600;
        }}
        .event-details {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 4px solid #cd5c5c;
        }}
        .qr-section {{
            text-align: center;
            margin: 30px 0;
            padding: 20px;
            background: linear-gradient(135deg, rgba(205, 92, 92, 0.05), rgba(255, 107, 107, 0.05));
            border-radius: 10px;
        }}
        .qr-code {{
            max-width: 200px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}
        .instructions {{
            background: #e8f4fd;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 4px solid #007bff;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            color: #666;
        }}
        .highlight {{
            background: linear-gradient(135deg, #cd5c5c, #ff6b6b);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            display: inline-block;
            margin: 5px;
            font-weight: 500;
        }}
        .contact-info {{
            background: #fff3cd;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
            border-left: 4px solid #ffc107;
        }}
        @media (max-width: 600px) {{
            body {{
                padding: 10px;
            }}
            .email-container {{
                padding: 20px;
            }}
            .header h1 {{
                font-size: 1.8rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <div class="korean-flag">🇰🇷</div>
            <h1>Korea Week 2025</h1>
            <p>대한민국 주간 - You're Invited!</p>
        </div>
        
        <div class="content">
            <div class="greeting">
                안녕하세요 {participant['fullName']}! 👋
            </div>
            
            <p>We are thrilled to invite you to <strong>Korea Week 2025</strong> - a celebration of Korean culture, traditions, and innovation!</p>
            
            <div class="event-details">
                <h3>🎯 Your Event Details:</h3>
                <p><strong>Selected Day:</strong> <span class="highlight">{participant['selectedDay'].upper() if participant['selectedDay'] else 'To be confirmed'}</span></p>
                <p><strong>Your Activities:</strong> {activities_text}</p>
                <p><strong>Location:</strong> {participant['city']}</p>
                {f"<p><strong>Special Requirements:</strong> {participant['dietary']}</p>" if participant['dietary'] else ""}
            </div>
            
            <div class="qr-section">
                <h3>📱 Your Digital Pass</h3>
                <p>Below is your unique QR code. Simply show this to our staff at the event entrance!</p>
                <img src="cid:qr_code" alt="Your QR Code" class="qr-code">
                <p><em>This QR code contains your personal information and will be scanned at check-in.</em></p>
            </div>
            
            <div class="instructions">
                <h3>📋 How to Use Your QR Code:</h3>
                <ol>
                    <li><strong>Save this email</strong> or screenshot the QR code</li>
                    <li><strong>Present at entrance</strong> - show the QR code to staff</li>
                    <li><strong>Get scanned</strong> - staff will scan to verify your details</li>
                    <li><strong>Enjoy Korea Week!</strong> 🇰🇷</li>
                </ol>
            </div>
            
            <div class="contact-info">
                <h3>📞 Need Help?</h3>
                <p>If you have any questions or need assistance:</p>
                <p><strong>Phone:</strong> {participant['phone']}</p>
                <p><strong>Emergency Contact:</strong> {participant['emergencyName']} ({participant['emergencyRelation']}) - {participant['emergencyPhone']}</p>
            </div>
            
            <p><strong>Important Notes:</strong></p>
            <ul>
                <li>Please arrive 15 minutes before your scheduled activities</li>
                <li>Bring comfortable clothing for your selected activities</li>
                <li>Don't forget to bring your enthusiasm for Korean culture! 🇰🇷</li>
            </ul>
        </div>
        
        <div class="footer">
            <p><strong>🇰🇷 Korea Week 2025 - Celebrating Korean Culture Together 🇰🇷</strong></p>
            <p>We can't wait to see you there!</p>
            <p><em>This is an automated invitation. Please do not reply to this email.</em></p>
        </div>
    </div>
</body>
</html>
        """
        
        return html_template
    
    def send_email_with_qr(self, participant, qr_filename):
        """Send personalized email with QR code attachment"""
        try:
            # Create message
            msg = MIMEMultipart('related')
            msg['From'] = self.sender_email
            msg['To'] = participant['email']
            msg['Subject'] = f"🇰🇷 Korea Week 2025 - Your Invitation & QR Code, {participant['fullName']}!"
            
            # Create HTML content
            html_content = self.create_email_template(participant)
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Attach QR code image
            with open(qr_filename, 'rb') as f:
                qr_img = MIMEImage(f.read())
                qr_img.add_header('Content-ID', '<qr_code>')
                qr_img.add_header('Content-Disposition', 'inline', filename='qr_code.png')
                msg.attach(qr_img)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            print(f"❌ Error sending email to {participant['email']}: {e}")
            return False
    
    def send_all_invitations(self):
        """Send invitations to all participants"""
        print("📧 Starting to send email invitations...")
        print(f"📊 Total participants to email: {len(self.participants_data)}")
        
        success_count = 0
        failed_count = 0
        
        for participant_id, participant in self.participants_data.items():
            if not participant['email'] or participant['email'].strip() == '':
                print(f"⚠️  Skipping {participant['fullName']} - no email address")
                failed_count += 1
                continue
            
            print(f"📧 Sending invitation to {participant['fullName']} ({participant['email']})...")
            
            # Generate QR code if it doesn't exist
            qr_filename = f"{self.qr_codes_dir}/QR_{participant['fullName'].replace(' ', '_').replace('/', '_')}.png"
            if not os.path.exists(qr_filename):
                qr_filename = self.generate_qr_code(participant_id, participant['fullName'])
            
            # Send email
            if self.send_email_with_qr(participant, qr_filename):
                print(f"✅ Sent successfully to {participant['fullName']}")
                success_count += 1
            else:
                print(f"❌ Failed to send to {participant['fullName']}")
                failed_count += 1
            
            # Small delay to avoid overwhelming the email server
            time.sleep(1)
        
        print(f"\n🎉 Email sending completed!")
        print(f"✅ Successfully sent: {success_count}")
        print(f"❌ Failed: {failed_count}")
        
        return success_count, failed_count
    
    def setup_email_config(self):
        """Interactive setup for email configuration"""
        print("🔧 Email Configuration Setup")
        print("=" * 50)
        
        print("\n📧 Please provide your email configuration:")
        
        # Email provider selection
        print("\nChoose your email provider:")
        print("1. Gmail")
        print("2. Outlook/Hotmail")
        print("3. Yahoo")
        print("4. Custom SMTP")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":  # Gmail
            self.smtp_server = "smtp.gmail.com"
            self.smtp_port = 587
            print("\n📧 Gmail Configuration:")
            print("⚠️  Note: You'll need to use an App Password, not your regular password")
            print("   To create an App Password:")
            print("   1. Go to your Google Account settings")
            print("   2. Enable 2-Step Verification")
            print("   3. Generate an App Password for 'Mail'")
            
        elif choice == "2":  # Outlook
            self.smtp_server = "smtp-mail.outlook.com"
            self.smtp_port = 587
            
        elif choice == "3":  # Yahoo
            self.smtp_server = "smtp.mail.yahoo.com"
            self.smtp_port = 587
            
        else:  # Custom
            self.smtp_server = input("Enter SMTP server: ").strip()
            self.smtp_port = int(input("Enter SMTP port: ").strip())
        
        self.sender_email = input(f"\n📧 Enter your email address: ").strip()
        self.sender_password = input(f"🔑 Enter your password/app password: ").strip()
        
        # Test the configuration
        print(f"\n🧪 Testing email configuration...")
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                print("✅ Email configuration successful!")
                return True
        except Exception as e:
            print(f"❌ Email configuration failed: {e}")
            print("Please check your email and password/app password.")
            return False

def main():
    """Main function to run the invitation system"""
    print("🇰🇷 Korea Week Email Invitation System")
    print("=" * 50)
    
    sender = KoreaWeekInvitationSender()
    
    # Load participants
    if not sender.load_participants():
        print("❌ Failed to load participants. Exiting.")
        return
    
    # Setup email configuration
    if not sender.setup_email_config():
        print("❌ Email configuration failed. Exiting.")
        return
    
    # Generate QR codes if they don't exist
    if not os.path.exists(sender.qr_codes_dir) or not os.listdir(sender.qr_codes_dir):
        sender.generate_all_qr_codes()
    
    # Confirm before sending
    print(f"\n📧 Ready to send invitations to {len(sender.participants_data)} participants")
    confirm = input("Do you want to proceed? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("❌ Cancelled by user.")
        return
    
    # Send invitations
    success, failed = sender.send_all_invitations()
    
    # Summary
    print(f"\n📊 Final Summary:")
    print(f"✅ Successfully sent: {success} invitations")
    print(f"❌ Failed: {failed} invitations")
    print(f"📧 Total participants: {len(sender.participants_data)}")
    
    if success > 0:
        print(f"\n🎉 Korea Week invitations have been sent successfully!")
        print("📱 Participants can now use their QR codes at the event.")

if __name__ == "__main__":
    main()
