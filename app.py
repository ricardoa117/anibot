import logging
import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Configura logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Obtener el token de las variables de entorno (Heroku)
TOKEN = os.environ.get('TELEGRAM_TOKEN')

if not TOKEN:
    logger.error("No se encontró el token de Telegram. Configura la variable de entorno TELEGRAM_TOKEN.")
    exit(1)

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = """
¡Hola! 👋 Soy un bot informativo sobre Infecciones de Transmisión Sexual (ITS).

📌 *Mi objetivo es brindarte información clara y veraz.*
🔬 *Recuerda:* Yo *NO* puedo diagnosticar. Si tienes preocupaciones, consulta siempre a un profesional de la salud.

Usa el comando /menu para ver la lista de ITS sobre las que puedo informarte.
"""
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("VIH"), KeyboardButton("VPH")],
        [KeyboardButton("Clamidia"), KeyboardButton("Gonorrea")],
        [KeyboardButton("Herpes"), KeyboardButton("Sífilis")],
        [KeyboardButton("Prevención General")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(
        '¿Sobre qué quieres información? Selecciona una opción:',
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    info_db = {
        "VIH": "info...",
        "VPH": "info...",
        "Prevención General": "info..."
    }
    response_text = info_db.get(user_message, "Opción no reconocida. Usa /menu o escribe /start.")
    await update.message.reply_text(response_text, parse_mode='Markdown')

# --- Construcción de la app Telegram ---
def build_app():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    return application

# Solo corre polling si lo ejecutas localmente
if __name__ == '__main__':
    build_app().run_polling()