import os

API_KEY = os.getenv("GEMINI_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = 'whatsapp:+14155238886'
MAID_PHONE_NUMBER = os.getenv("MAID_PHONE_NUMBER", "whatsapp:+917358444025")

EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RESERVATION_EMAIL = os.getenv("RESERVATION_EMAIL", EMAIL_USERNAME)
