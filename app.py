from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# نخزن اختيار اللغة لكل رقم مستخدم
user_language = {}

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    from_number = request.values.get('From', '')
    incoming_msg = request.values.get('Body', '').strip().lower()
    resp = MessagingResponse()
    msg = resp.message()

    # لو المستخدم لسه مختارش لغة
    if from_number not in user_language:
        if incoming_msg in ["1", "عربي", "arabic"]:
            user_language[from_number] = "ar"
            msg.body("✅ تم اختيار اللغة العربية.\n\nاكتب /start لعرض القائمة.")
        elif incoming_msg in ["2", "english", "انجليزي"]:
            user_language[from_number] = "en"
            msg.body("✅ English selected.\n\nType /start to show menu.")
        else:
            msg.body(
                "🌐 اختر اللغة / Choose your language:\n"
                "1️⃣ عربي\n"
                "2️⃣ English"
            )
        return str(resp)

    # لو اللغة العربية
    if user_language[from_number] == "ar":
        if incoming_msg in ["/start", "قائمة"]:
            msg.body(
                "📋 *القائمة:*\n"
                "1️⃣ /time - معرفة الوقت\n"
                "2️⃣ /date - معرفة التاريخ\n"
                "3️⃣ /help - المساعدة\n"
            )
        elif incoming_msg == "/time":
            from datetime import datetime
            now = datetime.now().strftime("%H:%M:%S")
            msg.body(f"⏰ الوقت الحالي هو: {now}")
        elif incoming_msg == "/date":
            from datetime import datetime
            today = datetime.now().strftime("%Y-%m-%d")
            msg.body(f"📅 تاريخ اليوم هو: {today}")
        elif incoming_msg == "/help":
            msg.body("💡 اكتب أحد الأوامر من القائمة لبدء الاستخدام.")
        else:
            msg.body("⚠️ أمر غير معروف. اكتب /start لعرض القائمة.")

    # لو اللغة الإنجليزية
    elif user_language[from_number] == "en":
        if incoming_msg in ["/start", "menu"]:
            msg.body(
                "📋 *Menu:*\n"
                "1️⃣ /time - Show current time\n"
                "2️⃣ /date - Show today's date\n"
                "3️⃣ /help - Help"
            )
        elif incoming_msg == "/time":
            from datetime import datetime
            now = datetime.now().strftime("%H:%M:%S")
            msg.body(f"⏰ Current time: {now}")
        elif incoming_msg == "/date":
            from datetime import datetime
            today = datetime.now().strftime("%Y-%m-%d")
            msg.body(f"📅 Today's date: {today}")
        elif incoming_msg == "/help":
            msg.body("💡 Type any command from the menu to start.")
        else:
            msg.body("⚠️ Unknown command. Type /start to see the menu.")

    return str(resp)

if __name__ == "__main__":
   
