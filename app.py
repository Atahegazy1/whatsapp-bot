from flask import Flask, request, jsonify
from twilio.rest import Client
import os
import requests

app = Flask(__name__)

# إعدادات Twilio
ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
FROM_NUMBER = "whatsapp:+201555822228"  # رقم Twilio WhatsApp
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Content SIDs من Twilio (غيّر القيم دي بالـ SIDs الحقيقية بتاعتك)
TEMPLATE_CHOOSE_LANGUAGE = "HX20f316d6fdb0eb434ffa3c7d5de9f27c"
TEMPLATE_SERVICES_AR = "HX87ba643af656bb847a337b5ee07caf08"
TEMPLATE_SERVICES_EN = "HXce53e1f86338e0dc594c8e5cb0ec7da9"
TEMPLATE_ORDER_AR = "HXa904c71f31a01e0c234a6860d98bff06"
TEMPLATE_ORDER_EN = "HX66d98fc783df105eab8bbb60fd95f7c7"

# إعدادات Slack
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID")

def send_message_to_slack(text):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel": SLACK_CHANNEL_ID,
        "text": text
    }
    response = requests.post(url, json=payload, headers=headers)
    if not response.ok or not response.json().get("ok", False):
        print("Failed to send message to Slack:", response.text)

def send_message_to_whatsapp(to, body):
    client.messages.create(
        from_=FROM_NUMBER,
        to=to,
        body=body
    )

def send_template(to, content_sid):
    client.messages.create(
        from_=FROM_NUMBER,
        to=to,
        content_sid=content_sid
    )

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
    body = data.get("Body", "")
    payload = data.get("ButtonPayload") or data.get("ListSelectionId")

    # أرسل رسالة إلى Slack عند استقبال أي رسالة جديدة
    send_message_to_slack(f"📩 رسالة جديدة من {from_number}:\n{body}")

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
        # إرسال اختيار اللغة فقط عند أول تواصل
        send_template(from_number, TEMPLATE_CHOOSE_LANGUAGE)

    return "OK", 200

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json

    # الرد على تحدي URL Verification في Slack (عند التسجيل)
    if data.get("type") == "url_verification":
        return jsonify({"challenge": data.get("challenge")})

    # معالجة الأحداث العادية
    if data.get("type") == "event_callback":
        event = data.get("event", {})
        # نلتقط الرسائل الجديدة التي كتبها الفريق في القناة
        if event.get("type") == "message" and not event.get("bot_id"):
            channel = event.get("channel")
            text = event.get("text")

            # تأكد إن الرسالة في القناة الصحيحة فقط
            if channel == SLACK_CHANNEL_ID:
                if text.startswith("whatsapp:"):
                    try:
                        to_number, message_body = text.split(" ", 1)
                        send_message_to_whatsapp(to_number, message_body)
                    except Exception as e:
                        print("Error sending WhatsApp message:", e)

    return "OK", 200

if __name__ == "__main__":
    app.run(port=5000)
