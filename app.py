import logging
import os
import random
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

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

# --- Base de datos ampliada de información sobre ITS ---
info_db = {
    "VIH": {
        "info": """🧬 *VIH (Virus de la Inmunodeficiencia Humana)*

*¿Qué es?*
El VIH ataca y debilita el sistema inmunológico, específicamente las células CD4. Sin tratamiento, puede evolucionar a SIDA.

*Transmisión:*
- Relaciones sexuales sin protección (vaginal, anal, oral)
- Compartir agujas o jeringas contaminadas
- De madre a hijo durante el embarazo, parto o lactancia
- Transfusiones de sangre no seguras (hoy es muy raro en países con controles)

*Síntomas iniciales (2-4 semanas después de la infección):*
- Fiebre, escalofríos
- Erupción cutánea
- Sudores nocturnos
- Dolores musculares
- Dolor de garganta
- Fatiga
- Ganglios linfáticos inflamados
- Úlceras bucales

*Tratamiento:*
La terapia antirretroviral (TAR) consiste en una combinación de medicamentos que:
- Reducen la carga viral hasta niveles indetectables
- Preservan la función inmunológica
- Previenen la transmisión a otras personas

*Prevención:*
- Uso correcto de preservativos
- Profilaxis preexposición (PrEP) para personas en alto riesgo
- Profilaxis posexposición (PEP) dentro de las 72 horas tras posible exposición
- No compartir agujas
- Pruebas regulares

*Dato crucial:* Indetectable = Intransmisible (I=I). Personas con carga viral indetectable no transmiten el VIH por vía sexual.""",
        "recursos": [
            {"text": "📊 Estadísticas actualizadas", "url": "https://www.who.int/hiv/data/es/"},
            {"text": "📍 Centros de prueba cerca", "url": "https://www.gob.mx/salud/acciones-y-programas/pruebas-de-vih"},
            {"text": "📱 Línea de ayuda", "url": "tel:+525533553333"}
        ]
    },
    
    "VPH": {
        "info": """🌿 *VPH (Virus del Papiloma Humano)*

*¿Qué es?*
El VPH es la ITS más común, con más de 200 tipos virales. Algunos pueden causar verrugas genitales y otros cáncer.

*Transmisión:*
- Contacto piel a piel durante actividad sexual
- Sexo vaginal, anal u oral
- Puede transmitirse incluso cuando la persona infectada no tiene síntomas

*Tipos de VPH:*
- De bajo riesgo: Causan verrugas genitales (tipos 6 y 11)
- De alto riesgo: Pueden causar cáncer (tipos 16, 18, 31, 33, 45, 52, 58)

*Cánceres relacionados:*
- Cuello uterino
- Vulva
- Vagina
- Pene
- Ano
- Garganta

*Detección:*
- Prueba de Papanicolaou (citología vaginal)
- Prueba de VPH
- Inspección visual con ácido acético (IVA)

*Prevención:*
- Vacunación (recomendada para preadolescentes hasta los 26 años, y algunos hasta 45)
- Uso de preservativos (reduce pero no elimina completamente el riesgo)
- Exámenes ginecológicos regulares

*Tratamiento:*
No existe tratamiento para el virus mismo, pero sí para los problemas de salud que causa:
- Verrugas genitales: cremas, crioterapia, cirugía
- Lesiones precancerosas: seguimiento, extirpación
- Cáncer: tratamiento oncológico estándar""",
        "recursos": [
            {"text": "💉 Información sobre vacunación", "url": "https://www.gob.mx/salud/acciones-y-programas/vacunacion-contra-vph"},
            {"text": "📋 Guía de detección temprana", "url": "https://www.cancer.org/es/cancer/causas-del-cancer/agentes-infecciosos/vph.html"}
        ]
    },
    
    "Clamidia": {
        "info": """🧫 *Clamidia*

*¿Qué es?*
Infección bacteriana causada por Chlamydia trachomatis. Es una de las ITS bacterianas más comunes.

*Transmisión:*
- Sexo vaginal, anal u oral sin protección
- De madre a hijo durante el parto

*Síntomas (aparecen 1-3 semanas después de la exposición):*
*En mujeres:*
- Flujo vaginal anormal
- Sangrado entre periodos
- Dolor durante las relaciones sexuales
- Ardor al orinar
- Dolor abdominal bajo

*En hombres:*
- Secreción del pene
- Ardor al orinar
- Dolor e inflamación testicular

*Complicaciones si no se trata:*
*En mujeres:*
- Enfermedad inflamatoria pélvica (EIP)
- Embarazo ectópico
- Infertilidad
- Dolor pélvico crónico

*En hombres:*
- Epididimitis (inflamación del epidídimo)
- Infertilidad (poco común)

*Tratamiento:*
- Antibióticos (azitromicina o doxiciclina)
- Las parejas sexuales deben tratarse simultáneamente
- Abstinencia sexual hasta completar el tratamiento

*Prevención:*
- Uso correcto de preservativos
- Pruebas regulares para personas sexualmente activas""",
        "recursos": [
            {"text": "🩺 Síntomas y diagnóstico", "url": "https://www.cdc.gov/std/spanish/clamidia/stdfact-chlamydia-s.htm"}
        ]
    },
    
    "Gonorrea": {
        "info": """🧪 *Gonorrea*

*¿Qué es?*
Infección bacteriana causada por Neisseria gonorrhoeae que puede infectar tracto genital, recto y garganta.

*Transmisión:*
- Sexo vaginal, anal u oral sin protección
- De madre a hijo durante el parto

*Síntomas (aparecen 2-14 días después de la exposición):*
*En mujeres (a menudo asintomáticas):*
- Secreción vaginal
- Ardor al orinar
- Sangrado entre periodos
- Dolor abdominal

*En hombres:*
- Secreción blanca, amarilla o verde del pene
- Ardor al orinar
- Dolor testicular

*En recto:*
- Secreción
- Picazón anal
- Dolor
- Sangrado

*Complicaciones si no se trata:*
*En mujeres:*
- Enfermedad inflamatoria pélvica (EIP)
- Embarazo ectópico
- Infertilidad
- Dolor abdominal crónico

*En hombres:*
- Epididimitis
- Infertilidad (raro)

*En ambos sexos:*
- Diseminación a articulaciones (artritis gonocócica)
- Mayor riesgo de contraer/transmitir VIH

*Resistencia a antibióticos:*
La gonorrea ha desarrollado resistencia a muchos antibióticos, por lo que el tratamiento debe seguir las recomendaciones actualizadas.

*Tratamiento:*
- Terapia dual (ceftriaxona + azitromicina)
- Las parejas sexuales deben tratarse
- Prueba de curación recomendada""",
        "recursos": [
            {"text": "⚠️ Alertas sobre resistencia", "url": "https://www.who.int/news-room/fact-sheets/detail/gonorrhoea-(neisseria-gonorrhoeae)"}
        ]
    },
    
    "Herpes": {
        "info": """🔥 *Herpes Genital*

*¿Qué es?*
Infección viral causada por el virus del herpes simple (VHS). Existen dos tipos: VHS-1 (principalmente oral) y VHS-2 (principalmente genital).

*Transmisión:*
- Contacto directo con lesiones o fluidos de persona infectada
- Sexo vaginal, anal u oral
- Contacto piel a piel en área genital
- La transmisión puede ocurrir incluso sin síntomas visibles

*Síntomas del primer brote (2-20 días después de la exposición):*
- Ampollas o llagas dolorosas en área genital, recto o muslos
- Picazón o ardor
- Dolor al orinar
- Secreción vaginal
- Síntomas similares a la gripe (fiebre, dolor corporal)

*Brotes recurrentes:*
- Generalmente más leves que el primer brote
- Hormigueo o picazón antes de la aparición de lesiones
- Las lesiones sanan más rápido (2-7 días)

*Factores desencadenantes de brotes:*
- Estrés
- Enfermedad o fiebre
- Exposición al sol
- Menstruación
- Cirugía
- Sistema inmunológico debilitado

*Tratamiento:*
No existe cura, pero los antivirales pueden:
- Acortar la duración de los brotes
- Reducir la frecuencia de brotes
- Disminuir el riesgo de transmisión

*Prevención:*
- Uso de preservativos (reduce pero no elimina el riesgo)
- Evitar contacto sexual durante brotes
- Terapia supresiva con antivirales
- Comunicación abierta con parejas sexuales""",
        "recursos": [
            {"text": "🩹 Manejo de brotes", "url": "https://www.plannedparenthood.org/es/temas-de-salud/enfermedades-de-transmision-sexual-ets/herpes"}
        ]
    },
    
    "Sífilis": {
        "info": """🧠 *Sífilis*

*¿Qué es?*
Infección bacteriana causada por Treponema pallidum que progresa por etapas si no se trata.

*Etapas y síntomas:*
*Sífilis primaria (3-90 días después de la exposición):*
- Chancro (úlcera indolora) en sitio de infección
- Ganglios linfáticos inflamados

*Sífilis secundaria (4-10 semanas después del chancro):*
- Erupción cutánea (incluye palmas y plantas)
- Fiebre
- Dolor de garganta
- Pérdida de peso
- Caída del cabello
- Dolor de cabeza
- Dolor muscular

*Sífilis latente:*
- Sin síntomas visibles
- La infección permanece en el cuerpo

*Sífilis terciaria (10-30 años después de la infección inicial):*
- Daño a órganos internos (cerebro, nervios, ojos, corazón, vasos sanguíneos, hígado, huesos)
- Puede ser mortal

*Transmisión:*
- Contacto directo con chancro durante sexo vaginal, anal u oral
- De madre a hijo (sífilis congénita)

*Diagnóstico:*
- Pruebas de sangre
- Examen de líquido de lesiones

*Tratamiento:*
- Penicilina (único tratamiento efectivo)
- Dosis varía según etapa
- Seguimiento con pruebas serológicas

*Sífilis congénita:*
Puede causar muerte fetal, parto prematuro, discapacidades graves o muerte del recién nacido.""",
        "recursos": [
            {"text": "📈 Datos epidemiológicos", "url": "https://www.gob.mx/salud/acciones-y-programas/historial-de-la-situacion-de-la-sifilis-en-mexico"}
        ]
    },
    
    "Prevención General": {
        "info": """🛡️ *Prevención Integral de ITS*

*Métodos de barrera:*
- Preservativos masculinos (85-98% efectivos)
- Preservativos femeninos (79-95% efectivos)
- Barreras bucales (dental dams) para sexo oral

*Vacunación:*
- VPH: recomendada para preadolescentes hasta 26 años
- Hepatitis A y B: recomendada para todos

*Pruebas regulares:*
- Anual para personas sexualmente activas
- Después de parejas nuevas
- Antes de iniciar relación sin preservativos

*Comunicación:*
- Hablar abiertamente sobre historial sexual con parejas
- Negociar el uso de protección
- Divulgar estado de ITS

*Reducción de riesgos:*
- Limitar número de parejas sexuales
- Evitar alcohol/drogas en contextos sexuales
- Conocer los límites y consentimiento

*Profilaxis:*
- PrEP (profilaxis preexposición) para VIH
- PEP (profilaxis posexposición) para VIH

*Señales de alerta para consultar:*
- Secreciones inusuales
- Llagas, bultos o erupciones
- Dolor al orinar o durante sexo
- Sangrado entre periodos
- Dolor abdominal bajo""",
        "recursos": [
            {"text": "🗺️ Mapa de centros de salud", "url": "https://www.gob.mx/salud/acciones-y-programas/directorio-de-unidades-medicas"},
            {"text": "📞 Línea de orientación", "url": "tel:+525533553333"}
        ]
    },
    
    "Hepatitis B": {
        "info": """🟡 *Hepatitis B*

*¿Qué es?*
Infección viral que afecta el hígado, causada por el virus de la hepatitis B (VHB).

*Transmisión:*
- Contacto con sangre, semen u otros fluidos corporales
- Relaciones sexuales sin protección
- Compartir agujas o jeringas
- De madre a hijo durante el parto

*Síntomas:*
- Fatiga
- Náuseas y vómitos
- Dolor abdominal
- Orina oscura
- Heces color arcilla
- Ictericia (coloración amarillenta de piel y ojos)

*Complicaciones:*
- Hepatitis crónica
- Cirrosis hepática
- Cáncer de hígado
- Insuficiencia hepática aguda

*Prevención:*
- Vacunación (serie de 3 dosis)
- Uso de preservativos
- No compartir agujas u objetos personales (cepillos de dientes, rasuradoras)

*Tratamiento:*
- Para casos agudos: reposo, hidratación y manejo de síntomas
- Para casos crónicos: medicamentos antivirales, interferón
- Trasplante hepático en casos avanzados""",
        "recursos": [
            {"text": "💉 Información sobre vacuna", "url": "https://www.who.int/es/news-room/fact-sheets/detail/hepatitis-b"}
        ]
    },
    
    "Tricomoniasis": {
        "info": """🟣 *Tricomoniasis*

*¿Qué es?*
ITS parasitaria causada por Trichomonas vaginalis.

*Transmisión:*
- Relaciones sexuales sin protección

*Síntomas (aparecen 5-28 días después de la exposición):*
*En mujeres:*
- Secreción vaginal espumosa, verde-amarillenta, con mal olor
- Picazón, ardor o enrojecimiento genital
- Molestia al orinar
- Dolor durante las relaciones sexuales

*En hombres:*
- Generalmente asintomático
- Irritación dentro del pene
- Ardor al orinar o eyacular
- Secreción del pene

*Complicaciones:*
- Mayor riesgo de contraer/transmitir VIH
- Parto prematuro en embarazadas
- Bajo peso al nacer

*Tratamiento:*
- Antibióticos (metronidazol o tinidazol)
- Abstinencia sexual hasta completar tratamiento
- Tratamiento de todas las parejas sexuales""",
        "recursos": []
    }
}

