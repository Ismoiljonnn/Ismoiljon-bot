import telebot
import os
import http.server
import socketserver
import threading

# 1. Render-dagi "Port" xatosini yo'qotish uchun kichik server
def run_health_check():
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

# Serverni alohida oqimda ishga tushiramiz
threading.Thread(target=run_health_check, daemon=True).start()

TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "Salom, men Ismoiljonning botiman. Unga murojaatingiz, "
        "xizmatingiz yoki xabaringiz bo'lsa shu yerga yozib "
        "qoldirishingiz mumkin, men buni unga yuboraman. (Aloqa ma'lumotlar ham qoldiring)"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'video', 'document', 'voice'])
def forward_to_admin(message):
    try:
        user_info = f"📩 Yangi xabar!\n\n" \
                    f"👤 Kimdan: {message.from_user.first_name}\n" \
                    f"🆔 ID: {message.from_user.id}\n" \
                    f"🔗 Username: @{message.from_user.username if message.from_user.username else 'Mavjud emas'}"

        bot.send_message(ADMIN_ID, user_info)
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "Xabaringiz yuborildi. Tez orada javob olasiz.")
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")

if __name__ == "__main__":
    print("Bot Render-da muvaffaqiyatli ishga tushdi...")
    bot.infinity_polling()
