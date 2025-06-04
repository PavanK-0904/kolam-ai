import google.generativeai as genai
from config import API_KEY
from models import ChatHistory, MemoryLog, SessionLocal
from messaging import send_whatsapp_message, send_booking_email
from datetime import datetime

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

kolam_info = """
Welcome to Kolam Serviced Apartments, your home away from home in Chennai! We're delighted to offer you a comfortable and memorable stay with us. Here's everything you need to know to make the most of your time here:

🏠 About Kolam:
- Located in the heart of Chennai, we offer modern serviced apartments with all the comforts of home.
- Whether you're here for business or leisure, our friendly staff is here to assist you 24/7.

🛎️ Services & Amenities:
- Daily Housekeeping
- Free Wi-Fi
- In-room Dining
- Airport Pickup & Drop (On Request)
- 24/7 Front Desk
- Laundry Service
- Local Tour Assistance
- Grocery Delivery

🕐 Check-in/Check-out:
- Check-in: 12:00 PM
- Check-out: 11:00 AM

📞 Contact Us Anytime:
- Front Desk: +91 98765 43210
- WhatsApp: +91 98765 43210
- Email: info@kolamstay.com

Thank you for choosing Kolam Serviced Apartments. We’re here to make your stay as pleasant and hassle-free as possible. Just send me a message if you need anything!
"""

session = SessionLocal()

def fetch_recent_chats(phone_number, limit=20):
    chats = session.query(ChatHistory).filter_by(phone_number=phone_number).order_by(ChatHistory.timestamp.desc()).limit(limit).all()
    chats.reverse()
    return chats

def fetch_recent_memory(phone_number, limit=10):
    mems = session.query(MemoryLog).filter_by(phone_number=phone_number).order_by(MemoryLog.timestamp.desc()).limit(limit).all()
    mems.reverse()
    return mems

def save_chat(phone_number, sender, message):
    chat = ChatHistory(phone_number=phone_number, sender=sender, message=message, timestamp=datetime.utcnow())
    session.add(chat)
    session.commit()

def save_memory(phone_number, memory):
    mem = MemoryLog(phone_number=phone_number, memory=memory, timestamp=datetime.utcnow())
    session.add(mem)
    session.commit()

def build_chat_context(phone_number):
    chats = fetch_recent_chats(phone_number)
    return "\n".join([f"{c.sender.capitalize()}: {c.message}" for c in chats])

def build_memory_log(phone_number):
    mems = fetch_recent_memory(phone_number)
    return "\n".join([m.memory for m in mems])

def parse_response(text):
    reply = ""
    intent = ""
    item = ""
    for line in text.split('\n'):
        if line.startswith("Reply:"):
            reply = line[len("Reply:"):].strip()
        elif line.startswith("Intent:"):
            intent = line[len("Intent:"):].strip()
        elif line.startswith("Item:"):
            item = line[len("Item:"):].strip()
    return reply, intent, item

def generate_response(user_input, phone_number):
    save_chat(phone_number, "guest", user_input)
    save_memory(phone_number, f"Guest said: {user_input}")

    prompt = f"""
You are Kolamai, a smart assistant for Kolam Serviced Apartments in Chennai. You greet guests warmly, help them with their needs, answer questions about the property, and handle service requests like cleaning or laundry.

Here is information about Kolam Serviced Apartments:
{kolam_info}

You maintain a memory log to understand the guest’s preferences and context.
Memory Log:
{build_memory_log(phone_number)}

Current Conversation:
{build_chat_context(phone_number)}

Guest’s new message:
\"\"\"{user_input}\"\"\"

Your task:
1. Generate a natural, friendly response as Kolamai.
2. Determine the user's intent:
    - "booking_request"
    - "service_request"
    - "emergency"
    - "general_query"
    - "room_service_order"
    - "maintenance_request"
    - "billing_inquiry"
    - "check_in_out_info"
3. If it's a service request or room service, extract the item if mentioned, else return "none".
4. Reply with this structure:

Reply: [your message to the guest]  
Intent: [intent]  
Item: [item if any, or "none"]
"""

    try:
        response = model.generate_content(prompt)
        full_reply = response.text.strip()

        reply, intent, item = parse_response(full_reply)

        save_chat(phone_number, "bot", reply)
        save_memory(phone_number, f"Kolamai replied: {reply}, Intent: {intent}, Item: {item}")

        action_result = ""
        if intent == "service_request" and item != "none":
            action_result = send_whatsapp_message(f"Guest has requested: {item}. Please arrange it.")
            reply += f" ({action_result})"

        elif intent == "booking_request":
            action_result = send_booking_email(user_input)
            reply += f" ({action_result})"

        elif intent == "emergency":
            action_result = send_whatsapp_message(f"Emergency alert: {user_input}")
            reply += f" ({action_result})"

        return reply

    except Exception as e:
        error_msg = "Sorry, I'm facing a technical issue. Please try again later."
        save_chat(phone_number, "bot", error_msg)
        save_memory(phone_number, f"Error: {e}")
        return error_msg
