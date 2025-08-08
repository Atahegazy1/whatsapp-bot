from flask import Flask, request
from twilio.rest import Client
import os

app = Flask(__name__)

# بيانات Twilio
ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
FROM_NUMBER = "whatsapp:+14155238886"  # رقم واتساب الخاص بـ Twilio
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Content SIDs من Twilio (غيّر القيم دي بالـ SIDs الحقيقية بتاعتك)
TEMPLATE_CHOOSE_LANGUAGE = "HX20f316d6fdb0eb434ffa3c7d5de9f27c"
TEMPLATE_SERVICES_AR = "HX87ba643af656bb847a337b5ee07caf08"
TEMPLATE_SERVICES_EN = "HXce53e1f86338e0dc594c8e5cb0ec7da9"
TEMPLATE_ORDER_AR = "HXa904c71f31a01e0c234a6860d98bff06"
TEMPLATE_ORDER_EN = "HX66d98fc783df105eab8bbb60fd95f7c7"

# دالة إرسال Template
def send_template(to, content_sid):
    client.messages.create(
        from_=FROM_NUMBER,
        to=to,
        content_sid=content_sid
    )

# دالة إرسال نصوص عادية
def send_text(to, body):
    client.messages.create(
        from_=FROM_NUMBER,
        to=to,
        body=body
    )

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    data = request.form.to_dict()
    from_number = data.get("From")

    payload = data.get("ButtonPayload") or data.get("ListSelectionId")

    if payload:
        # اختيار اللغة
        if payload == "LANG_AR":
            send_template(from_number, TEMPLATE_SERVICES_AR)
        elif payload == "LANG_EN":
            send_template(from_number, TEMPLATE_SERVICES_EN)

        # خدمات بالعربي
        elif payload == "SERVICE_INFO_AR":
            send_text(from_number, "📌 نحن شركة متخصصة في تقديم أفضل الخدمات التقنية.")
        elif payload == "SERVICE_ORDER_AR":
            send_template(from_number, TEMPLATE_ORDER_AR)
        elif payload == "SERVICE_SUPPORT_AR":
            send_text(from_number, "📞 للتواصل مع الدعم، أرسل لنا مشكلتك وسنقوم بالرد فورًا.")

        # خدمات بالإنجليزي
        elif payload == "SERVICE_INFO_EN":
            send_text(from_number, "📌 We are a company specialized in providing the best tech services.")
        elif payload == "SERVICE_ORDER_EN":
            send_template(from_number, TEMPLATE_ORDER_EN)
        elif payload == "SERVICE_SUPPORT_EN":
            send_text(from_number, "📞 To contact support, please send your issue and we will reply promptly.")

        # طلب خدمة بالعربي
        elif payload == "ORDER_WEB_AR":
            send_text(from_number, "✅ تم تسجيل طلب تصميم موقعك.")
        elif payload == "ORDER_APP_AR":
            send_text(from_number, "✅ تم تسجيل طلب تطبيق الموبايل.")

        # طلب خدمة بالإنجليزي
        elif payload == "ORDER_WEB_EN":
            send_text(from_number, "✅ Website design request has been submitted.")
        elif payload == "ORDER_APP_EN":
            send_text(from_number, "✅ Mobile app request has been submitted.")

    else:
        # أول رسالة من العميل
        send_text(from_number, "👋 أهلاً وسهلاً بك في شركتنا!\nنحن سعداء بخدمتك ❤️")
        send_template(from_number, TEMPLATE_CHOOSE_LANGUAGE)

    return "OK", 200

if __name__ == "__main__":
    app.run(port=5000)
