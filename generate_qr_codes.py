#!/usr/bin/env python3
"""
Simple QR Code Generator for Korea Week Participants
Creates QR codes for all users and serves their data when scanned
"""

import pandas as pd
import qrcode
import os
from flask import Flask, render_template_string, request
import hashlib
from datetime import datetime
import socket
import json

# Create Flask app
app = Flask(__name__)

# Global variable to store participant data
participants_data = {}

# File to store check-in data
CHECKIN_DATA_FILE = "checkin_data.json"

def get_local_ip():
    """Get the local IP address of this computer"""
    try:
        # Connect to a remote address to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "192.168.1.9"  # Fallback IP

def load_checkin_data():
    """Load existing check-in data from file"""
    if os.path.exists(CHECKIN_DATA_FILE):
        try:
            with open(CHECKIN_DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_checkin_data():
    """Save check-in data to file"""
    checkin_data = {}
    for participant_id, participant in participants_data.items():
        if participant.get('checked_in', False):
            checkin_data[participant_id] = {
                'checked_in': participant['checked_in'],
                'check_in_time': participant['check_in_time'],
                'fullName': participant['fullName']
            }
    
    try:
        with open(CHECKIN_DATA_FILE, 'w') as f:
            json.dump(checkin_data, f, indent=2)
        print(f"💾 Check-in data saved to {CHECKIN_DATA_FILE}")
    except Exception as e:
        print(f"❌ Error saving check-in data: {e}")

def load_participants():
    """Load participants from Excel file"""
    global participants_data
    try:
        df = pd.read_excel('korea_week_split(1).xlsx')
        
        # Load existing check-in data
        existing_checkins = load_checkin_data()
        
        for index, row in df.iterrows():
            # Generate consistent ID based on email and name
            email = row.get('email', '').strip()
            name = row.get('fullName', '').strip()
            
            # Create a consistent hash-based ID
            if email:
                # Use email as primary identifier
                id_string = email.lower()
            else:
                # Fallback to name if no email
                id_string = name.lower()
            
            # Generate consistent 8-character ID
            participant_id = hashlib.md5(id_string.encode()).hexdigest()[:8]
            
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
            
            # Check if this participant was previously checked in
            checked_in = False
            check_in_time = None
            if participant_id in existing_checkins:
                checked_in = existing_checkins[participant_id].get('checked_in', False)
                check_in_time = existing_checkins[participant_id].get('check_in_time')
            
            participants_data[participant_id] = {
                'id': participant_id,
                'fullName': name,
                'age': row.get('age', ''),
                'email': email,
                'phone': str(row.get('phone', '')),
                'city': row.get('city', ''),
                'selectedDay': row.get('selectedDay', ''),
                'activities': activities,
                'dietary': row.get('dietary', ''),
                'emergencyName': row.get('emergencyName', ''),
                'emergencyPhone': str(row.get('emergencyPhone', '')),
                'emergencyRelation': row.get('emergencyRelation', ''),
                'checked_in': checked_in,
                'check_in_time': check_in_time
            }
        
        print(f"✅ Loaded {len(participants_data)} participants")
        if existing_checkins:
            print(f"📊 Restored {len(existing_checkins)} previous check-ins")
        return True
    except Exception as e:
        print(f"❌ Error loading participants: {e}")
        return False

def generate_qr_code(participant_id, participant_name):
    """Generate QR code for a participant"""
    # Use Vercel URL for production
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
    
    # Create QR codes directory if it doesn't exist
    if not os.path.exists('qr_codes'):
        os.makedirs('qr_codes')
    
    # Save QR code image
    filename = f"qr_codes/QR_{participant_name.replace(' ', '_').replace('/', '_')}.png"
    img.save(filename)
    
    return filename

def generate_all_qr_codes():
    """Generate QR codes for all participants"""
    print("🔄 Generating QR codes for all participants...")
    
    print(f"🌐 Using Vercel URL: https://korean-week-qr.vercel.app")
    
    generated_files = []
    for participant_id, participant in participants_data.items():
        filename = generate_qr_code(participant_id, participant['fullName'])
        generated_files.append(filename)
        print(f"✅ Generated: {filename}")
    
    print(f"\n🎉 Successfully generated {len(generated_files)} QR codes!")
    print("📁 QR codes saved in 'qr_codes' folder")
    print(f"🔗 Each QR code links to: https://korean-week-qr.vercel.app/user/[participant_id]")
    
    return generated_files

# HTML template for displaying participant data
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Korea Week - Participant Pass</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 25%, #cd5c5c 50%, #ff6b6b 75%, #ee5a24 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 10px;
            position: relative;
            overflow-x: hidden;
        }
        
        /* Korean flag pattern background */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 20% 20%, rgba(255,255,255,0.1) 2px, transparent 2px),
                radial-gradient(circle at 80% 80%, rgba(255,255,255,0.1) 2px, transparent 2px),
                radial-gradient(circle at 40% 60%, rgba(255,255,255,0.1) 2px, transparent 2px);
            background-size: 50px 50px, 30px 30px, 40px 40px;
            pointer-events: none;
            z-index: 0;
        }
        
        .pass-card {
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(25px);
            border-radius: 28px;
            padding: 0;
            max-width: 450px;
            width: 100%;
            box-shadow: 
                0 30px 60px rgba(0, 0, 0, 0.2),
                0 0 0 1px rgba(255, 255, 255, 0.3);
            border: 2px solid rgba(255, 255, 255, 0.3);
            overflow: hidden;
            position: relative;
            z-index: 1;
        }
        
        .header {
            background: linear-gradient(135deg, #cd5c5c 0%, #ff6b6b 50%, #ee5a24 100%);
            color: white;
            padding: 35px 25px 30px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        /* Korean traditional pattern overlay */
        .header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                linear-gradient(45deg, transparent 40%, rgba(255,255,255,0.1) 50%, transparent 60%),
                radial-gradient(circle at 30% 30%, rgba(255,255,255,0.1) 0%, transparent 50%),
                radial-gradient(circle at 70% 70%, rgba(255,255,255,0.1) 0%, transparent 50%);
            background-size: 100px 100px, 60px 60px, 80px 80px;
            animation: koreanPattern 20s linear infinite;
        }
        
        @keyframes koreanPattern {
            0% { transform: translateX(0) translateY(0); }
            100% { transform: translateX(-100px) translateY(-100px); }
        }
        
        .header h1 {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 8px;
            position: relative;
            z-index: 1;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1rem;
            opacity: 0.95;
            font-weight: 400;
            position: relative;
            z-index: 1;
            text-shadow: 0 1px 2px rgba(0,0,0,0.3);
        }
        
        .korean-symbols {
            position: absolute;
            top: 15px;
            left: 15px;
            font-size: 1.5rem;
            opacity: 0.8;
            z-index: 1;
        }
        
        .content {
            padding: 35px 25px;
        }
        
        .info-section {
            margin-bottom: 30px;
        }
        
        .info-section:last-child {
            margin-bottom: 0;
        }
        
        .section-title {
            font-size: 0.9rem;
            font-weight: 600;
            color: #cd5c5c;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .section-title::before {
            content: '⚡';
            font-size: 1rem;
        }
        
        .section-title::after {
            content: '';
            flex: 1;
            height: 2px;
            background: linear-gradient(90deg, #cd5c5c, transparent);
            border-radius: 1px;
        }
        
        .info-grid {
            display: grid;
            gap: 18px;
        }
        
        .info-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px 20px;
            background: linear-gradient(135deg, rgba(205, 92, 92, 0.05), rgba(255, 107, 107, 0.05));
            border-radius: 16px;
            border: 1px solid rgba(205, 92, 92, 0.15);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .info-item::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            transition: left 0.5s ease;
        }
        
        .info-item:hover::before {
            left: 100%;
        }
        
        .info-item:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(205, 92, 92, 0.2);
        }
        
        .info-label {
            font-size: 0.95rem;
            font-weight: 500;
            color: #4a5568;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .info-label::before {
            content: '🎯';
            font-size: 0.8rem;
        }
        
        .info-value {
            font-size: 0.95rem;
            font-weight: 600;
            color: #2d3748;
            text-align: right;
            max-width: 65%;
            word-break: break-word;
        }
        
        .activities-container {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: flex-end;
        }
        
        .activity-badge {
            background: linear-gradient(135deg, #cd5c5c, #ff6b6b);
            color: white;
            padding: 8px 16px;
            border-radius: 25px;
            font-size: 0.85rem;
            font-weight: 500;
            box-shadow: 0 4px 15px rgba(205, 92, 92, 0.3);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .activity-badge::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            transition: left 0.5s ease;
        }
        
        .activity-badge:hover::before {
            left: 100%;
        }
        
        .activity-badge:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(205, 92, 92, 0.4);
        }
        
        .dietary-info {
            background: linear-gradient(135deg, #ff6b6b, #ee5a24);
            color: white;
            padding: 12px 16px;
            border-radius: 12px;
            font-size: 0.9rem;
            font-weight: 500;
            text-align: center;
            box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
            position: relative;
            overflow: hidden;
        }
        
        .dietary-info::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            transition: left 0.5s ease;
        }
        
        .dietary-info:hover::before {
            left: 100%;
        }
        
        .footer {
            background: linear-gradient(135deg, rgba(205, 92, 92, 0.05), rgba(255, 107, 107, 0.05));
            padding: 25px;
            text-align: center;
            border-top: 1px solid rgba(205, 92, 92, 0.15);
            position: relative;
        }
        
        .footer::before {
            content: '🇰🇷';
            position: absolute;
            top: 10px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 1.5rem;
            opacity: 0.3;
        }
        
        .footer-text {
            font-size: 0.85rem;
            color: #718096;
            font-weight: 400;
            position: relative;
            z-index: 1;
        }
        
        .qr-indicator {
            position: absolute;
            top: 20px;
            right: 20px;
            width: 45px;
            height: 45px;
            background: rgba(255, 255, 255, 0.25);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.3rem;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        
        /* Mobile Responsive Design */
        @media (max-width: 480px) {
            body {
                padding: 5px;
            }
            
            .pass-card {
                margin: 5px;
                border-radius: 24px;
                max-width: 100%;
            }
            
            .header {
                padding: 25px 20px 20px;
            }
            
            .header h1 {
                font-size: 1.8rem;
            }
            
            .header p {
                font-size: 0.9rem;
            }
            
            .content {
                padding: 25px 20px;
            }
            
            .info-item {
                padding: 14px 16px;
                flex-direction: column;
                align-items: flex-start;
                gap: 8px;
            }
            
            .info-value {
                text-align: left;
                max-width: 100%;
                font-size: 0.9rem;
            }
            
            .activities-container {
                justify-content: flex-start;
                width: 100%;
            }
            
            .activity-badge {
                font-size: 0.8rem;
                padding: 6px 12px;
            }
            
            .section-title {
                font-size: 0.85rem;
            }
            
            .korean-symbols {
                font-size: 1.2rem;
                top: 10px;
                left: 10px;
            }
            
            .qr-indicator {
                width: 40px;
                height: 40px;
                font-size: 1.1rem;
                top: 15px;
                right: 15px;
            }
        }
        
        @media (max-width: 360px) {
            .header h1 {
                font-size: 1.6rem;
            }
            
            .content {
                padding: 20px 15px;
            }
            
            .info-item {
                padding: 12px 14px;
            }
            
            .activity-badge {
                font-size: 0.75rem;
                padding: 5px 10px;
            }
        }
        
        /* Korean wave animation */
        @keyframes koreanWave {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-5px); }
        }
        
        .pass-card {
            animation: koreanWave 6s ease-in-out infinite;
        }
    </style>
