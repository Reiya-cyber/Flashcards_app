import math, random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app, flash, session
from flask_mail import Message, Mail

def generateOTP():
    digits = '0123456789'
    otp = ""

    for i in range(6):
        otp += digits[math.floor(random.random() * 10)]
    return otp

def send_email(receiver):
    mail = Mail(current_app)
    otp = generateOTP()
    session['otp'] = otp
    print(f'######### {otp}')

    body = f"""
    <html>
    <body>
        <h2>Your OTP is: <strong>{otp}</strong></h2>
        <p>Please use this OTP to verify your identity. It is valid for 5 minutes.</p>
    </body>
    </html>
    """
    
    try:
        with current_app.app_context():
            msg = Message()
            msg.subject = 'Your One-Time Passcord'
            msg.recipients = [receiver]
            msg.html = body
            mail.send(msg)
            flash('OTP email was sent successfully!', category='success')

    except Exception as e:
        print(f"Error: {e}")