# --- Base de datos de centros de prueba en Puebla ---
centros_puebla = {
    "CAPASITS Puebla": {
        "direccion": "11 Sur 2904, Col. La Paz, Puebla, Pue.",
        "servicios": ["Pruebas de VIH", "Consejería", "Tratamiento antirretroviral"],
        "horario": "Lunes a Viernes 8:00-15:00",
        "costo": "Gratuito",
        "telefono": "+52 222 123 4567"
    },
    "Centro de Salud Urbano Puebla": {
        "direccion": "5 de Mayo 415, Centro Histórico, Puebla",
        "servicios": ["Pruebas de ITS", "Planificación familiar", "Vacunación"],
        "horario": "Lunes a Sábado 8:00-20:00",
        "costo": "Gratuito/Seguro Popular",
        "telefono": "+52 222 234 5678"
    },
    "Laboratorio Cholula": {
        "direccion": "Av. 14 Poniente 1915, San Pedro Cholula",
        "servicios": ["Paquetes de pruebas de ITS", "Resultados en 24h"],
        "horario": "Lunes a Sábado 7:00-20:00, Domingo 8:00-14:00",
        "costo": "$300-$1500 según pruebas",
        "telefono": "+52 222 345 6789"
    },
    "Clínica Condesa Puebla": {
        "direccion": "Av. Juárez 1906, Col. La Paz, Puebla",
        "servicios": ["Pruebas rápidas", "Profylaxis PrEP/PEP", "Atención especializada"],
        "horario": "Lunes a Viernes 9:00-17:00",
        "costo": "Gratuito para población vulnerable",
        "telefono": "+52 222 456 7890"
    }
}

