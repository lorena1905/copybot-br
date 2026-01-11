from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

TOKEN = os.getenv("BOT_TOKEN")

def start(update, context):
    update.message.reply_text(
        "Oi! 👋\n"
        "Me envie no formato:\n"
        "Produto | Preço | Link"
    )

def gerar_copy(update, context):
    texto = update.message.text

    if "|" not in texto:
        update.message.reply_text(
            "Formato inválido ❌\n"
            "Use: Produto | Preço | Link"
        )
        return

    partes = [p.strip() for p in texto.split("|")]

    if len(partes) < 3:
        update.message.reply_text(
            "Formato incompleto ❌\n"
            "Use: Produto | Preço | Link"
        )
        return

    produto, preco, link = partes

    copy = (
        f"🔥 OFERTA IMPERDÍVEL 🔥\n\n"
        f"🛍️ {produto}\n"
        f"💰 Apenas {preco}\n\n"
        f"👉 Compre agora:\n{link}\n\n"
        f"⚠️ Corre que pode acabar!"
    )

    update.message.reply_text(copy)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, gerar_copy))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