</head>
<body>
    <div class="pass-card">
        <div class="header">
            <div class="korean-symbols">🎌</div>
            <div class="qr-indicator">📱</div>
            <h1>Korea Week 2025</h1>
            <p>대한민국 주간 디지털 참가자 패스</p>
        </div>
        
        <div class="content">
            <div class="info-section">
                <div class="section-title">Personal Information</div>
                <div class="info-grid">
                    <div class="info-item">
                        <span class="info-label">Full Name</span>
                        <span class="info-value">{{ participant.fullName }}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Email Address</span>
                        <span class="info-value">{{ participant.email }}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Phone Number</span>
                        <span class="info-value">{{ participant.phone }}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">City</span>
                        <span class="info-value">{{ participant.city }}</span>
                    </div>
                </div>
            </div>
            
            <div class="info-section">
                <div class="section-title">Event Details</div>
                <div class="info-grid">
                    <div class="info-item">
                        <span class="info-label">Selected Day</span>
                        <span class="info-value">{{ participant.selectedDay.upper() if participant.selectedDay else 'Not specified' }}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Activities</span>
                        <div class="activities-container">
                            {% for activity in participant.activities %}
                                <span class="activity-badge">{{ activity.strip() }}</span>
                            {% endfor %}
                        </div>
                    </div>
                </div>
            </div>
            
            {% if participant.dietary %}
            <div class="info-section">
                <div class="section-title">Special Requirements</div>
                <div class="dietary-info">
                    🍽️ {{ participant.dietary }}
                </div>
            </div>
            {% endif %}
        </div>
        
        <div class="footer">
            <div class="footer-text">
                🇰🇷 Welcome to Korea Week! 🇰🇷<br>
                Scan this QR code to view participant information
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/user/<participant_id>')
def show_participant(participant_id):
    """Show participant data when QR code is scanned"""
    participant = participants_data.get(participant_id)
    if not participant:
        return "Participant not found", 404
    
    return render_template_string(HTML_TEMPLATE, participant=participant)

