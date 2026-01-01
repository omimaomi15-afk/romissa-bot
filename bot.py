from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import requests
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
HF_TOKEN = os.environ.get("HF_TOKEN")

SYSTEM_PROMPT = """
أنت الحاجة روميصة:
عجوزة جزائرية فكاهية،
تفهم جميع لهجات الجزائر،
تفهم العربية الفصحى،
وتهدر بالدارجة الجزائرية،
تنسى شوية وتضحك،
ما تكونش وقحة.
"""

def ask_ai(msg):
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}"
    }

    payload = {
        "inputs": f"{SYSTEM_PROMPT}\nالعضو قال: {msg}\nالحاجة روميصة:"
    }

    r = requests.post(
        "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-7B-Instruct",
        headers=headers,
        json=payload
    )

    return r.json()[0]["generated_text"]

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(ask_ai(update.message.text))

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
app.run_polling()

