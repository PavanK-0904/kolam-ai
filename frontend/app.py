from flask import Flask, render_template, request, jsonify
from ai_agent import generate_response
from models import init_db
from utils import clean_phone_number

app = Flask(__name__)
init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send_message", methods=["POST"])
def send_message():
    user_message = request.form.get("message", "").strip()
    user_phone = request.form.get("phone", "").strip()
    if not user_message:
        return jsonify({"response": "Please enter a valid message."})
    if not user_phone:
        return jsonify({"response": "Please provide your phone number for session tracking."})

    phone_number = clean_phone_number(user_phone)
    response_text = generate_response(user_message, phone_number)
    return jsonify({"response": response_text})

if __name__ == "__main__":
    app.run(debug=True)