curiosidades = [
    "🔍 El VIH no se transmite por abrazos, besos, compartir utensilios, picaduras de insectos o asientos de inodoro.",
    "💉 La prueba rápida de VIH puede darte resultados en menos de 30 minutos con solo una gota de sangre.",
    "🧠 Hablar de ITS no es tabú, es salud. ¡Infórmate y comparte! La educación sexual salva vidas.",
    "🌎 Más del 50% de las personas sexualmente activas tendrán VPH en algún momento de sus vidas.",
    "🧬 El herpes puede transmitirse incluso sin síntomas visibles, a través de lo que se llama 'diseminación asintomática'.",
    "📊 México reporta aproximadamente 12,000 nuevos casos de VIH cada año, según CENSIDA.",
    "🛡️ Usar condón reduce en un 98% el riesgo de contraer VIH y en un 60-70% el riesgo de contraer VPH.",
    "💊 La PrEP (profilaxis preexposición) puede reducir el riesgo de contraer VIH por sexo en más de un 90%.",
    "👥 Las personas entre 15 y 24 años representan el 50% de todas las nuevas ITS diagnosticadas anualmente.",
    "🧪 La sífilis congénita (transmitida de madre a hijo) ha resurgido en los últimos años, con un aumento del 200% en algunas regiones."
]

