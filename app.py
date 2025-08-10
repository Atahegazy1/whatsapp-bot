from flask import Flask, request
from twilio.rest import Client
import os

app = Flask(__name__)

# بيانات Twilio (حطهم في متغيرات البيئة)
ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
FROM_NUMBER = "whatsapp:+201555822228"  # رقم واتساب Sandbox من Twilio
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# دالة إرسال رسالة نصية عادية
def send_text(to, body):
    message = client.messages.create(
        from_=FROM_NUMBER,
        to=to,
        body=body
    )
    print(f"Sent message: {message.sid} to {to}")

# قاعدة بيانات مؤقتة (بسيطة) لتخزين حالة المستخدم (في الذاكرة)
user_states = {}

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    data = request.form.to_dict()
    from_number = data.get("From")  # رقم المرسل
    incoming_msg = data.get("Body", "").strip().lower()

    print(f"Received message from {from_number}: {incoming_msg}")

    # الحالة الحالية للمستخدم، لو ما موجودة نخليها "start"
    state = user_states.get(from_number, "start")

    if state == "start":
        # نرسل ترحيب واختيارات اللغة
        msg = (
            "أهلاً! من فضلك اختر اللغة بالرقم:\n"
            "1. العربية\n"
            "2. English"
        )
        send_text(from_number, msg)
        user_states[from_number] = "language_selected"

    elif state == "language_selected":
        if incoming_msg == "1":
            # عربي - عرض الخدمات
            msg = (
                "اختر الخدمة:\n"
                "1. معلومات عن الشركة\n"
                "2. طلب خدمة\n"
                "3. الدعم الفني"
            )
            send_text(from_number, msg)
            user_states[from_number] = "service_ar"
        elif incoming_msg == "2":
            # English - show services
            msg = (
                "Please choose a service:\n"
                "1. About the company\n"
                "2. Order a service\n"
                "3. Technical support"
            )
            send_text(from_number, msg)
            user_states[from_number] = "service_en"
        else:
            send_text(from_number, "من فضلك أرسل 1 للعربية أو 2 للإنجليزية.")

    elif state == "service_ar":
        if incoming_msg == "1":
            send_text(from_number, "📌 نحن شركة متخصصة في تقديم أفضل الخدمات التقنية.")
            user_states[from_number] = "language_selected"  # نرجع للاختيار
        elif incoming_msg == "2":
            send_text(from_number, "يرجى إرسال طلبك، وسنقوم بمعالجته.")
            user_states[from_number] = "language_selected"
        elif incoming_msg == "3":
            send_text(from_number, "📞 للتواصل مع الدعم، أرسل لنا مشكلتك وسنقوم بالرد فورًا.")
            user_states[from_number] = "language_selected"
        else:
            send_text(from_number, "يرجى اختيار رقم من 1 إلى 3.")

    elif state == "service_en":
        if incoming_msg == "1":
            send_text(from_number, "📌 We are a company specialized in providing the best tech services.")
            user_states[from_number] = "language_selected"
        elif incoming_msg == "2":
            send_text(from_number, "Please send your order request, and we will process it.")
            user_states[from_number] = "language_selected"
        elif incoming_msg == "3":
            send_text(from_number, "📞 To contact support, please send your issue and we will reply promptly.")
            user_states[from_number] = "language_selected"
        else:
            send_text(from_number, "Please choose a number between 1 and 3.")

    else:
        send_text(from_number, "حدث خطأ، يرجى إعادة المحاولة.")
        user_states[from_number] = "start"

    return "OK", 200


if __name__ == "__main__":
    app.run(port=5000)
