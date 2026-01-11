from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

import os

TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Olá! 🤖\n\n"
        "Me envie no formato:\n"
        "Produto | Preço | Link\n\n"
        "Que eu crio o anúncio pra você 🔥"
    )

async def gerar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text

    if "|" not in texto:
        return

    partes = texto.split("|")
    if len(partes) < 3:
        await update.message.reply_text("Use: Produto | Preço | Link")
        return

    produto = partes[0].strip()
    preco = partes[1].strip()
    link = partes[2].strip()

    resposta = (
        "🔥 OFERTA IMPERDÍVEL 🔥\n\n"
        f"🛍️ {produto}\n"
        f"💰 Apenas {preco}\n\n"
        f"👉 Compre aqui:\n{link}"
    )

    await update.message.reply_text(resposta)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, gerar))
app.run_polling()
