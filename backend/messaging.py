from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText
from config import *

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_whatsapp_message(body, to=MAID_PHONE_NUMBER):
    try:
        message = twilio_client.messages.create(
            from_=TWILIO_WHATSAPP_FROM,
            to=to,
            body=body
        )
        return "WhatsApp notification sent."
    except Exception as e:
        return f"Failed to send WhatsApp: {e}"

def send_booking_email(user_query):
    try:
        msg = MIMEText(f"New booking request: '{user_query}'")
        msg['Subject'] = "New Booking Request"
        msg['From'] = EMAIL_USERNAME
        msg['To'] = RESERVATION_EMAIL

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USERNAME, [RESERVATION_EMAIL], msg.as_string())
        return "Booking email sent."
    except Exception as e:
        return f"Failed to send booking email: {e}"
