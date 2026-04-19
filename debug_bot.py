import os
import sys

try:
    import telebot
    from telebot import types
    print("✅ Librería 'pyTelegramBotAPI' detectada correctamente.")
except ImportError:
    print("❌ ERROR: La librería 'pyTelegramBotAPI' NO está instalada.")
    print("👉 Por favor, ejecuta: pip install pyTelegramBotAPI")
    sys.exit()

# TOKEN del usuario (Extraído de su última captura/mensaje)
TOKEN = "8758265776:AAHRTZh5HbsjrvWZSaNpiygoZHnRR4h4ANE"

try:
    bot = telebot.TeleBot(TOKEN)
    me = bot.get_me()
    print(f"🤖 BOT IDENTIFICADO COMO: @{me.username} (ID: {me.id})")
    print("\n🚀 Conexión establecida con éxito.")
    print("🔔 Si le escribes al bot, deberías ver actividad abajo.")
    print("--------------------------------------------------")
except Exception as e:
    print(f"❌ ERROR DE TOKEN: No se pudo conectar. {e}")
    sys.exit()

@bot.message_handler(func=lambda message: True)
def debug_all(message):
    print(f"📩 ¡MENSAJE RECIBIDO!")
    print(f"   De: {message.from_user.first_name} (@{message.from_user.username})")
    print(f"   Texto: {message.text}")
    print(f"   Chat ID: {message.chat.id}")
    bot.reply_to(message, f"¡Hola {message.from_user.first_name}! Conexión confirmada.\nTu ID de Chat es: {message.chat.id}\nCopia este número para tu configuración.")

try:
    print("\n🤖 ESPERANDO MENSAJES... Escribe CUALQUIER COSA a tu bot en Telegram.")
    bot.polling(none_stop=True)
except Exception as e:
    print(f"❌ ERROR DE CONEXIÓN DURANTE EL POLLING: {e}")
