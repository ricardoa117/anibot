import random
from telegram import Update
from telegram.ext import ContextTypes
from database.content import curiosidades, mitos
from handlers.commands import menu

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja clics en botones inline"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "mas_datos":
        await query.edit_message_text(random.choice(curiosidades))
    elif query.data == "mas_mitos":
        mito = random.choice(mitos)
        texto = f"{mito['mito']}\n\n{mito['verdad']}"
        await query.edit_message_text(texto, parse_mode='Markdown')
    elif query.data == "menu_principal":
        await menu(update, context)