mitos = [
    {
        "mito": "❌ *Mito:* Solo las personas promiscuas tienen ITS.",
        "verdad": "✅ *Verdad:* Cualquier persona sexualmente activa puede contraer una ITS, independientemente de su número de parejas. Lo importante es la prevención y las pruebas regulares."
    },
    {
        "mito": "❌ *Mito:* Si no tengo síntomas, no tengo ITS.",
        "verdad": "✅ *Verdad:* Muchas ITS son asintomáticas, especialmente en etapas iniciales. La única forma de saber con certeza es mediante pruebas."
    },
    {
        "mito": "❌ *Mito:* El condón protege de todas las ITS al 100%.",
        "verdad": "✅ *Verdad:* Los condones son muy efectivos para prevenir muchas ITS, pero no protegen completamente contra aquellas que se transmiten por contacto piel a piel (como VPH o herpes)."
    },
    {
        "mito": "❌ *Mito:* Las ITS se curan con remedios caseros o automedicación.",
        "verdad": "✅ *Verdad:* El tratamiento debe ser siempre supervisado por profesionales de la salud. Los remedios caseros pueden enmascarar síntomas y empeorar la condición."
    },
    {
        "mito": "❌ *Mito:* Si tu pareja es 'limpia', no necesitas protección.",
        "verdad": "✅ *Verdad:* El concepto de 'limpieza' no aplica a las ITS. Muchas personas no saben que están infectadas. La protección es necesaria a menos que ambas partes se hayan hecho pruebas recientes."
    },
    {
        "mito": "❌ *Mito:* Las ITS solo afectan a ciertos grupos de personas.",
        "verdad": "✅ *Verdad:* Las ITS no discriminan por orientación sexual, género, edad o raza. Todas las personas sexualmente activas están en riesgo."
    },
    {
        "mito": "❌ *Mito:* Si ya tuviste una ITS, no puedes contraerla again.",
        "verdad": "✅ *Verdad:* Algunas ITS, como la clamidia o gonorrea, se pueden contraer múltiples veces. Otras, como el VIH o herpes, son infecciones de por vida."
    }
]