@app.route('/check-in/<participant_id>', methods=['POST'])
def check_in(participant_id):
    """Check in a participant"""
    participant = participants_data.get(participant_id)
    if not participant:
        return "Participant not found", 404
    
    if participant.get('checked_in', False):
        return "Already checked in", 200
    
    # Mark as checked in
    participant['checked_in'] = True
    participant['check_in_time'] = datetime.now().isoformat()
    
    # Save updated data
    save_checkin_data()
    
    return "Successfully checked in", 200

@app.route('/')
def index():
    """Show simple dashboard"""
    total = len(participants_data)
    checked_in = sum(1 for p in participants_data.values() if p.get('checked_in', False))
    
    return f"""
    <html>
    <head>
        <title>Korea Week QR System</title>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; text-align: center; }}
            .stats {{ display: flex; justify-content: center; gap: 20px; margin: 20px 0; }}
            .stat {{ background: #f0f0f0; padding: 20px; border-radius: 10px; }}
            .links {{ margin-top: 30px; }}
            .links a {{ 
                display: inline-block; 
                background: #667eea; 
                color: white; 
                padding: 10px 20px; 
                text-decoration: none; 
                border-radius: 10px; 
                margin: 5px; 
            }}
        </style>
    </head>
    <body>
        <h1>🇰🇷 Korea Week QR Code System</h1>
        <div class="stats">
            <div class="stat">
                <h3>Total Participants</h3>
                <p>{total}</p>
            </div>
            <div class="stat">
                <h3>Checked In</h3>
                <p>{checked_in}</p>
            </div>
        </div>
        <p>Scan any QR code to view participant data and check them in!</p>
        
        <div class="links">
            <a href="/checkin-data">📊 View Check-in Data</a>
            <a href="/export-csv">📄 Export to CSV</a>
        </div>
    </body>
    </html>
    """

