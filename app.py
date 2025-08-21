import logging
import os
import random
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# --- Configuración de logging ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Token desde variable de entorno ---
TOKEN = os.environ.get('TELEGRAM_TOKEN')
if not TOKEN:
    logger.error("No se encontró el token de Telegram. Configura la variable de entorno TELEGRAM_TOKEN.")
    exit(1)

# --- Base de datos de información ---
info_db = {
    "VIH": """🧬 *VIH (Virus de la Inmunodeficiencia Humana)*

Afecta el sistema inmunológico. Se transmite por relaciones sexuales sin protección, sangre o de madre a hijo.

💡 *Dato útil:* El tratamiento antirretroviral permite llevar una vida larga y saludable.

¿Quieres saber sobre pruebas, prevención o tratamiento?""",

    "VPH": """🌿 *VPH (Virus del Papiloma Humano)*

Es muy común. Puede causar verrugas genitales y algunos tipos de cáncer.

🛡️ *Tip:* La vacuna contra el VPH es altamente efectiva.

¿Te interesa saber sobre síntomas o cómo prevenirlo?""",

    "Clamidia": """🧫 *Clamidia*

Una ITS silenciosa pero común. Puede causar dolor al orinar y secreciones.

📍 Se trata fácilmente con antibióticos. ¡No lo ignores!""",

    "Gonorrea": """🧪 *Gonorrea*

Puede afectar genitales, recto y garganta. A veces no da síntomas.

💊 Se trata con antibióticos. ¡Hazte pruebas si tienes dudas!""",

    "Herpes": """🔥 *Herpes Genital*

Causa ampollas dolorosas. No tiene cura, pero sí tratamiento para controlar brotes.

💬 Hablarlo con tu pareja es clave. No estás solo.""",

    "Sífilis": """🧠 *Sífilis*

Puede pasar desapercibida. Si no se trata, afecta órganos internos.

🧪 Se detecta con análisis de sangre. ¡Es curable si se detecta a tiempo!""",

    "Prevención General": """🛡️ *Prevención de ITS*

- Usa condón en todas tus relaciones sexuales.
- Hazte pruebas regularmente.
- Habla abiertamente sobre salud sexual.

¿Quieres saber dónde hacerte pruebas en Puebla? Escribe 'pruebas Puebla'."""
}

curiosidades = [
    "🔍 El VIH no se transmite por abrazos, besos ni compartir utensilios.",
    "💉 La prueba rápida de VIH puede darte resultados en menos de 30 minutos.",
    "🧠 Hablar de ITS no es tabú, es salud. ¡Infórmate y comparte!",
    "🌎 Más del 50% de las personas sexualmente activas tendrán VPH en algún momento.",
    "🧬 El herpes puede transmitirse incluso sin síntomas visibles."
]

mitos = [
    "❌ *Mito:* Solo las personas promiscuas tienen ITS.\n✅ *Verdad:* Cualquiera puede tener una ITS. Lo importante es cuidarse.",
    "❌ *Mito:* Si no tengo síntomas, no tengo ITS.\n✅ *Verdad:* Muchas ITS no presentan síntomas. ¡Hazte pruebas!",
    "❌ *Mito:* El condón protege de todo.\n✅ *Verdad:* Protege mucho, pero no de infecciones como el VPH si hay contacto con piel infectada."
]

frases_motivadoras = [
    "🌄 Cada paso que das hacia tu salud es un acto de amor propio.",
    "💬 Hablar de ITS no te hace vulnerable, te hace valiente.",
    "🧭 La información es tu brújula. ¡Sigue explorando con confianza!"
]

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = """
¡Hola! 👋 Soy tu bot de confianza para hablar de salud sexual sin tabúes.

📚 Aquí encontrarás información clara, sin juicios.
💬 Si tienes dudas, pregúntame con confianza. Estoy aquí para ayudarte.

Usa /menu para comenzar, /dato para aprender algo curioso, o /mitos para derribar prejuicios.
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
        '¿Sobre qué ITS quieres saber más? Selecciona una opción:',
        reply_markup=reply_markup
    )

async def dato(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(curiosidades))

async def mitos_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(mitos), parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()

    # Reconocimiento por palabra clave
    for key in info_db:
        if key.lower() in user_message:
            await update.message.reply_text(info_db[key], parse_mode='Markdown')
            return

    # Frases motivadoras
    if "gracias" in user_message or "me ayudaste" in user_message:
        await update.message.reply_text(random.choice(frases_motivadoras))
        return

    # Localización
    if "puebla" in user_message and "prueba" in user_message:
        await update.message.reply_text("📍 Puedes hacerte pruebas en el CAPASITS Puebla o en centros de salud locales. Busca el más cercano en https://www.gob.mx/salud")
        return

    await update.message.reply_text("No entendí bien 😅. Usa /menu para ver opciones o dime sobre qué ITS quieres saber.")

# --- Construcción de la app Telegram ---
def build_app():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("dato", dato))
    application.add_handler(CommandHandler("mitos", mitos_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    return application

# --- Ejecución local ---
if __name__ == '__main__':
    build_app().run_polling()
