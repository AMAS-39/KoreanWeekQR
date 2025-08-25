# 🇰�� Korea Week QR Code System

A beautiful, responsive QR code invitation and check-in system for Korea Week events. Each participant receives a unique QR code that displays their digital pass when scanned.

## ✨ Features

- **🎨 Beautiful Korea-Themed Design**: Modern, responsive design with Korean cultural elements
- **📱 Mobile-First**: Perfectly optimized for mobile devices
- **🔗 Dynamic QR Codes**: Each participant gets a unique QR code
- **💾 Data Persistence**: Check-in data is saved permanently
- **📊 Real-time Dashboard**: Live statistics and participant management
- **📄 Export Functionality**: Export check-in data to CSV
- **🎯 Activity Tracking**: Shows all participant activities correctly

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AMAS-39/KoreanWeekQR.git
   cd KoreanWeekQR
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare your data**
   - Place your Excel file (e.g., `korea_week_split(1).xlsx`) in the project directory
   - Ensure it has columns: `fullName`, `email`, `phone`, `city`, `selectedDay`, `activities`, `dietary`

4. **Run the system**
   ```bash
   python generate_qr_codes.py
   ```

5. **Access the system**
   - Dashboard: `http://your-ip:5000`
   - QR codes are saved in the `qr_codes/` folder

## 📱 How It Works

### For Organizers:
1. **Setup**: Run the script with your Excel data
2. **Generate QR Codes**: System creates unique QR codes for each participant
3. **Distribute**: Send QR codes to participants via email/WhatsApp
4. **Monitor**: Use the dashboard to track check-ins in real-time

### For Staff:
1. **Scan QR Code**: Use any phone camera to scan participant QR codes
2. **View Details**: Beautiful digital pass shows all participant information
3. **Check-in**: Mark participants as attended (optional)

### For Participants:
1. **Receive QR Code**: Get your unique QR code via email/WhatsApp
2. **Present at Event**: Show your QR code to staff
3. **Digital Pass**: Staff can view your details instantly

## 🎨 Design Features

- **Korean Theme**: Red and blue gradient inspired by Korean flag
- **Responsive Design**: Works perfectly on all devices
- **Animations**: Subtle Korean wave animations
- **Modern UI**: Glass morphism effects and smooth transitions
- **Cultural Elements**: Korean symbols and traditional patterns

## 📊 System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Excel Data    │───▶│  Flask Backend  │───▶│  QR Code Gen    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  Web Interface  │
                       │  (Mobile/Web)   │
                       └─────────────────┘
```

## 🔧 Configuration

### IP Address
The system automatically detects your local IP address. If needed, you can modify the `get_local_ip()` function in `generate_qr_codes.py`.

### Port
Default port is 5000. Change in the `app.run()` call if needed.

### Data Format
The system expects an Excel file with these columns:
- `fullName`: Participant's full name
- `email`: Email address
- `phone`: Phone number
- `city`: City/location
- `selectedDay`: Chosen event day
- `activities`: Activities (JSON format or single activity)
- `dietary`: Dietary requirements (optional)

## 📁 Project Structure

```
KoreanWeekQR/
├── generate_qr_codes.py      # Main application
├── simple_qr_generator.py    # QR code generator only
├── examine_activities.py     # Data analysis tool
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── .gitignore              # Git ignore rules
├── qr_codes/               # Generated QR codes
├── korea_week_split(1).xlsx # Participant data (not in repo)
└── checkin_data.json       # Check-in records (auto-generated)
```

## 🛠️ API Endpoints

- `GET /`: Dashboard with statistics
- `GET /user/<id>`: Display participant digital pass
- `POST /check-in/<id>`: Mark participant as checked in
- `GET /checkin-data`: View all check-in records
- `GET /export-csv`: Download check-in data as CSV

## 🎯 Features in Detail

### QR Code Generation
- Unique 8-character IDs for each participant
- Links to dynamic web pages
- High-quality PNG images
- Automatic IP detection for network access

### Digital Pass Display
- Beautiful Korea-themed design
- Responsive layout for all devices
- Shows all participant information
- Activity badges with hover effects
- Special dietary requirements section

### Data Management
- Persistent check-in storage
- Real-time statistics
- Export functionality
- Backup and restore capabilities

## 🔒 Security Notes

- This is a development system
- For production use, consider:
  - HTTPS encryption
  - User authentication
  - Database backend
  - Rate limiting
  - Input validation

## 🚀 Deployment Options

### Local Development
```bash
python generate_qr_codes.py
```

### Production Deployment
1. Use a production WSGI server (Gunicorn, uWSGI)
2. Set up reverse proxy (Nginx)
3. Configure SSL certificates
4. Use a proper database (PostgreSQL, MySQL)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

If you encounter any issues:
1. Check the terminal output for error messages
2. Ensure all dependencies are installed
3. Verify your Excel file format
4. Check your network connectivity

## 🎉 Acknowledgments

- Built with Flask and Python
- QR code generation with qrcode library
- Beautiful design with modern CSS
- Korean cultural elements and theming

---

**🇰🇷 Welcome to Korea Week! 🇰🇷**

*Experience the beauty of Korean culture through technology*
