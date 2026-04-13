from telegram import Update
from telegram.ext import ContextTypes

async def emergencia_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /emergencia - Recursos de ayuda y emergencia"""
    texto = """🆘 *Recursos de ayuda y emergencia*

*Líneas de atención:*
- Línea de la Vida: 800 911 2000 (Atención psicológica)
- Centro de Atención al Suicida: +52 55 5259 8121
- Emergencias: 911

*Si crees que has estado expuesto a VIH:*
La PEP (profilaxis posexposición) debe iniciarse dentro de las 72 horas posteriores a la exposición. Contacta inmediatamente:
- CAPASITS Puebla: +52 222 123 4567
- Hospitales generales o de especialidad

*Violencia sexual:*
- Línea de emergencia por violencia: 800 422 5256
- Atención en centros de salud: Deben proporcionarte PEP, anticoncepción de emergencia y apoyo psicológico.

*Recuerda:* En situaciones de emergencia, acude siempre a un centro de salud lo antes posible."""
    
    await update.message.reply_text(texto, parse_mode='Markdown')