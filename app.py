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

# إعدادات Slack
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID")
SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET")  # لو عايز تحقق سلامة التوقيع (اختياري)

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

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    data = request.form.to_dict()
    from_number = data.get("From")
    body = data.get("Body", "")
    payload = data.get("ButtonPayload") or data.get("ListSelectionId")

    # أرسل رسالة إلى Slack عند استقبال أي رسالة جديدة
    send_message_to_slack(f"📩 رسالة جديدة من {from_number}:\n{body}")

    # التعامل مع الأزرار والقوائم لو في Payload
    if payload:
        # ... (يمكن تضيف هنا الأكواد السابقة حسب حاجتك)
        pass
    else:
        # يمكنك إرسال رسالة ترحيبية أو تركها بدون رد
        pass

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
            user = event.get("user")
            text = event.get("text")

            # تأكد إن الرسالة في القناة الصحيحة فقط
            if channel == SLACK_CHANNEL_ID:
                # مثال: يجب أن يكون الرد بداية برقم الواتساب المستلم من Slack (أو طريقة تربطها)
                # هنا تفترض إن الرسالة تبدأ برقم واتساب المستلم (لتبسيط المثال)
                # صيغة الرسالة: "whatsapp:+20XXXXXXXXX رسالة الرد هنا"
                if text.startswith("whatsapp:"):
                    try:
                        to_number, message_body = text.split(" ", 1)
                        send_message_to_whatsapp(to_number, message_body)
                    except Exception as e:
                        print("Error sending WhatsApp message:", e)

    return "OK", 200

if __name__ == "__main__":
    app.run(port=5000)