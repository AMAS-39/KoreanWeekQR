#!/usr/bin/env python3
"""
Korean & Kurdistan Themed QR Code Generator
Creates beautiful QR codes with Korean and Kurdistan flags
"""

import pandas as pd
import qrcode
import os
from PIL import Image, ImageDraw, ImageFont
import uuid
import socket

def get_local_ip():
    """Get the local IP address of this computer"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "192.168.1.9"

def create_korean_flag():
    """Create Korean flag design"""
    white = (255, 255, 255)
    red = (205, 49, 58)
    blue = (0, 71, 171)
    black = (0, 0, 0)
    
    flag_width, flag_height = 300, 200
    flag = Image.new('RGB', (flag_width, flag_height), white)
    draw = ImageDraw.Draw(flag)
    
    # Central circle (yin-yang symbol)
    center_x, center_y = flag_width // 2, flag_height // 2
    radius = 30
    
    # Red part of yin-yang
    draw.ellipse([center_x - radius, center_y - radius, center_x + radius, center_y + radius], 
                 fill=red, outline=black, width=2)
    
    # Blue part of yin-yang
    draw.ellipse([center_x - radius//2, center_y - radius, center_x + radius//2, center_y], 
                 fill=blue, outline=black, width=2)
    
    # Small circles
    small_radius = 8
    draw.ellipse([center_x - small_radius, center_y - radius//2 - small_radius, 
                  center_x + small_radius, center_y - radius//2 + small_radius], 
                 fill=red, outline=black, width=1)
    draw.ellipse([center_x - small_radius, center_y + radius//2 - small_radius, 
                  center_x + small_radius, center_y + radius//2 + small_radius], 
                 fill=blue, outline=black, width=1)
    
    return flag

def create_kurdistan_flag():
    """Create Kurdistan flag design"""
    red = (255, 0, 0)
    white = (255, 255, 255)
    green = (0, 128, 0)
    yellow = (255, 215, 0)
    
    flag_width, flag_height = 300, 200
    flag = Image.new('RGB', (flag_width, flag_height), white)
    draw = ImageDraw.Draw(flag)
    
    # Draw Kurdistan flag stripes
    stripe_height = flag_height // 3
    
    # Red stripe (top)
    draw.rectangle([0, 0, flag_width, stripe_height], fill=red)
    
    # Green stripe (bottom)
    draw.rectangle([0, flag_height - stripe_height, flag_width, flag_height], fill=green)
    
    # Sun symbol in center
    center_x, center_y = flag_width // 2, flag_height // 2
    sun_radius = 25
    
    # Draw sun
    draw.ellipse([center_x - sun_radius, center_y - sun_radius, 
                  center_x + sun_radius, center_y + sun_radius], 
                 fill=yellow, outline=(255, 165, 0), width=2)
    
    return flag

def create_themed_qr_code(participant_id, participant_name):
    """Create QR code with Korean and Kurdistan themes"""
    local_ip = get_local_ip()
    qr_url = f"http://{local_ip}:5000/user/{participant_id}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_url)
    qr.make(fit=True)
    
    # Create QR code image
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_size = 300
    qr_img = qr_img.resize((qr_size, qr_size))
    
    # Create background
    bg_width, bg_height = 600, 800
    background = Image.new('RGB', (bg_width, bg_height), (255, 255, 255))
    draw = ImageDraw.Draw(background)
    
    # Add Korean flag (top left)
    korean_flag = create_korean_flag()
    korean_flag = korean_flag.resize((150, 100))
    background.paste(korean_flag, (20, 20))
    
    # Add Kurdistan flag (top right)
    kurdistan_flag = create_kurdistan_flag()
    kurdistan_flag = kurdistan_flag.resize((150, 100))
    background.paste(kurdistan_flag, (bg_width - 170, 20))
    
    # Add QR code in center
    qr_x = (bg_width - qr_size) // 2
    qr_y = (bg_height - qr_size) // 2
    background.paste(qr_img, (qr_x, qr_y))
    
    # Add Korean text
    try:
        font_large = ImageFont.truetype("arial.ttf", 24)
        font_small = ImageFont.truetype("arial.ttf", 16)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Add title
    title = "Korea Week 2025"
    title_bbox = draw.textbbox((0, 0), title, font=font_large)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (bg_width - title_width) // 2
    draw.text((title_x, 140), title, fill=(205, 49, 58), font=font_large)
    
    # Add Korean subtitle
    subtitle = "대한민국 주간"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=font_small)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (bg_width - subtitle_width) // 2
    draw.text((subtitle_x, 170), subtitle, fill=(0, 71, 171), font=font_small)
    
    # Add participant name
    name_text = f"Participant: {participant_name}"
    name_bbox = draw.textbbox((0, 0), name_text, font=font_small)
    name_width = name_bbox[2] - name_bbox[0]
    name_x = (bg_width - name_width) // 2
    draw.text((name_x, bg_height - 80), name_text, fill=(0, 0, 0), font=font_small)
    
    # Add scan instruction
    scan_text = "Scan this QR code"
    scan_bbox = draw.textbbox((0, 0), scan_text, font=font_small)
    scan_width = scan_bbox[2] - scan_bbox[0]
    scan_x = (bg_width - scan_width) // 2
    draw.text((scan_x, bg_height - 60), scan_text, fill=(128, 128, 128), font=font_small)
    
    return background

def load_participants():
    """Load participants from Excel file"""
    try:
        df = pd.read_excel('korea_week_split(1).xlsx')
        participants = []
        
        for index, row in df.iterrows():
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
            
            participants.append({
                'id': participant_id,
                'fullName': row.get('fullName', ''),
                'email': row.get('email', ''),
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

def generate_themed_qr_codes():
    """Generate themed QR codes for all participants"""
    print("🔄 Generating Korean & Kurdistan themed QR codes...")
    
    local_ip = get_local_ip()
    print(f"🌐 Using IP address: {local_ip}")
    
    # Load participants
    participants = load_participants()
    if not participants:
        print("❌ No participants loaded. Exiting.")
        return
    
    # Create themed QR codes directory
    if not os.path.exists('themed_qr_codes'):
        os.makedirs('themed_qr_codes')
    
    generated_files = []
    for participant in participants:
        # Create themed QR code
        themed_qr = create_themed_qr_code(participant['id'], participant['fullName'])
        
        # Save themed QR code
        filename = f"themed_qr_codes/KR_KR_{participant['fullName'].replace(' ', '_').replace('/', '_')}.png"
        themed_qr.save(filename)
        generated_files.append(filename)
        print(f"✅ Generated: {filename}")
    
    print(f"\n🎉 Successfully generated {len(generated_files)} themed QR codes!")
    print("📁 Themed QR codes saved in 'themed_qr_codes' folder")
    print(f"🔗 Each QR code links to: http://{local_ip}:5000/user/[participant_id]")
    
    return generated_files

if __name__ == "__main__":
    generate_themed_qr_codes()
