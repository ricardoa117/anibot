import random
from telegram import Update
from telegram.ext import ContextTypes
from database.content import frases_motivadoras
from handlers.its_info import handle_its_info
from handlers.testing import pruebas_handler
from handlers.emergency import emergencia_handler

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manejador general de mensajes de texto"""
    user_message = update.message.text.lower()

    # Intenta manejar información sobre ITS
    if await handle_its_info(update, context):
        return

    # Centros de prueba
    if any(palabra in user_message for palabra in ["prueba", "centro", "dónde", "donde", "lugar", "clínica"]):
        await pruebas_handler(update, context)
        return

    # Emergencia
    if any(palabra in user_message for palabra in ["emergencia", "urgencia", "ayuda", "urgente", "peligro"]):
        await emergencia_handler(update, context)
        return

    # Frases motivadoras
    if any(palabra in user_message for palabra in ["gracias", "me ayudaste", "agradecido", "agradecida", "genial", "increíble"]):
        await update.message.reply_text(random.choice(frases_motivadoras))
        return

    # Localización específica
    if "puebla" in user_message and any(palabra in user_message for palabra in ["prueba", "centro", "dónde", "donde"]):
        await pruebas_handler(update, context)
        return

    # Respuesta por defecto
    default_responses = [
        "No estoy seguro de entender 😅. ¿Podrías reformular tu pregunta?",
        "Interesante pregunta. ¿Podrías ser más específico?",
        "No tengo información sobre eso en mi base de datos. ¿Te interesa saber sobre alguna ITS en particular?",
        "Usa /menu para ver las opciones disponibles o dime específicamente sobre qué quieres información."
    ]
    
    await update.message.reply_text(random.choice(default_responses))
