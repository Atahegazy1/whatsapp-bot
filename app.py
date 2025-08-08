from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    msg = request.form.get("Body").strip().lower()
    resp = MessagingResponse()
    reply = resp.message()

    # أول رسالة ترحيبية
    if msg in ["hi", "hello", "مرحبا", "السلام عليكم"]:
        reply.body("اختر اللغة:\n1️⃣ عربي\n2️⃣ English")
    
    # لو اختار عربي
    elif msg == "1":
        reply.body("أهلاً بك! 😊\nهذه القائمة الرئيسية بالعربي:\n- الخيار 1\n- الخيار 2")
    
    # لو اختار انجليزي
    elif msg == "2":
        reply.body("Welcome! 😊\nHere is the main menu in English:\n- Option 1\n- Option 2")
    
    # أي حاجة تانية
    else:
        reply.body("الرجاء اختيار:\n1️⃣ عربي\n2️⃣ English")

    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
