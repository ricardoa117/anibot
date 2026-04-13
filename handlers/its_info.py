import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.its_database import info_db
from database.content import curiosidades, mitos, frases_motivadoras

async def handle_its_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja solicitudes de información sobre ITS específicas"""
    user_message = update.message.text.lower()

    for key in info_db:
        if key.lower() in user_message:
            info = info_db[key]["info"]
            recursos = info_db[key]["recursos"]
            
            # Crear botones inline para recursos
            keyboard = []
            for recurso in recursos:
                keyboard.append([InlineKeyboardButton(recurso["text"], url=recurso["url"])])
            
            # Añadir botón para más información
            keyboard.append([InlineKeyboardButton("📋 Volver al menú", callback_data="menu_principal")])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(info, parse_mode='Markdown', reply_markup=reply_markup)
            return
    
    return False

async def dato(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /dato - Dato curioso aleatorio"""
    dato = random.choice(curiosidades)
    keyboard = [[InlineKeyboardButton("📚 Más datos curiosos", callback_data="mas_datos")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(dato, reply_markup=reply_markup)

async def mitos_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /mitos - Mitos y realidades aleatorios"""
    mito = random.choice(mitos)
    texto = f"{mito['mito']}\n\n{mito['verdad']}"
    keyboard = [[InlineKeyboardButton("🧠 Más mitos y realidades", callback_data="mas_mitos")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(texto, parse_mode='Markdown', reply_markup=reply_markup)