from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# تخزين الحالات مؤقتاً في الذاكرة (ينفع لاحقًا نستبدله بقاعدة بيانات)
user_states = {}

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    from_number = request.form.get("From")
    msg = request.form.get("Body", "").strip().lower()

    resp = MessagingResponse()
    reply = resp.message()

    # لو أول مرة المستخدم يتواصل
    if from_number not in user_states:
        user_states[from_number] = "choose_language"
        reply.body("اختر اللغة:\n1️⃣ عربي\n2️⃣ English")
        return str(resp)

    state = user_states[from_number]

    # المرحلة الأولى: اختيار اللغة
    if state == "choose_language":
        if msg == "1":
            user_states[from_number] = "menu_ar"
            reply.body("أهلاً بك! 😊\nاختر من القائمة:\n1️⃣ معلومات\n2️⃣ تواصل معنا\n0️⃣ رجوع")
        elif msg == "2":
            user_states[from_number] = "menu_en"
            reply.body("Welcome! 😊\nChoose from menu:\n1️⃣ Info\n2️⃣ Contact us\n0️⃣ Back")
        else:
            reply.body("الرجاء اختيار:\n1️⃣ عربي\n2️⃣ English")

    # القائمة العربية
    elif state == "menu_ar":
        if msg == "1":
            reply.body("📄 هذه هي المعلومات المطلوبة.")
        elif msg == "2":
            reply.body("📞 يمكنك التواصل معنا على: example@example.com")
        elif msg == "0":
            user_states[from_number] = "choose_language"
            reply.body("اختر اللغة:\n1️⃣ عربي\n2️⃣ English")
        else:
            reply.body("❌ اختيار غير صحيح.\nاختر:\n1️⃣ معلومات\n2️⃣ تواصل معنا\n0️⃣ رجوع")

    # القائمة الإنجليزية
    elif state == "menu_en":
        if msg == "1":
            reply.body("📄 Here is the requested information.")
        elif msg == "2":
            reply.body("📞 You can contact us at: example@example.com")
        elif msg == "0":
            user_states[from_number] = "choose_language"
            reply.body("Choose language:\n1️⃣ Arabic\n2️⃣ English")
        else:
            reply.body("❌ Invalid choice.\nChoose:\n1️⃣ Info\n2️⃣ Contact us\n0️⃣ Back")

    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
