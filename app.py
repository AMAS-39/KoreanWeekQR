from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from flask_cors import CORS
import pandas as pd
import qrcode
import json
import os
import uuid
from datetime import datetime
import io
import base64

app = Flask(__name__)
CORS(app)

# Global variable to store participant data
participants_data = {}
qr_codes_generated = False

def load_participants():
    """Load participants from Excel file"""
    global participants_data
    try:
        df = pd.read_excel('korea_week_split(1).xlsx')
        
        # Clean and process the data
        for index, row in df.iterrows():
            # Generate unique ID for each participant
            participant_id = str(uuid.uuid4())[:8]
            
            # Clean activities data
            activities = row.get('activities', '')
            if isinstance(activities, str) and activities.startswith('["') and activities.endswith('"]'):
                # Parse JSON-like string
                activities = activities.replace('"', '').replace('[', '').replace(']', '').split(',')
            else:
                activities = [activities] if activities else []
            
            participants_data[participant_id] = {
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
                'emergencyRelation': row.get('emergencyRelation', ''),
                'mediaConsent': row.get('mediaConsent', ''),
                'checked_in': False,
                'check_in_time': None
            }
        
        print(f"Loaded {len(participants_data)} participants")
        return True
    except Exception as e:
        print(f"Error loading participants: {e}")
        return False

def generate_qr_code(data, participant_id):
    """Generate QR code for a participant"""
    # Create QR code with the invite URL
    invite_url = f"http://localhost:5000/invite/{participant_id}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(invite_url)
    qr.make(fit=True)
    
    # Create QR code image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64 for embedding in HTML
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return img_str

@app.route('/')
def index():
    """Main dashboard"""
    global participants_data, qr_codes_generated
    
    if not participants_data:
        load_participants()
    
    total_participants = len(participants_data)
    checked_in = sum(1 for p in participants_data.values() if p.get('checked_in', False))
    
    return render_template('dashboard.html', 
                         total_participants=total_participants,
                         checked_in=checked_in,
                         qr_codes_generated=qr_codes_generated)

@app.route('/generate-qr-codes')
def generate_qr_codes():
    """Generate QR codes for all participants"""
    global participants_data, qr_codes_generated
    
    if not participants_data:
        load_participants()
    
    qr_codes = {}
    for participant_id, participant in participants_data.items():
        qr_image = generate_qr_code(participant, participant_id)
        qr_codes[participant_id] = qr_image
    
    qr_codes_generated = True
    
    return render_template('qr_codes.html', 
                         participants=participants_data,
                         qr_codes=qr_codes)

@app.route('/invite/<participant_id>')
def show_invite(participant_id):
    """Show participant's digital pass card"""
    global participants_data
    
    if not participants_data:
        load_participants()
    
    participant = participants_data.get(participant_id)
    if not participant:
        return "Participant not found", 404
    
    return render_template('invite.html', participant=participant)

@app.route('/check-in/<participant_id>', methods=['POST'])
def check_in(participant_id):
    """Check in a participant"""
    global participants_data
    
    participant = participants_data.get(participant_id)
    if not participant:
        return jsonify({'error': 'Participant not found'}), 404
    
    if participant.get('checked_in', False):
        return jsonify({'message': 'Already checked in', 'checked_in': True})
    
    # Mark as checked in
    participant['checked_in'] = True
    participant['check_in_time'] = datetime.now().isoformat()
    
    return jsonify({
        'message': 'Successfully checked in',
        'checked_in': True,
        'check_in_time': participant['check_in_time']
    })

@app.route('/participants')
def list_participants():
    """List all participants"""
    global participants_data
    
    if not participants_data:
        load_participants()
    
    return render_template('participants.html', participants=participants_data.values())

@app.route('/api/participants')
def api_participants():
    """API endpoint to get all participants"""
    global participants_data
    
    if not participants_data:
        load_participants()
    
    return jsonify(list(participants_data.values()))

@app.route('/api/participant/<participant_id>')
def api_participant(participant_id):
    """API endpoint to get a specific participant"""
    global participants_data
    
    if not participants_data:
        load_participants()
    
    participant = participants_data.get(participant_id)
    if not participant:
        return jsonify({'error': 'Participant not found'}), 404
    
    return jsonify(participant)

if __name__ == '__main__':
    # Load participants on startup
    load_participants()
    app.run(debug=True, host='0.0.0.0', port=5000)
