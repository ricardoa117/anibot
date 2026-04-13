from telegram import Update
from telegram.ext import ContextTypes
from database.centers import centros_puebla

async def pruebas_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /pruebas - Muestra centros de prueba disponibles"""
    texto = "📍 *Centros de prueba en Puebla:*
\n"
    for centro, info in centros_puebla.items():
        texto += f"*{centro}*\n"
        texto += f"📍 {info['direccion']}\n"
        texto += f"🕒 {info['horario']}\n"
        texto += f"💰 {info['costo']}\n"
        texto += f"📞 {info['telefono']}\n"
        texto += f"🩺 Servicios: {', '.join(info['servicios'])}\n\n"
    
    texto += "¿Necesitas ayuda para elegir un centro o información sobre otras localidades?"
    await update.message.reply_text(texto, parse_mode='Markdown')
