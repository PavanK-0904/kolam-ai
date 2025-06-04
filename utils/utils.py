def clean_phone_number(phone):
    # Ensure phone is in WhatsApp format like "whatsapp:+91xxxxxxxxxx"
    phone = phone.strip()
    if not phone.startswith("whatsapp:"):
        if phone.startswith("+"):
            phone = "whatsapp:" + phone
        else:
            phone = "whatsapp:+" + phone
    return phone
