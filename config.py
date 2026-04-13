import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Configuration
TOKEN = os.environ.get('TELEGRAM_TOKEN')
if not TOKEN:
    raise ValueError("No se encontró el token de Telegram. Configura la variable de entorno TELEGRAM_TOKEN.")

# Logging Configuration
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