@app.route('/checkin-data')
def checkin_data():
    """Show detailed check-in data"""
    checked_in_participants = [p for p in participants_data.values() if p.get('checked_in', False)]
    
    html = """
    <html>
    <head>
        <title>Check-in Data - Korea Week</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            .header { text-align: center; margin-bottom: 30px; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
            th { background-color: #667eea; color: white; }
            tr:nth-child(even) { background-color: #f2f2f2; }
            .back-btn { 
                display: inline-block; 
                background: #667eea; 
                color: white; 
                padding: 10px 20px; 
                text-decoration: none; 
                border-radius: 10px; 
                margin-bottom: 20px; 
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📊 Check-in Data</h1>
            <a href="/" class="back-btn">← Back to Dashboard</a>
        </div>
        
        <h2>Checked-in Participants ({len(checked_in_participants)})</h2>
        
        <table>
            <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
                <th>City</th>
                <th>Day</th>
                <th>Check-in Time</th>
            </tr>
    """
    
    for participant in checked_in_participants:
        check_in_time = participant.get('check_in_time', '')
        if check_in_time:
            # Format the time nicely
            try:
                dt = datetime.fromisoformat(check_in_time.replace('Z', '+00:00'))
                formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
            except:
                formatted_time = check_in_time
        else:
            formatted_time = 'Unknown'
        
        html += f"""
            <tr>
                <td>{participant['fullName']}</td>
                <td>{participant['email']}</td>
                <td>{participant['phone']}</td>
                <td>{participant['city']}</td>
                <td>{participant['selectedDay']}</td>
                <td>{formatted_time}</td>
            </tr>
        """
    
    html += """
        </table>
    </body>
    </html>
    """
    
    return html

@app.route('/export-csv')
def export_csv():
    """Export check-in data to CSV"""
    from flask import Response
    
    checked_in_participants = [p for p in participants_data.values() if p.get('checked_in', False)]
    
    csv_data = "Name,Email,Phone,City,Day,Check-in Time\n"
    
    for participant in checked_in_participants:
        check_in_time = participant.get('check_in_time', '')
        if check_in_time:
            try:
                dt = datetime.fromisoformat(check_in_time.replace('Z', '+00:00'))
                formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
            except:
                formatted_time = check_in_time
        else:
            formatted_time = 'Unknown'
        
        csv_data += f'"{participant["fullName"]}","{participant["email"]}","{participant["phone"]}","{participant["city"]}","{participant["selectedDay"]}","{formatted_time}"\n'
    
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=checkin_data.csv"}
    )

def main():
    """Main function to run the system"""
    print("🚀 Starting Korea Week QR Code System...")
    
    # Load participants
    if not load_participants():
        print("❌ Failed to load participants. Exiting.")
        return
    
    # Generate QR codes for Vercel deployment
    generate_all_qr_codes()
    
    print("\n🌐 QR codes generated for Vercel deployment!")
    print("📱 QR codes are ready! Scan any QR code to see participant data.")
    print(f"🔗 Vercel deployment: https://korean-week-qr.vercel.app")
    print(f"📋 Dashboard: https://korean-week-qr.vercel.app")
    print("\n💡 How to use:")
    print("1. Open any QR code image from the 'qr_codes' folder")
    print("2. Scan it with your phone camera")
    print("3. It will open the participant's data page on Vercel")
    print("4. All QR codes work worldwide - no local network needed!")
    
    # Start the web server for local development
    print(f"\n🔧 Local development server also available at: http://localhost:5000")
    app.run(debug=False, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()
