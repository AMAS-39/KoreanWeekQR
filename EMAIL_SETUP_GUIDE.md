# 📧 Korea Week Email Invitation Setup Guide

This guide will help you set up and send personalized email invitations with QR codes to all Korea Week participants.

## 🚀 Quick Start

### Step 1: Preview the Email Template
```bash
python preview_email.py
```
This will show you exactly how the email will look for participants.

### Step 2: Send All Invitations
```bash
python send_invitations.py
```
This will guide you through the email setup and send invitations to all participants.

## 📧 Email Provider Setup

### Gmail Setup (Recommended)
1. **Enable 2-Step Verification**:
   - Go to your Google Account settings
   - Security → 2-Step Verification → Turn it on

2. **Generate App Password**:
   - Go to Google Account settings
   - Security → App passwords
   - Select "Mail" and generate password
   - Use this 16-character password (not your regular password)

3. **Use in Script**:
   - Email: your-gmail@gmail.com
   - Password: Your 16-character app password

### Outlook/Hotmail Setup
- Email: your-email@outlook.com
- Password: Your regular password
- SMTP: smtp-mail.outlook.com
- Port: 587

### Yahoo Setup
- Email: your-email@yahoo.com
- Password: Your regular password
- SMTP: smtp.mail.yahoo.com
- Port: 587

## 📋 What Each Email Contains

### 🎨 Beautiful Design
- Korea-themed header with Korean flag
- Professional, responsive layout
- Works perfectly on mobile devices

### 📝 Personalized Content
- **Greeting**: "안녕하세요 [Name]! 👋"
- **Event Details**: Day, activities, location
- **QR Code**: Embedded image of their unique QR code
- **Instructions**: How to use the QR code at the event
- **Contact Info**: Phone and emergency contact details

### 📱 QR Code Features
- Unique QR code for each participant
- Links to their personal digital pass
- Embedded directly in the email
- High-quality PNG image

## 🔧 Email Configuration Options

The script supports multiple email providers:

1. **Gmail** (Recommended)
   - Most reliable
   - Good delivery rates
   - Requires app password

2. **Outlook/Hotmail**
   - Good for business emails
   - Reliable delivery

3. **Yahoo**
   - Alternative option
   - Good for personal emails

4. **Custom SMTP**
   - For corporate email servers
   - Requires IT department setup

## 📊 Email Sending Process

### Before Sending
1. **Load Participants**: Reads from Excel file
2. **Generate QR Codes**: Creates unique QR codes
3. **Test Configuration**: Verifies email settings
4. **Preview**: Shows email template

### During Sending
1. **Personalize**: Each email is customized
2. **Attach QR Code**: Embeds participant's QR code
3. **Send**: Delivers via SMTP
4. **Track Progress**: Shows success/failure for each

### After Sending
1. **Summary Report**: Shows total sent/failed
2. **Log File**: Detailed results saved
3. **QR Codes Ready**: All participants can use their codes

## 🎯 Email Template Features

### Header Section
- Korean flag emoji 🇰🇷
- "Korea Week 2025" title
- Korean subtitle "대한민국 주간"

### Personal Details
- Participant's full name
- Selected day (DAY 1, DAY 2, etc.)
- Chosen activities (Kimbap, Taekwondo, Makeup)
- Location/city
- Dietary requirements (if any)

### QR Code Section
- Embedded QR code image
- Instructions for use
- "Your Digital Pass" title

### Instructions
- How to save the email
- How to present at entrance
- What happens during scanning
- Event day reminders

### Contact Information
- Participant's phone number
- Emergency contact details
- Support information

## 🔒 Security & Privacy

### Data Protection
- Emails sent individually (not BCC)
- QR codes contain only participant ID
- No sensitive data in email body
- Secure SMTP connection

### Email Limits
- Gmail: 500 emails/day
- Outlook: 300 emails/day
- Yahoo: 100 emails/day
- Custom: Varies by provider

## 🚨 Troubleshooting

### Common Issues

**"Authentication Failed"**
- Check your email and password
- For Gmail: Use app password, not regular password
- Enable 2-Step Verification first

**"SMTP Connection Error"**
- Check internet connection
- Verify SMTP server and port
- Try different email provider

**"Email Not Delivered"**
- Check spam folder
- Verify recipient email addresses
- Try sending to fewer recipients

**"QR Code Not Showing"**
- Check if QR code file exists
- Verify image format (PNG)
- Check file permissions

### Getting Help

1. **Check Logs**: Look at terminal output
2. **Test Configuration**: Use preview script first
3. **Verify Data**: Check Excel file format
4. **Contact Support**: If issues persist

## 📈 Best Practices

### Before Sending
1. **Preview First**: Always test with preview script
2. **Check Data**: Verify all email addresses are valid
3. **Test Configuration**: Send test email to yourself
4. **Backup Data**: Keep copy of participant list

### During Sending
1. **Monitor Progress**: Watch for errors
2. **Don't Interrupt**: Let process complete
3. **Check Limits**: Respect email provider limits
4. **Keep Logs**: Save terminal output

### After Sending
1. **Review Results**: Check success/failure counts
2. **Follow Up**: Contact participants who didn't receive
3. **Backup QR Codes**: Keep copies of all QR codes
4. **Test QR Codes**: Verify they work correctly

## 🎉 Success Checklist

- [ ] Email preview looks good
- [ ] Email configuration tested successfully
- [ ] All participants have valid email addresses
- [ ] QR codes generated for all participants
- [ ] Email sending completed
- [ ] Success count matches participant count
- [ ] QR codes tested and working
- [ ] Participants can access their digital passes

## 📞 Support

If you need help:
1. Check this guide first
2. Look at terminal error messages
3. Verify your email configuration
4. Test with preview script
5. Contact technical support

---

**🇰🇷 Ready to send beautiful Korea Week invitations! 🇰🇷**
