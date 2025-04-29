import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_alert_email(subject, body, to_email):
    # Configure your SMTP server credentials here
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_user = 'aaronsonnie@gmail.com'  # Your Gmail address
    smtp_pass = 'vpls suzd ruoh sqmi'      # Use an app password, not your main password

    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
        server.quit()
        print(f"Alert email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send alert email: {e}")
