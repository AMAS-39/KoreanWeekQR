#!/usr/bin/env python3
"""
Email Template Generator for Korea Week QR Code System
Generates personalized email templates for sending QR codes to participants
"""

import pandas as pd
import os
from datetime import datetime

def generate_email_template(participant_data, qr_code_path):
    """
    Generate a personalized email template for a participant
    
    Args:
        participant_data (dict): Participant information
        qr_code_path (str): Path to the QR code image
    
    Returns:
        str: HTML email template
    """
    
    # Format activities as a list
    activities_text = ", ".join(participant_data.get('activities', []))
    
    # Format the selected day
    day_text = participant_data.get('selectedDay', '').upper()
    
    email_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Korea Week Event - Your QR Code Invitation</title>
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
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #ff6b6b;
        }}
        .header h1 {{
            color: #ff6b6b;
            margin-bottom: 10px;
        }}
        .qr-section {{
            text-align: center;
            margin: 30px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }}
        .qr-code {{
            max-width: 200px;
            margin: 20px auto;
        }}
        .details {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }}
        .detail-row {{
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
            padding: 5px 0;
        }}
        .detail-label {{
            font-weight: bold;
            color: #666;
        }}
        .detail-value {{
            color: #333;
        }}
        .instructions {{
            background: #e3f2fd;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 4px solid #2196f3;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            color: #666;
            font-size: 0.9em;
        }}
        .btn {{
            display: inline-block;
            background: #ff6b6b;
            color: white;
            padding: 12px 25px;
            text-decoration: none;
            border-radius: 25px;
            margin: 10px 5px;
            font-weight: bold;
        }}
        .btn:hover {{
            background: #ee5a24;
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <h1>🇰🇷 Korea Week in Erbil 2025</h1>
            <p>Your Digital Invitation & QR Code</p>
        </div>
        
        <p>Dear <strong>{participant_data.get('fullName', 'Participant')}</strong>,</p>
        
        <p>Thank you for registering for Korea Week in Erbil 2025! We're excited to have you join us for this amazing cultural celebration.</p>
        
        <div class="qr-section">
            <h3>📱 Your Personal QR Code</h3>
            <p>Please find your unique QR code attached to this email. This QR code contains your digital invitation and will be used for check-in at the event.</p>
            
            <div class="qr-code">
                <img src="{qr_code_path}" alt="Your QR Code" style="max-width: 200px; border: 2px solid #ddd; border-radius: 10px; padding: 10px;">
            </div>
            
            <p><strong>Important:</strong> Please save this QR code on your phone or print it out to bring to the event.</p>
        </div>
        
        <div class="details">
            <h3>📋 Your Event Details</h3>
            <div class="detail-row">
                <span class="detail-label">Name:</span>
                <span class="detail-value">{participant_data.get('fullName', 'N/A')}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Email:</span>
                <span class="detail-value">{participant_data.get('email', 'N/A')}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Phone:</span>
                <span class="detail-value">{participant_data.get('phone', 'N/A')}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">City:</span>
                <span class="detail-value">{participant_data.get('city', 'N/A')}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Selected Day:</span>
                <span class="detail-value">{day_text}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Activities:</span>
                <span class="detail-value">{activities_text}</span>
            </div>
        </div>
        
        <div class="instructions">
            <h3>🎯 How to Use Your QR Code</h3>
            <ol>
                <li><strong>Save the QR Code:</strong> Download and save the QR code image to your phone</li>
                <li><strong>Bring to Event:</strong> Show the QR code to event staff at the entrance</li>
                <li><strong>Scan & Check-in:</strong> Staff will scan your QR code to check you in</li>
                <li><strong>Enjoy the Event:</strong> Your digital pass will display all your details</li>
            </ol>
        </div>
        
        <div class="instructions">
            <h3>📅 Event Information</h3>
            <p><strong>Date:</strong> [Insert Event Date]</p>
            <p><strong>Venue:</strong> [Insert Event Venue]</p>
            <p><strong>Time:</strong> [Insert Event Time]</p>
            <p><strong>Dress Code:</strong> [Insert Dress Code]</p>
        </div>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="#" class="btn">📅 Add to Calendar</a>
            <a href="#" class="btn">📍 Get Directions</a>
        </div>
        
        <div class="footer">
            <p><strong>Korea Week in Erbil 2025</strong></p>
            <p>For any questions, please contact us at: [Insert Contact Email]</p>
            <p>Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>
    </div>
</body>
</html>
"""
    
    return email_template

def generate_all_email_templates():
    """
    Generate email templates for all participants
    """
    try:
        # Load participant data
        df = pd.read_excel('korea_week_split(1).xlsx')
        
        # Create output directory
        output_dir = 'email_templates'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Create QR codes directory reference
        qr_codes_dir = 'qr_codes'
        
        print(f"Generating email templates for {len(df)} participants...")
        
        for index, row in df.iterrows():
            # Create participant data dictionary
            participant_data = {
                'fullName': row.get('fullName', ''),
                'email': row.get('email', ''),
                'phone': str(row.get('phone', '')),
                'city': row.get('city', ''),
                'selectedDay': row.get('selectedDay', ''),
                'activities': row.get('activities', ''),
                'dietary': row.get('dietary', ''),
                'emergencyName': row.get('emergencyName', ''),
                'emergencyPhone': str(row.get('emergencyPhone', '')),
                'emergencyRelation': row.get('emergencyRelation', '')
            }
            
            # Clean activities data
            activities = participant_data['activities']
            if isinstance(activities, str) and activities.startswith('["') and activities.endswith('"]'):
                activities = activities.replace('"', '').replace('[', '').replace(']', '').split(',')
                participant_data['activities'] = activities
            else:
                participant_data['activities'] = [activities] if activities else []
            
            # Generate QR code filename (assuming QR codes are saved with participant names)
            participant_name = participant_data['fullName'].replace(' ', '_').replace('/', '_')
            qr_code_filename = f"QR_{participant_name}.png"
            qr_code_path = f"{qr_codes_dir}/{qr_code_filename}"
            
            # Generate email template
            email_template = generate_email_template(participant_data, qr_code_path)
            
            # Save email template
            email_filename = f"email_{participant_name}.html"
            email_filepath = os.path.join(output_dir, email_filename)
            
            with open(email_filepath, 'w', encoding='utf-8') as f:
                f.write(email_template)
            
            print(f"Generated: {email_filename}")
        
        print(f"\n✅ Successfully generated {len(df)} email templates in '{output_dir}' directory")
        print("\n📧 Next Steps:")
        print("1. Download QR codes from the web interface")
        print("2. Place QR codes in the 'qr_codes' directory")
        print("3. Customize email templates with event details")
        print("4. Send personalized emails to participants")
        
    except Exception as e:
        print(f"❌ Error generating email templates: {e}")

if __name__ == "__main__":
    generate_all_email_templates()