frases_motivadoras = [
    "🌄 Cada paso que das hacia tu salud es un acto de amor propio. ¡Celebra tu compromiso!",
    "💬 Hablar de ITS no te hace vulnerable, te hace valiente. Romper el estigma comienza contigo.",
    "🧭 La información es tu brújula. ¡Sigue explorando con confianza!",
    "🤝 Hoy es un buen día para priorizar tu salud sexual. Tu futuro yo te lo agradecerá.",
    "💪 Conocerte y cuidarte es la forma más poderosa de autocuidado. ¡Tú puedes!",
    "🌟 La prevención es el regalo más valioso que puedes darte a ti mismo y a tus parejas."
]

# --- Handlers mejorados ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = """
¡Hola! 👋 Soy tu bot de confianza para hablar de salud sexual sin tabúes.

📚 Aquí encontrarás información clara, científica y sin juicios sobre:
- Infecciones de transmisión sexual (ITS)
- Prevención y métodos de protección
- Pruebas y detección temprana
- Tratamientos y recursos disponibles
- Mitos y realidades sobre salud sexual

💬 Si tienes dudas, pregúntame con confianza. Estoy aquí para ayudarte a tomar decisiones informadas sobre tu salud.

*Comandos disponibles:*
/menu - Ver opciones principales
/dato - Aprender algo curioso
/mitos - Derribar conceptos erróneos
/pruebas - Encontrar centros de prueba
/emergencia - Recursos de ayuda inmediata
/glosario - Términos importantes

*Recuerda:* Este bot ofrece información general, no reemplaza la consulta con profesionales de la salud.
"""
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("VIH"), KeyboardButton("VPH"), KeyboardButton("Clamidia")],
        [KeyboardButton("Gonorrea"), KeyboardButton("Herpes"), KeyboardButton("Sífilis")],
        [KeyboardButton("Hepatitis B"), KeyboardButton("Tricomoniasis"), KeyboardButton("Prevención General")],
        [KeyboardButton("📍 Centros de prueba"), KeyboardButton("🆘 Recursos de emergencia")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(
        '¿Sobre qué aspecto de salud sexual quieres información? Selecciona una opción:',
        reply_markup=reply_markup
    )

async def dato(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dato = random.choice(curiosidades)
    keyboard = [[InlineKeyboardButton("📚 Más datos curiosos", callback_data="mas_datos")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(dato, reply_markup=reply_markup)

async def mitos_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mito = random.choice(mitos)
    texto = f"{mito['mito']}\n\n{mito['verdad']}"
    keyboard = [[InlineKeyboardButton("🧠 Más mitos y realidades", callback_data="mas_mitos")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(texto, parse_mode='Markdown', reply_markup=reply_markup)

async def pruebas_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = "📍 *Centros de prueba en Puebla:*\n\n"
    for centro, info in centros_puebla.items():
        texto += f"*{centro}*\n"
        texto += f"📍 {info['direccion']}\n"
        texto += f"🕒 {info['horario']}\n"
        texto += f"💰 {info['costo']}\n"
        texto += f"📞 {info['telefono']}\n"
        texto += f"🩺 Servicios: {', '.join(info['servicios'])}\n\n"
    
    texto += "¿Necesitas ayuda para elegir un centro o información sobre otras localidades?"
    await update.message.reply_text(texto, parse_mode='Markdown')

async def emergencia_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

async def glosario_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    glosario = """
*📖 Glosario de términos importantes:*

*ITS:* Infecciones de Transmisión Sexual. Infecciones que se transmiten principalmente por contacto sexual.

*PrEP:* Profilaxis Pre-Exposición. Medicamento para prevenir VIH en personas con alto riesgo.

*PEP:* Profilaxis Post-Exposición. Medicamento de emergencia para prevenir VIH después de posible exposición.

*Carga viral:* Cantidad de virus en la sangre de una persona. "Indetectable" significa que es tan baja que no puede transmitir VIH.

*Seroconversión:* Período en el que el cuerpo desarrolla anticuerpos detectables contra una infección.

*Asintomático:* Que no presenta síntomas. Muchas ITS son asintomáticas en etapas iniciales.

*Condón interno/femenino:* Método de barrera que se coloca dentro de la vagina o ano.

*Condón externo/masculino:* Método de barrera que se coloca sobre el pene.

*I=I:* Indetectable = Intransmisible. Personas con VIH y carga viral indetectable no transmiten el virus por vía sexual.
"""
    await update.message.reply_text(glosario, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()

    # Reconocimiento por palabra clave para ITS
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

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

# --- Construcción de la app Telegram ---
def build_app():
    application = Application.builder().token(TOKEN).build()
    
    # Handlers de comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("dato", dato))
    application.add_handler(CommandHandler("mitos", mitos_handler))
    application.add_handler(CommandHandler("pruebas", pruebas_handler))
    application.add_handler(CommandHandler("emergencia", emergencia_handler))
    application.add_handler(CommandHandler("glosario", glosario_handler))
    
    # Handlers de mensajes
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Handler de botones inline
    application.add_handler(CallbackQueryHandler(button_handler))
    
    return application

# --- Ejecución local ---
if __name__ == '__main__':
    app = build_app()
    print("Bot iniciado...")
    app.run_polling()
